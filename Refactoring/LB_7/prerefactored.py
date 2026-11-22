from datetime import date


class Cinema:
    def __init__(self, name: str):
        self.name = name
        self._sessions = []         

    def get_sessions(self):
        return self._sessions        

    def add_session(self, session):
        self._sessions.append(session)


class Session:
    def __init__(self, film: str, start: str, duration_min: int):
        self.film = film
        self.start = start
        self.duration_min = duration_min   


class Ticket:
    def __init__(self, film: str, seat: str, price: float):
        self.film = film
        self.seat = seat
        self.price = price                  
        self.discount = 0.0                 

    def final_price(self):
        return self.price * (1 - self.discount)

    def describe(self):
        return f"{self.film}, {self.seat}, {self.final_price()}"


class StandardTicket(Ticket):
    def __init__(self, film, seat, price):
        super().__init__(film, seat, price)
        self.loyalty_points = 0            

    def describe(self):
        return f"[STD] {super().describe()}"


class VipTicket(Ticket):
    def __init__(self, film, seat, price):
        super().__init__(film, seat, price)
        self.loyalty_points = 0        
        self.lounge_access = True          

    def describe(self):
        return f"[VIP] {super().describe()}"


class StudentTicket(Ticket):
    def __init__(self, film, seat, price):
        super().__init__(film, seat, price)
        self.loyalty_points = 0           
        self.student_id = ""               

    def describe(self):
        return f"[STDNT] {super().describe()}"


def calculate_refund(price: float, days_before: int) -> float:
    if days_before >= 7:
        return price * 0.9
    elif days_before >= 3:
        return price * 0.5
    return price * 0.1