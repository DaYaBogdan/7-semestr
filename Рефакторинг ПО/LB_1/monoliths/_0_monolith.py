# monolith.py
import json
import os
from datetime import datetime


class OrderProcessor:

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
            discount = 0.0
            if user.get("vip") and o["amount"] > 1000:
                discount = o["amount"] * 0.15
            elif user.get("vip"):
                discount = o["amount"] * 0.05
            elif o["amount"] > 1000:
                discount = o["amount"] * 0.03
            else:
                discount = 0.0

            country = user.get("country", "RU")
            if country == "RU":
                tax = (o["amount"] - discount) * 0.2
            elif country == "US":
                tax = (o["amount"] - discount) * 0.07
            elif country == "DE":
                tax = (o["amount"] - discount) * 0.19
            else:
                tax = 0.0

            final = o["amount"] - discount + tax

            total = total + final
            count = count + 1
            if final > max_amount:
                max_amount = final
            if final < min_amount:
                min_amount = final

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