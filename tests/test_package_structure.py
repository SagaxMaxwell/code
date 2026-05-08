"""包结构和 notebook 基础检查。"""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
NOTEBOOKS = SRC / "python_notes" / "tutorials"


class PackageStructureTest(TestCase):
    """检查 src 包结构和导出约束。"""

    def test_package_imports(self) -> None:
        """核心包可以通过绝对路径导入。"""
        package = importlib.import_module("python_notes")

        self.assertEqual(package.__all__, ["examples", "tutorials"])

    def test_all_only_defined_in_init_files(self) -> None:
        """普通模块不定义 __all__。"""
        offenders: list[Path] = []
        for path in (SRC / "python_notes").rglob("*.py"):
            tree = ast.parse(path.read_text(), filename=str(path))
            has_all = any(
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
                for node in tree.body
            )
            if has_all and path.name != "__init__.py":
                offenders.append(path.relative_to(ROOT))

        self.assertEqual(offenders, [])

    def test_task_functions_without_broker(self) -> None:
        """任务函数的核心计算逻辑不依赖外部服务。"""
        celery_work = importlib.import_module("python_notes.examples.task_queues.celery.work")
        dramatiq_work = importlib.import_module("python_notes.examples.task_queues.dramatiq.work")

        self.assertEqual(celery_work.add.run(2, 3), 5)
        self.assertEqual(celery_work.multiply.run(2, 3), 6)
        self.assertEqual(celery_work.sum_numbers.run([1, 2, 3]), 6)
        self.assertEqual(dramatiq_work.add.fn(2, 3), 5)
        self.assertEqual(dramatiq_work.multiply.fn(2, 3), 6)


class ArqTaskTest(IsolatedAsyncioTestCase):
    """检查 ARQ 协程任务的核心逻辑。"""

    async def test_arq_tasks_without_worker(self) -> None:
        """ARQ 任务函数可直接执行核心计算。"""
        arq_work = importlib.import_module("python_notes.examples.task_queues.arq.work")
        ctx = {"processed_jobs": 0, "job_try": 3}

        self.assertEqual(await arq_work.add(ctx, 3, 7), 10)
        self.assertEqual(await arq_work.multiply(ctx, 6, 7), 42)
        self.assertEqual(await arq_work.flaky_job(ctx, 21), 42)


class NotebookSyntaxTest(TestCase):
    """检查 notebook JSON 和代码单元语法。"""

    def test_notebooks_are_valid_json(self) -> None:
        """所有 notebook 都是合法 JSON。"""
        notebooks = sorted(NOTEBOOKS.rglob("*.ipynb"))

        self.assertGreater(len(notebooks), 0)
        for path in notebooks:
            data = json.loads(path.read_text())
            self.assertEqual(data["nbformat"], 4)
            self.assertIn("cells", data)

    def test_code_cells_parse(self) -> None:
        """所有代码单元都能通过 Python 语法解析。"""
        failures: list[str] = []
        for path in sorted(NOTEBOOKS.rglob("*.ipynb")):
            data = json.loads(path.read_text())
            for index, cell in enumerate(data.get("cells", [])):
                if cell.get("cell_type") != "code":
                    continue
                source = "".join(cell.get("source", []))
                try:
                    ast.parse(source, filename=f"{path}:{index}")
                except SyntaxError as exc:
                    failures.append(f"{path.relative_to(ROOT)} cell {index}: {exc}")

        self.assertEqual(failures, [])
