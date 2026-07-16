"""Pydantic 工具 notebook 测试。"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "src"
    / "python_notes"
    / "tutorials"
    / "tools"
    / "pydantic.ipynb"
)


def load_notebook_namespace() -> dict[str, object]:
    """执行 Pydantic notebook。"""
    data = json.loads(NOTEBOOK.read_text())
    namespace: dict[str, object] = {"__name__": "__pydantic_tools_notebook__"}
    for index, cell in enumerate(data["cells"]):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        exec(
            compile(source, f"{NOTEBOOK}:{index}", "exec", dont_inherit=True), namespace
        )
    return namespace


class PydanticToolsTest(TestCase):
    """检查 Pydantic 示例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """缓存 notebook 命名空间。"""
        cls.namespace = load_notebook_namespace()

    def test_parse_order_normalizes_and_computes_total(self) -> None:
        """单个订单会被校验，并生成计算字段。"""
        order_class = self.namespace["Order"]
        parse_order = self.namespace["parse_order"]

        order = parse_order(
            {
                "order_id": " ORD-001 ",
                "user_id": " USER-001 ",
                "status": "paid",
                "items": [
                    {"sku_id": " SKU-1 ", "quantity": 2, "unit_price": "12.50"},
                    {"sku_id": "SKU-2", "quantity": 1, "unit_price": 3.5},
                ],
            }
        )

        self.assertIsInstance(order, order_class)
        self.assertEqual(order.order_id, "ORD-001")
        self.assertEqual(order.items[0].sku_id, "SKU-1")
        self.assertEqual(order.items[1].unit_price, Decimal("3.5"))
        self.assertEqual(order.total_amount, Decimal("28.50"))

    def test_parse_orders_from_json(self) -> None:
        """订单列表可以从 JSON 文本批量解析。"""
        parse_orders = self.namespace["parse_orders"]
        raw_orders = [
            {
                "order_id": "ORD-001",
                "user_id": "USER-001",
                "items": [{"sku_id": "SKU-1", "quantity": 2, "unit_price": "12.50"}],
            }
        ]

        orders = parse_orders(json.dumps(raw_orders))

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].status, "pending")
        self.assertEqual(orders[0].total_amount, Decimal("25.00"))

    def test_dump_order_uses_json_safe_values(self) -> None:
        """导出的订单字典会使用 JSON 友好的字段值。"""
        dump_order = self.namespace["dump_order"]
        parse_order = self.namespace["parse_order"]

        order = parse_order(
            {
                "order_id": "ORD-001",
                "user_id": "USER-001",
                "items": [{"sku_id": "SKU-1", "quantity": 2, "unit_price": "12.50"}],
            }
        )

        data = dump_order(order)

        self.assertEqual(data["total_amount"], "25.00")
        self.assertEqual(data["items"][0]["unit_price"], "12.50")
        self.assertEqual(data["items"][0]["line_total"], "25.00")

    def test_order_schema_describes_model(self) -> None:
        """JSON Schema 会包含订单模型字段描述。"""
        order_schema = self.namespace["order_schema"]

        schema = order_schema()

        self.assertEqual(schema["title"], "Order")
        self.assertIn("items", schema["properties"])

    def test_summarize_validation_error(self) -> None:
        """校验异常可以整理成带字段路径的错误消息。"""
        parse_order = self.namespace["parse_order"]
        summarize_validation_error = self.namespace["summarize_validation_error"]

        with self.assertRaises(ValidationError) as context:
            parse_order(
                {
                    "order_id": "ORD-001",
                    "user_id": "USER-001",
                    "items": [{"sku_id": "", "quantity": 0, "unit_price": "0"}],
                }
            )

        messages = summarize_validation_error(context.exception)

        self.assertTrue(
            any(message.startswith("items.0.sku_id:") for message in messages)
        )
        self.assertTrue(
            any(message.startswith("items.0.quantity:") for message in messages)
        )
        self.assertTrue(
            any(message.startswith("items.0.unit_price:") for message in messages)
        )
