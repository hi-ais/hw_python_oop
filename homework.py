import datetime as dt
from typing import Optional
FORMAT_DATE = "%d.%m.%Y"


def set_date(date: dt.date):
    """
    Функция для преобразования
    даты в конструкте.
    """
    if not date:
        return dt.date.today()
    return dt.datetime.strptime(date, FORMAT_DATE).date()


class Record():
    """Записи для калькулятора."""

    amount: float
    comment: str
    date: Optional[str]
    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = set_date(date)


class Calculator():
    """Калькулятор с общими методами."""
    limit = float
    record: Record

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        """Добавление записи в калькулятор."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Сколько потрачено
        сегодня."""
        today = dt.date.today()
        return sum([x.amount for x in self.records
                   if x.date == today])

    def get_week_stats(self) -> float:
        """Сколько потрачено
        в течение недели."""
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        return sum([x.amount for x in self.records
                   if week_start < x.date <= today])

    def get_remains(self) -> float:
        """Сколько можно еще потратить сегодня."""
        remains = self.limit - self.get_today_stats()
        return remains


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """Могу ли поесть еще и сколько."""
        ccal_remained = self.get_remains()
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{ccal_remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег."""
    EURO_RATE: float = 88.22
    USD_RATE: float = 74.3
    RUB_RATE: float = 1.0
    currency: str

    def settings(self):
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        return currencies

    def get_today_cash_remained(self, currency: str):
        """Сколько ещё могу потратить в разной валюте."""
        cash_remained = self.get_remains()
        dict_currency = self.settings()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in dict_currency:
            return f'Валюта {currency} не поддерживается'
        name, rate = dict_currency[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained}'
                       f'{name}')
        return message
