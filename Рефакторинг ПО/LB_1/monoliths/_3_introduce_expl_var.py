# monolith.py
import json
import os
from datetime import datetime


class OrderProcessor:

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

    def process_orders(self, orders_file, users_file, config, db_conn,
                       send_email=True, dry_run=False, log_level="INFO"):
        result = []
        errors = []
        orders, err = self._load_json(orders_file)
        if err:
            return {"ok": False, "errors": [err], "data": []}

        users, err = self._load_json(users_file)
        if err:
            return {"ok": False, "errors": [err], "data": []}

        if not os.path.exists(users_file):
            errors.append("users file not found: " + users_file)
            return {"ok": False, "errors": errors, "data": result}
        with open(users_file, "r") as f:
            users = json.loads(f.read())

        total = 0.0
        count = 0
        max_amount = 0.0
        min_amount = 999999999.0
        users_by_id = {}
        
        for u in users:
            users_by_id[u["id"]] = u

        should_email = send_email and not dry_run
        should_persist = not dry_run and db_conn is not None

        for o in orders:
            
            err = self._validate_order(o, users_by_id)
            if err:
                errors.append(err)
                continue

            user = users_by_id[o["user_id"]]
            discount = self._calc_discount(user, o["amount"])
            country = user.get("country", "RU")
            tax = self._calc_tax(country, o["amount"] - discount)
            final = o["amount"] - discount + tax

            result.append(row)

            total = total + final
            count = count + 1
            if final > max_amount:
                max_amount = final
            if final < min_amount:
                min_amount = final

            row = self._build_row(o, user, discount, tax, final)
            result.append(row)
            
            if should_email:
                self._send_email(user, o)
            if should_persist:
                self._persist(db_conn, o, user, final, country, row["ts"])

        if log_level == "DEBUG":
            print("DEBUG processed", count, "orders, total", total)
        elif log_level == "INFO":
            print("INFO processed", count, "orders")
        elif log_level == "WARN":
            pass
        else:
            print("UNKNOWN log level", log_level)

        summary = ""
        if count > 0:
            avg = total / count
            summary = "Orders: %d, Total: %.2f, Avg: %.2f, Min: %.2f, Max: %.2f" % (
                count, total, avg, min_amount, max_amount,
            )
        else:
            summary = "No valid orders"

        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "data": result,
            "summary": summary,
            "config_used": config,
        }