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

    def process_orders(self, orders_file, users_file, config, db_conn,
                       send_email=True, dry_run=False, log_level="INFO"):
        result = []
        errors = []
        if not os.path.exists(orders_file):
            errors.append("orders file not found: " + orders_file)
            return {"ok": False, "errors": errors, "data": result}
        with open(orders_file, "r") as f:
            raw = f.read()
        try:
            orders = json.loads(raw)
        except Exception as e:
            errors.append("bad json: " + str(e))
            return {"ok": False, "errors": errors, "data": result}

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

        for o in orders:
            if "id" not in o or "user_id" not in o or "amount" not in o:
                errors.append("order missing fields: " + str(o))
                continue
            if o["amount"] <= 0:
                errors.append("order amount <= 0: " + str(o["id"]))
                continue
            if o["user_id"] not in users_by_id:
                errors.append("unknown user: " + str(o["user_id"]))
                continue

            user = users_by_id[o["user_id"]]
            discount = self._calc_discount(user, o["amount"])
            country = user.get("country", "RU")
            tax = self._calc_tax(country, o["amount"] - discount)
            final = o["amount"] - discount + tax

            row = {
                "order_id": o["id"],
                "user": user.get("name", "unknown"),
                "amount": o["amount"],
                "discount": discount,
                "tax": tax,
                "final": final,
                "ts": datetime.now().isoformat(),
            }
            result.append(row)

            total = total + final
            count = count + 1
            if final > max_amount:
                max_amount = final
            if final < min_amount:
                min_amount = final

            if send_email and not dry_run:
                print("EMAIL to", user.get("email"), "order", o["id"])

            if send_email and not dry_run:
                print("EMAIL to", user.get("email"), "order", o["id"])

            if not dry_run and db_conn is not None:
                db_conn.execute(
                    "INSERT INTO orders VALUES (?,?,?,?,?)",
                    (o["id"], user["id"], final, country, row["ts"]),
                )

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