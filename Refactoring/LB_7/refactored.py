from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List


# =====================================================================
# 1. REPLACE DATA VALUE WITH OBJECT — Деньги, Скидка, Длительность
# =====================================================================

@dataclass(frozen=True)
class Money:
    """Неизменяемый объект-значение: сумма + валюта."""
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Сумма не может быть отрицательной")

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"Валюты не совпадают: {self.currency} != {other.currency}")

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"


@dataclass(frozen=True)
class Discount:
    """Неизменяемый объект-значение: процент скидки 0..1."""
    rate: float

    def __post_init__(self):
        if not 0.0 <= self.rate <= 1.0:
            raise ValueError("Скидка должна быть в диапазоне 0..1")

    def apply(self, price: Money) -> Money:
        return price * (1.0 - self.rate)


@dataclass(frozen=True)
class Duration:
    """Неизменяемый объект-значение: длительность в минутах."""
    minutes: int

    def __post_init__(self):
        if self.minutes <= 0:
            raise ValueError("Длительность должна быть положительной")

    def __str__(self) -> str:
        return f"{self.minutes} мин"


# =====================================================================
# 2. ENCAPSULATE COLLECTION — Cinema скрывает внутренний список
# =====================================================================

class Cinema:
    def __init__(self, name: str):
        self.name = name
        self._sessions: List[Session] = []

    def add_session(self, session: "Session") -> None:
        self._sessions.append(session)

    def remove_session(self, session: "Session") -> None:
        self._sessions.remove(session)

    def sessions(self) -> tuple:
        """Возвращает неизменяемое представление коллекции."""
        return tuple(self._sessions)

    def session_count(self) -> int:
        return len(self._sessions)


# =====================================================================
# 3. REPLACE MAGIC NUMBER WITH SYMBOLIC CONSTANT — возврат средств
# =====================================================================

class RefundPolicy:
    FULL_REFUND_DAYS = 7          # за 7+ дней — 90% возврат
    PARTIAL_REFUND_DAYS = 3       # за 3+ дня — 50% возврат
    FULL_REFUND_RATE = 0.9
    PARTIAL_REFUND_RATE = 0.5
    MINIMAL_REFUND_RATE = 0.1

    @classmethod
    def calculate(cls, price: Money, days_before: int) -> Money:
        if days_before >= cls.FULL_REFUND_DAYS:
            return price * cls.FULL_REFUND_RATE
        elif days_before >= cls.PARTIAL_REFUND_DAYS:
            return price * cls.PARTIAL_REFUND_RATE
        return price * cls.MINIMAL_REFUND_RATE


# =====================================================================
# 4. PULL UP FIELD + PULL UP METHOD + FORM TEMPLATE METHOD
#    Иерархия билетов: общее — в базовом классе
# =====================================================================

class Ticket(ABC):
    """Базовый билет. Общие поля и шаблонный метод describe()."""

    def __init__(self, film: str, seat: str, price: Money):
        self.film = film
        self.seat = seat
        self.price = price
        self.loyalty_points: int = 0          # PULL UP FIELD

    def final_price(self) -> Money:
        return self.price

    def _type_label(self) -> str:
        """Шаг, который переопределяют подклассы."""
        return "TICKET"

    def describe(self) -> str:                # PULL UP METHOD + TEMPLATE METHOD
        return f"[{self._type_label()}] {self.film}, {self.seat}, {self.final_price()}"

    def __str__(self) -> str:
        return self.describe()


class StandardTicket(Ticket):
    def _type_label(self) -> str:
        return "STD"


class VipTicket(Ticket):
    def __init__(self, film, seat, price, lounge_access: bool = True):
        super().__init__(film, seat, price)
        self.lounge_access = lounge_access

    def _type_label(self) -> str:
        return "VIP"


# =====================================================================
# 5. REPLACE INHERITANCE WITH DELEGATION — StudentTicket
#    Студенческий билет не хочет наследовать всё поведение Ticket,
#    поэтому использует делегирование + фиксированную скидку.
# =====================================================================

class StudentTicket:
    """Билет со студенческой скидкой через делегирование базовому Ticket."""

    STUDENT_DISCOUNT = Discount(0.5)

    def __init__(self, film: str, seat: str, base_price: Money, student_id: str):
        self._base = StandardTicket(film, seat, base_price)  # делегат
        self.student_id = student_id

    @property
    def film(self) -> str:
        return self._base.film

    @property
    def seat(self) -> str:
        return self._base.seat

    def final_price(self) -> Money:
        return self.STUDENT_DISCOUNT.apply(self._base.price)

    def describe(self) -> str:
        return f"[STDNT:{self.student_id}] {self.film}, {self.seat}, {self.final_price()}"

    def __str__(self) -> str:
        return self.describe()


# =====================================================================
# 6. Session использует объекты-значения
# =====================================================================

class Session:
    def __init__(self, film: str, start: str, duration: Duration):
        self.film = film
        self.start = start
        self.duration = duration

    def __str__(self) -> str:
        return f"Session({self.film} @ {self.start}, {self.duration})"


# =====================================================================
# ДЕМОНСТРАЦИЯ
# =====================================================================

def main() -> None:
    print("=== ЛР №7: Организация данных + Обобщение ===\n")

    # Money / Discount / Duration
    price = Money(Decimal("500.00"))
    discounted = Discount(0.2).apply(price)
    print(f"Цена: {price}; со скидкой 20%: {discounted}")

    duration = Duration(120)
    print(f"Длительность: {duration}\n")

    # Encapsulate Collection
    cinema = Cinema("СевГУ-Кино")
    cinema.add_session(Session("Dune", "18:00", duration))
    cinema.add_session(Session("Dune", "21:00", Duration(90)))
    print(f"Сеансов: {cinema.session_count()}")
    print(f"Снимок коллекции: {cinema.sessions()}\n")

    # Magic Number → Constant
    refund = RefundPolicy.calculate(price, days_before=5)
    print(f"Возврат за 5 дней: {refund}")

    # Pull Up Field / Method
    std = StandardTicket("Dune", "A1", price)
    vip = VipTicket("Dune", "VIP-1", price)
    print(std)
    print(vip)
    print(f"loyalty_points (общее поле): {std.loyalty_points}, {vip.loyalty_points}\n")

    # Replace Inheritance with Delegation
    student = StudentTicket("Dune", "B10", price, student_id="ST-2024-001")
    print(student)


if __name__ == "__main__":
    main()