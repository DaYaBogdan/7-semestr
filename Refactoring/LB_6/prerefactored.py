class Ticket:
    def __init__(self, film, seat, price,
                 with_popcorn=False,
                 with_drink=False,
                 is_vip=False,
                 discount=None,
                 comment=None):
        self.film = film
        self.seat = seat
        self.price = price
        self.with_popcorn = with_popcorn
        self.with_drink = with_drink
        self.is_vip = is_vip
        self.discount = discount
        self.comment = comment

    def __str__(self):
        return f"Ticket({self.film}, {self.seat}, {self.price})"


class UserSession:
    _instance = None
    def __init__(self, user): self.user = user
    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = UserSession("guest")
        return cls._instance


class StandardTicketNotifier:
    def notify(self): print("std ticket + email")


class VipTicketNotifier:
    def notify(self): print("vip ticket + sms")


class MoviePage:
    def __init__(self):
        self.poster = None
        self.description = None
        self.trailer = None
        self.subtitles = None


def build_movie_page(title):
    page = MoviePage()
    page.poster = f"{title}.jpg"
    page.description = f"Описание {title}"
    page.trailer = f"{title}.mp4"
    page.subtitles = f"{title}.srt"
    return page


class VideoDecoder:
    def __init__(self):
        print("VideoDecoder: дорогая инициализация")