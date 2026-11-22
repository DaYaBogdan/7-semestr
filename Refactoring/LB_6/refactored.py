from __future__ import annotations

import copy
import threading
from abc import ABC, abstractmethod


# =====================================================================
# 1. BUILDER — пошаговое создание Ticket (вместо телескопического
#    конструктора с 8 параметрами)
# =====================================================================

class Ticket:
    def __init__(self, b: "TicketBuilder") -> None:
        self.film = b.film
        self.seat = b.seat
        self.price = b.price
        self.extras = set(b.extras)
        self.discount = b.discount
        self.comment = b.comment

    def __str__(self) -> str:
        return (f"Ticket({self.film}, seat={self.seat}, "
                f"price={self.price}, extras={sorted(self.extras)})")

    def clone(self) -> "Ticket":
        """Прототип: глубокая копия билета."""
        return copy.deepcopy(self)


class TicketBuilder:
    def __init__(self) -> None:
        self.film: str | None = None
        self.seat: str | None = None
        self.price: float = 0.0
        self.extras: set[str] = set()
        self.discount: float | None = None
        self.comment: str | None = None

    def for_film(self, film: str) -> "TicketBuilder":
        self.film = film
        return self

    def seat(self, seat: str) -> "TicketBuilder":
        self.seat = seat
        return self

    def price(self, p: float) -> "TicketBuilder":
        self.price = p
        return self

    def with_popcorn(self) -> "TicketBuilder":
        self.extras.add("popcorn")
        return self

    def with_drink(self) -> "TicketBuilder":
        self.extras.add("drink")
        return self

    def with_discount(self, d: float) -> "TicketBuilder":
        self.discount = d
        return self

    def with_comment(self, c: str) -> "TicketBuilder":
        self.comment = c
        return self

    def build(self) -> Ticket:
        if not self.film or not self.seat:
            raise ValueError("film и seat обязательны")
        return Ticket(self)


# =====================================================================
# 2. SINGLETON — потокобезопасная сессия пользователя
# =====================================================================

class UserSession:
    _instance: "UserSession | None" = None
    _lock = threading.Lock()

    def __new__(cls, user: str = "guest") -> "UserSession":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    obj = super().__new__(cls)
                    obj.user = user
                    cls._instance = obj
        return cls._instance

    def __init__(self, user: str = "guest") -> None:
        # идемпотентно
        pass


# =====================================================================
# 3. ABSTRACT FACTORY — семейства «билет + уведомление»
# =====================================================================

class Notifier(ABC):
    @abstractmethod
    def notify(self, msg: str) -> None: ...


class EmailNotifier(Notifier):
    def notify(self, msg: str) -> None:
        print(f"EMAIL: {msg}")


class SmsNotifier(Notifier):
    def notify(self, msg: str) -> None:
        print(f"SMS: {msg}")


class TicketFactory(ABC):
    @abstractmethod
    def create_ticket(self, film: str, seat: str) -> Ticket: ...

    @abstractmethod
    def create_notifier(self) -> Notifier: ...


class StandardTicketFactory(TicketFactory):
    def create_ticket(self, film: str, seat: str) -> Ticket:
        return (TicketBuilder()
                .for_film(film).seat(seat)
                .price(300.0)
                .build())

    def create_notifier(self) -> Notifier:
        return EmailNotifier()


class VipTicketFactory(TicketFactory):
    def create_ticket(self, film: str, seat: str) -> Ticket:
        return (TicketBuilder()
                .for_film(film).seat(seat)
                .price(1500.0)
                .with_popcorn().with_drink()
                .build())

    def create_notifier(self) -> Notifier:
        return SmsNotifier()


# =====================================================================
# 4. FACTORY METHOD — фабрика страниц фильма
# =====================================================================

class MoviePage:
    def __init__(self, title: str, poster: str,
                 desc: str, trailer: str, subs: str) -> None:
        self.title = title
        self.poster = poster
        self.desc = desc
        self.trailer = trailer
        self.subs = subs

    def __str__(self) -> str:
        return f"MoviePage({self.title}, poster={self.poster})"


class MoviePageFactory(ABC):
    @abstractmethod
    def create(self, title: str) -> MoviePage: ...


class LocalMoviePageFactory(MoviePageFactory):
    def create(self, title: str) -> MoviePage:
        return MoviePage(
            title,
            f"local/{title}.jpg",
            f"Описание {title}",
            f"local/{title}.mp4",
            f"local/{title}.srt",
        )


class CloudMoviePageFactory(MoviePageFactory):
    def create(self, title: str) -> MoviePage:
        return MoviePage(
            title,
            f"https://cdn/{title}.jpg",
            f"Cloud-описание {title}",
            f"https://cdn/{title}.mp4",
            f"https://cdn/{title}.srt",
        )


# =====================================================================
# 5. LAZY INITIALIZATION (Singleton) — дорогой ресурс
# =====================================================================

class VideoDecoder:
    _instance: "VideoDecoder | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "VideoDecoder":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("VideoDecoder: дорогая инициализация (один раз)")
                    cls._instance = super().__new__(cls)
        return cls._instance

    def decode(self, f: str) -> None:
        print(f"decode {f}")


# =====================================================================
# ДЕМОНСТРАЦИЯ
# =====================================================================

def main() -> None:
    print("=== ЛР №6: Порождающие паттерны ===\n")

    print("--- Builder ---")
    ticket = (TicketBuilder()
              .for_film("Dune").seat("A1")
              .price(300.0).with_drink()
              .build())
    print(ticket)

    print("\n--- Singleton ---")
    s1 = UserSession("alice")
    s2 = UserSession("bob")
    print("same instance:", s1 is s2, "| user:", s1.user)

    print("\n--- Abstract Factory ---")
    for factory in (StandardTicketFactory(), VipTicketFactory()):
        t = factory.create_ticket("Dune", "B5")
        n = factory.create_notifier()
        n.notify(f"Билет готов: {t}")

    print("\n--- Factory Method ---")
    for f in (LocalMoviePageFactory(), CloudMoviePageFactory()):
        page = f.create("Dune")
        print(page)

    print("\n--- Prototype ---")
    copy_ticket = ticket.clone()
    copy_ticket.seat = "A2"
    print("original:", ticket)
    print("clone   :", copy_ticket)
    print("independent:", ticket is not copy_ticket,
          "| extras independent:", ticket.extras is not copy_ticket.extras)

    print("\n--- Lazy Initialization (Singleton) ---")
    d1 = VideoDecoder()
    d2 = VideoDecoder()
    print("same decoder:", d1 is d2)
    d1.decode("trailer.mp4")
    d2.decode("episode1.mp4")


if __name__ == "__main__":
    main()