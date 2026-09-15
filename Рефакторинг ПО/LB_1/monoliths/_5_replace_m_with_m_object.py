# monolith.py
import json
import os
from datetime import datetime

class Stats:
    def __init__(self):
        self.total = 0.0
        self.count = 0
        self.max = 0.0
        self.min = float("inf")

    def add(self, value):
        self.total += value
        self.count += 1
        self.max = max(self.max, value)
        self.min = min(self.min, value)

    def avg(self):
        return self.total / self.count if self.count else 0.0

class OrderProcessingRun:

    def __init__(self, orders_file, users_file, config, db_conn,
                 send_email=True, dry_run=False, log_level="INFO"):
        self.orders_file = orders_file
        self.users_file = users_file
        self.config = config
        self.db_conn = db_conn
        self.send_email = send_email
        self.dry_run = dry_run
        self.log_level = log_level

        self.result = []
        self.errors = []
        self.stats = Stats()
        self.orders = []
        self.users = []
        self.users_by_id = {}
        
# -------------------------------------------------------------------------

    def _calc_discount(self, user, amount):
        if user.get("vip") and amount > 1000:
            return amount * 0.15
        if user.get("vip"):
            return amount * 0.05
        if amount > 1000:
            return amount * 0.03
        return 0.0

    def _calc_tax(self, country, base):
        if country == "RU":
            return base * 0.2
        if country == "US":
            return base * 0.07
        if country == "DE":
            return base * 0.19
        return 0.0

    def _final_amount(self, order, user):
        discount = self._calc_discount(user, order["amount"])
        country = user.get("country", "RU")
        tax = self._calc_tax(country, order["amount"] - discount)
        return order["amount"] - discount + tax

# -------------------------------------------------------------------------

    def _validate_order(self, order, users_by_id):
        required = ("id", "user_id", "amount")
        if not all(k in order for k in required):
            return "order missing fields: " + str(order)
        if order["amount"] <= 0:
            return "order amount <= 0: " + str(order["id"])
        if order["user_id"] not in users_by_id:
            return "unknown user: " + str(order["user_id"])
        return None
   
    def _load_json(self, path):
        if not os.path.exists(path):
            return None, "file not found: " + path
        with open(path, "r") as f:
            raw = f.read()
        try:
            return json.loads(raw), None
        except Exception as e:
            return None, "bad json: " + str(e)
    
    def _build_row(self, order, user, discount, tax, final):
        return {
            "order_id": order["id"],
            "user": user.get("name", "unknown"),
            "amount": order["amount"],
            "discount": discount,
            "tax": tax,
            "final": final,
            "ts": datetime.now().isoformat(),
        }

    def _send_email(self, user, order):
        print("EMAIL to", user.get("email"), "order", order["id"])

    def _persist(self, db_conn, order, user, final, country, ts):
        db_conn.execute(
            "INSERT INTO orders VALUES (?,?,?,?,?)",
            (order["id"], user["id"], final, country, ts),
        )
# -------------------------------------------------------------------------

    def compute(self):
        if not self._load():
            return self._response()
        self._process_orders()
        self._log()
        return self._response()

    def _load(self):
        self.orders, err = self._load_json(self.orders_file)
        if err:
            self.errors.append(err)
            return False
        self.users, err = self._load_json(self.users_file)
        if err:
            self.errors.append(err)
            return False
        self.users_by_id = {u["id"]: u for u in self.users}
        return True

    def _process_orders(self):
        should_email = self.send_email and not self.dry_run
        should_persist = not self.dry_run and self.db_conn is not None

        for o in self.orders:
            err = self._validate_order(o, self.users_by_id)
            if err:
                self.errors.append(err)
                continue

            user = self.users_by_id[o["user_id"]]
            discount = self._calc_discount(user, o["amount"])
            country = user.get("country", "RU")
            tax = self._calc_tax(country, o["amount"] - discount)
            final = o["amount"] - discount + tax

            self.stats.add(final)
            row = self._build_row(o, user, discount, tax, final)
            self.result.append(row)

            if should_email:
                self._send_email(user, o)
            if should_persist:
                self._persist(self.db_conn, o, user, final, country, row["ts"])

    def _response(self):
        return {
            "ok": len(self.errors) == 0,
            "errors": self.errors,
            "data": self.result,
            "summary": self._build_summary(),
            "config_used": self.config,
        }

    def _build_summary(self):
        if self.stats.count == 0:
            return "No valid orders"
        return "Orders: %d, Total: %.2f, Avg: %.2f, Min: %.2f, Max: %.2f" % (
            self.stats.count, self.stats.total, self.stats.avg(),
            self.stats.min, self.stats.max,
        )
      
                
class OrderProcessor:
    def process_orders(self, orders_file, users_file, config, db_conn,
                       send_email=True, dry_run=False, log_level="INFO"):
        return OrderProcessingRun(
            orders_file, users_file, config, db_conn,
            send_email, dry_run, log_level,
        ).compute()
    