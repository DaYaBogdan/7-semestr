from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


# =====================================================================
# 1. ADAPTER — унификация несовместимых платёжных API
# =====================================================================

class PayPalAPI:
    def send_payment(self, amount_usd: float) -> None:
        print(f"PayPal: списано {amount_usd} USD")


class StripeAPI:
    def charge(self, amount: float, currency: str = "USD") -> None:
        print(f"Stripe: списано {amount} {currency}")


class CryptoAPI:
    def make_tx(self, amount: float) -> None:
        print(f"Crypto: транзакция на {amount}")


class PaymentGateway(ABC):
    """Целевой интерфейс (Target)."""

    @abstractmethod
    def pay(self, amount: float, currency: str = "USD") -> None: ...


class PayPalAdapter(PaymentGateway):
    def __init__(self, api: PayPalAPI) -> None:
        self._api = api

    def pay(self, amount: float, currency: str = "USD") -> None:
        self._api.send_payment(amount)


class StripeAdapter(PaymentGateway):
    def __init__(self, api: StripeAPI) -> None:
        self._api = api

    def pay(self, amount: float, currency: str = "USD") -> None:
        self._api.charge(amount, currency)


class CryptoAdapter(PaymentGateway):
    def __init__(self, api: CryptoAPI) -> None:
        self._api = api

    def pay(self, amount: float, currency: str = "USD") -> None:
        self._api.make_tx(amount)


# =====================================================================
# 2. FACADE — единая точка входа для подсистемы заказа
# =====================================================================

class SeatService:
    def reserve(self, seat: str) -> None:
        print(f"SeatService: место {seat} зарезервировано")


class TicketPrinter:
    def print_ticket(self, seat: str) -> None:
        print(f"TicketPrinter: билет на место {seat} напечатан")


class OrderFacade:
    """Скрывает взаимодействие трёх классов подсистемы."""

    def __init__(self,
                 seats: SeatService,
                 pay: PaymentGateway,
                 printer: TicketPrinter) -> None:
        self._seats = seats
        self._pay = pay
        self._printer = printer

    def buy(self, seat: str, amount: float) -> None:
        self._seats.reserve(seat)
        self._pay.pay(amount)
        self._printer.print_ticket(seat)


# =====================================================================
# 3. DECORATOR — комбинируемые уведомления
# =====================================================================

class Notifier(ABC):
    @abstractmethod
    def notify(self, text: str) -> None: ...


class EmailNotifier(Notifier):
    def notify(self, text: str) -> None:
        print(f"EMAIL: {text}")


class SmsNotifier(Notifier):
    def notify(self, text: str) -> None:
        print(f"SMS: {text}")


class NotifierDecorator(Notifier):
    def __init__(self, wrapped: Notifier) -> None:
        self._wrapped = wrapped

    def notify(self, text: str) -> None:
        self._wrapped.notify(text)


