# test_monolith.py
import json
import pytest
from monoliths._5_replace_m_with_m_object import OrderProcessor


class FakeDB:
    def __init__(self):
        self.rows = []

    def execute(self, sql, params):
        self.rows.append(params)


@pytest.fixture
def files(tmp_path):
    users = [
        {"id": 1, "name": "Alice", "vip": True,  "country": "RU", "email": "a@x"},
        {"id": 2, "name": "Bob",   "vip": False, "country": "US", "email": "b@x"},
        {"id": 3, "name": "Carl",  "vip": False, "country": "DE", "email": "c@x"},
    ]
    orders = [
        {"id": 101, "user_id": 1, "amount": 2000},  # vip + large → 15%
        {"id": 102, "user_id": 2, "amount": 500},   # no vip, small → 0%
        {"id": 103, "user_id": 3, "amount": 1500},  # no vip, large → 3%
        {"id": 104, "user_id": 99, "amount": 100},  # unknown user
        {"id": 105, "user_id": 1, "amount": -5},    # bad amount
        {"id": 106, "user_id": 2},                  # missing fields
    ]
    up = tmp_path / "users.json"
    op = tmp_path / "orders.json"
    up.write_text(json.dumps(users))
    op.write_text(json.dumps(orders))
    return str(op), str(up)


def test_basic_run(files):
    op, up = files
    db = FakeDB()
    r = OrderProcessor().process_orders(op, up, {"k": 1}, db, send_email=False)

    assert r["ok"] is False
    assert len(r["data"]) == 3
    assert len(r["errors"]) == 3
    assert len(db.rows) == 3
    assert r["summary"].startswith("Orders: 3, Total:")

    # Проверяем расчёты первой строки (vip + large, RU)
    first = r["data"][0]
    assert first["order_id"] == 101
    assert first["discount"] == pytest.approx(300.0)   # 2000 * 0.15
    assert first["tax"]      == pytest.approx(340.0)   # (2000-300) * 0.20
    assert first["final"]    == pytest.approx(2040.0)  # 2000-300+340


def test_dry_run_no_side_effects(files):
    op, up = files
    db = FakeDB()
    r = OrderProcessor().process_orders(op, up, {}, db, send_email=True, dry_run=True)
    assert db.rows == []
    assert len(r["data"]) == 3


def test_missing_orders_file(tmp_path):
    r = OrderProcessor().process_orders(
        str(tmp_path / "no.json"), str(tmp_path / "no2.json"), {}, None
    )
    assert r["ok"] is False
    assert "orders file not found" in r["errors"][0]


def test_missing_users_file(tmp_path):
    op = tmp_path / "orders.json"
    op.write_text(json.dumps([{"id": 1, "user_id": 1, "amount": 100}]))
    r = OrderProcessor().process_orders(
        str(op), str(tmp_path / "no_users.json"), {}, None
    )
    assert r["ok"] is False
    assert "users file not found" in r["errors"][0]


def test_bad_json(tmp_path):
    op = tmp_path / "orders.json"
    op.write_text("{not valid json")
    up = tmp_path / "users.json"
    up.write_text("[]")
    r = OrderProcessor().process_orders(str(op), str(up), {}, None)
    assert r["ok"] is False
    assert "bad json" in r["errors"][0]