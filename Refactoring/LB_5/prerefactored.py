# ---- до рефакторинга ----

class PayPalAPI:
    def send_payment(self, amount_usd):
        print(f"PayPal: списано {amount_usd} USD")

class StripeAPI:
    def charge(self, amount, currency="USD"):
        print(f"Stripe: списано {amount} {currency}")

class CryptoAPI:
    def make_tx(self, amount):
        print(f"Crypto: транзакция на {amount}")


class Cinema:
    def __init__(self):
        self.paypal = PayPalAPI()
        self.stripe = StripeAPI()
        self.crypto = CryptoAPI()

    def buy_ticket(self, amount, method):
        if method == "paypal":
            self.paypal.send_payment(amount)
        elif method == "stripe":
            self.stripe.charge(amount)
        elif method == "crypto":
            self.crypto.make_tx(amount)


class EmailSender:
    def send(self, text):
        print(f"EMAIL: {text}")


class Notifier:
    # жёстко зашит только email
    def __init__(self):
        self.email = EmailSender()
    def notify(self, text):
        self.email.send(text)


class MediaPlayer:
    # «раздутый» интерфейс: видео + аудио + субтитры
    def play_video(self, f): print(f"video {f}")
    def play_audio(self, f): print(f"audio {f}")
    def show_subtitles(self, f): print(f"subs {f}")


class SeatService:
    def reserve(self, seat): print(f"reserve {seat}")
class PaymentService:
    def pay(self, amount): print(f"pay {amount}")
class TicketPrinter:
    def print_ticket(self, seat): print(f"ticket {seat}")


class OrderClient:
    # клиент работает со всеми классами подсистемы напрямую
    def order(self, seat, amount):
        SeatService().reserve(seat)
        PaymentService().pay(amount)
        TicketPrinter().print_ticket(seat)