class WithPrefix(NotifierDecorator):
    def __init__(self, wrapped: Notifier, prefix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix

    def notify(self, text: str) -> None:
        super().notify(f"[{self._prefix}] {text}")


class MultiNotifier(NotifierDecorator):
    """Склеивает несколько каналов уведомления."""

    def __init__(self, wrapped: Notifier, extra: Notifier) -> None:
        super().__init__(wrapped)
        self._extra = extra

    def notify(self, text: str) -> None:
        super().notify(text)
        self._extra.notify(text)


# =====================================================================
# 4. BRIDGE — разделение MediaPlayer и его реализаций
# =====================================================================

class MediaImpl(ABC):
    @abstractmethod
    def render_video(self, f: str) -> None: ...
    @abstractmethod
    def render_audio(self, f: str) -> None: ...
    @abstractmethod
    def render_subs(self, f: str) -> None: ...


class BasicImpl(MediaImpl):
    def render_video(self, f: str) -> None: print(f"video {f}")
    def render_audio(self, f: str) -> None: print(f"audio {f}")
    def render_subs(self, f: str) -> None: print(f"subs {f}")


class HDImpl(MediaImpl):
    def render_video(self, f: str) -> None: print(f"HD video {f}")
    def render_audio(self, f: str) -> None: print(f"HD audio {f}")
    def render_subs(self, f: str) -> None: print(f"HD subs {f}")


class MediaPlayer(ABC):
    def __init__(self, impl: MediaImpl) -> None:
        self._impl = impl

    @abstractmethod
    def play(self, f: str) -> None: ...


class VideoPlayer(MediaPlayer):
    def play(self, f: str) -> None:
        self._impl.render_video(f)


class AudioPlayer(MediaPlayer):
    def play(self, f: str) -> None:
        self._impl.render_audio(f)


# =====================================================================
# 5. COMPOSITE — дерево меню кинотеатра
# =====================================================================

class MenuComponent(ABC):
    @abstractmethod
    def render(self, indent: int = 0) -> None: ...


class MenuItem(MenuComponent):
    def __init__(self, name: str) -> None:
        self._name = name

    def render(self, indent: int = 0) -> None:
        print(" " * indent + f"- {self._name}")


class Menu(MenuComponent):
    def __init__(self, name: str) -> None:
        self._name = name
        self._children: List[MenuComponent] = []

    def add(self, c: MenuComponent) -> None:
        self._children.append(c)

    def render(self, indent: int = 0) -> None:
        print(" " * indent + f"+ {self._name}")
        for c in self._children:
            c.render(indent + 2)


# =====================================================================
# 6. PROXY — ленивая загрузка трейлера
# =====================================================================

class Trailer(ABC):
    @abstractmethod
    def play(self) -> None: ...


class RealTrailer(Trailer):
    def __init__(self, url: str) -> None:
        self._url = url

    def play(self) -> None:
        print(f"playing {self._url}")


class TrailerProxy(Trailer):
    def __init__(self, url: str) -> None:
        self._url = url
        self._real: RealTrailer | None = None

    def play(self) -> None:
        if self._real is None:
            print("lazy load...")
            self._real = RealTrailer(self._url)
        self._real.play()


# =====================================================================
# 7. FLYWEIGHT — совместное использование данных о залах
# =====================================================================

class HallType:
    """Неизменяемое разделяемое состояние."""

    def __init__(self, name: str, rows: int, cols: int) -> None:
        self.name = name
        self.rows = rows
        self.cols = cols

    def __repr__(self) -> str:
        return f"HallType({self.name}, {self.rows}x{self.cols})"


class HallFactory:
    _cache: dict[str, HallType] = {}

    @classmethod
    def get(cls, name: str, rows: int, cols: int) -> HallType:
        key = f"{name}:{rows}x{cols}"
        if key not in cls._cache:
            cls._cache[key] = HallType(name, rows, cols)
        return cls._cache[key]


class Hall:
    """Контекст: ссылка на разделяемый HallType + уникальные данные."""

    def __init__(self, hall_id: int, htype: HallType) -> None:
        self.hall_id = hall_id
        self.htype = htype


# =====================================================================
# ДЕМОНСТРАЦИЯ
# =====================================================================

def main() -> None:
    print("=== ЛР №5: Структурные паттерны ===\n")

    print("--- Adapter + Facade ---")
    gateway = StripeAdapter(StripeAPI())
    facade = OrderFacade(SeatService(), gateway, TicketPrinter())
    facade.buy("A12", 250.0)

    print("\n--- Decorator ---")
    notifier = WithPrefix(
        MultiNotifier(EmailNotifier(), SmsNotifier()), "Cinema"
    )
    notifier.notify("Ваш билет забронирован")

    print("\n--- Bridge ---")
    VideoPlayer(HDImpl()).play("trailer.mp4")
    AudioPlayer(BasicImpl()).play("trailer.mp3")

    print("\n--- Composite ---")
    root = Menu("Главное меню")
    root.add(MenuItem("Афиша"))
    films = Menu("Фильмы")
    films.add(MenuItem("Фантастика"))
    films.add(MenuItem("Комедии"))
    root.add(films)
    root.render()

    print("\n--- Proxy ---")
    TrailerProxy("http://cdn/trailer.mp4").play()

    print("\n--- Flyweight ---")
    a = Hall(1, HallFactory.get("IMAX", 20, 30))
    b = Hall(2, HallFactory.get("IMAX", 20, 30))
    print(a.htype, "| shared:", a.htype is b.htype)
    c = Hall(3, HallFactory.get("IMAX", 10, 15))
    print(c.htype, "| shared with a:", a.htype is c.htype)


if __name__ == "__main__":
    main()