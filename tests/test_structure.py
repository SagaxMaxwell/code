"""包结构和 notebook 基础检查。"""

from __future__ import annotations

import ast
import importlib
import json
import re
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
NOTEBOOK_ROOTS = [
    SRC / "python_notes" / "tutorials",
    SRC / "python_notes" / "exercises",
]
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+\s*)?$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")


def iter_notebooks() -> list[Path]:
    """返回项目内所有 notebook。"""
    return [path for root in NOTEBOOK_ROOTS for path in sorted(root.rglob("*.ipynb"))]


def toggle_markdown_fence(
    line: str, in_fence: bool, marker: str | None
) -> tuple[bool, str | None]:
    """跟踪 Markdown 代码围栏，避免把代码注释当标题。"""
    match = FENCE_RE.match(line)
    if not match:
        return in_fence, marker

    current = match.group(1)[0] * 3
    if not in_fence:
        return True, current
    if marker == current:
        return False, None
    return in_fence, marker


class PackageStructureTest(TestCase):
    """检查包结构。"""

    def test_package_imports(self) -> None:
        """核心包可以通过绝对路径导入。"""
        package = importlib.import_module("python_notes")

        self.assertEqual(
            package.__all__, ["examples", "exercises", "resources", "tutorials"]
        )

    def test_all_only_defined_in_init_files(self) -> None:
        """普通模块不定义 __all__。"""
        offenders: list[Path] = []
        for path in (SRC / "python_notes").rglob("*.py"):
            tree = ast.parse(path.read_text(), filename=str(path))
            has_all = any(
                isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == "__all__"
                    for target in node.targets
                )
                for node in tree.body
            )
            if has_all and path.name != "__init__.py":
                offenders.append(path.relative_to(ROOT))

        self.assertEqual(offenders, [])

    def test_task_functions_without_broker(self) -> None:
        """任务函数可直接测试。"""
        celery_work = importlib.import_module(
            "python_notes.examples.task_queues.celery.tasks"
        )
        dramatiq_work = importlib.import_module(
            "python_notes.examples.task_queues.dramatiq.tasks"
        )

        self.assertEqual(celery_work.add.run(2, 3), 5)
        self.assertEqual(celery_work.multiply.run(2, 3), 6)
        self.assertEqual(celery_work.sum_numbers.run([1, 2, 3]), 6)
        self.assertEqual(dramatiq_work.add.fn(2, 3), 5)
        self.assertEqual(dramatiq_work.multiply.fn(2, 3), 6)


class ArqTaskTest(IsolatedAsyncioTestCase):
    """检查 ARQ 任务。"""

    async def test_arq_tasks_without_worker(self) -> None:
        """ARQ 任务可直接执行。"""
        arq_work = importlib.import_module("python_notes.examples.task_queues.arq.tasks")
        ctx = {"processed_jobs": 0, "job_try": 3}

        self.assertEqual(await arq_work.add(ctx, 3, 7), 10)
        self.assertEqual(await arq_work.multiply(ctx, 6, 7), 42)
        self.assertEqual(await arq_work.flaky_job(ctx, 21), 42)


class NotebookSyntaxTest(TestCase):
    """检查 notebook 语法。"""

    def test_notebooks_are_valid_json(self) -> None:
        """所有 notebook 都是合法 JSON。"""
        notebooks = iter_notebooks()

        self.assertGreater(len(notebooks), 0)
        for path in notebooks:
            data = json.loads(path.read_text())
            self.assertEqual(data["nbformat"], 4)
            self.assertIn("cells", data)

    def test_code_cells_parse(self) -> None:
        """Python 代码单元可解析。"""
        failures: list[str] = []
        for path in iter_notebooks():
            data = json.loads(path.read_text())
            for index, cell in enumerate(data.get("cells", [])):
                if cell.get("cell_type") != "code":
                    continue
                source = "".join(cell.get("source", []))
                if source.lstrip().startswith(("%", "!", "?")):
                    continue
                try:
                    ast.parse(source, filename=f"{path}:{index}")
                except SyntaxError as exc:
                    failures.append(f"{path.relative_to(ROOT)} cell {index}: {exc}")

        self.assertEqual(failures, [])

    def test_markdown_cells_have_consistent_structure(self) -> None:
        """Markdown 单元有一致的标题层级和基础格式。"""
        failures: list[str] = []
        for path in iter_notebooks():
            data = json.loads(path.read_text())
            headings: list[tuple[int, int, str]] = []
            for cell_index, cell in enumerate(data.get("cells", []), 1):
                if cell.get("cell_type") != "markdown":
                    continue

                source = "".join(cell.get("source", []))
                if not source.strip():
                    failures.append(
                        f"{path.relative_to(ROOT)} cell {cell_index}: empty markdown"
                    )
                if "\u00a0" in source:
                    failures.append(
                        f"{path.relative_to(ROOT)} cell {cell_index}: contains NBSP"
                    )
                for line_number, line in enumerate(source.splitlines(), 1):
                    if line.rstrip() != line:
                        failures.append(
                            f"{path.relative_to(ROOT)} cell {cell_index} "
                            f"line {line_number}: trailing whitespace"
                        )

                in_fence = False
                fence_marker: str | None = None
                lines = source.splitlines()
                for line_number, line in enumerate(lines, 1):
                    in_fence, fence_marker = toggle_markdown_fence(
                        line, in_fence, fence_marker
                    )
                    if in_fence or FENCE_RE.match(line):
                        continue

                    match = HEADING_RE.match(line.strip())
                    if not match:
                        continue

                    level = len(match.group(1))
                    title = match.group(2).strip()
                    headings.append((cell_index, level, title))

                    next_line = lines[line_number] if line_number < len(lines) else ""
                    if next_line.strip() and not HEADING_RE.match(next_line.strip()):
                        failures.append(
                            f"{path.relative_to(ROOT)} cell {cell_index} "
                            f"line {line_number}: missing blank line after heading"
                        )

            if not headings:
                failures.append(f"{path.relative_to(ROOT)}: missing markdown headings")
                continue

            h1_count = sum(1 for _, level, _ in headings if level == 1)
            if h1_count != 1:
                failures.append(f"{path.relative_to(ROOT)}: expected one H1")
            if headings[0][1] != 1:
                failures.append(f"{path.relative_to(ROOT)}: first heading is not H1")

            previous_level = headings[0][1]
            for cell_index, level, title in headings[1:]:
                if level > previous_level + 1:
                    failures.append(
                        f"{path.relative_to(ROOT)} cell {cell_index}: "
                        f"heading jumps H{previous_level} to H{level} ({title})"
                    )
                previous_level = level

        self.assertEqual(failures, [])
