import datetime as dt
from typing import Optional


def set_date(date):
    """
    Функция для преобразования
    даты в констукте.
    """
    if not date:
        return dt.date.today()
    return dt.datetime.strptime(date, "%d.%m.%Y").date()


class Record():
    """Записи для калькулятора"""

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = set_date(date)


class Calculator():
    """Калькулятор с общими методами."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        """Добавляем запись в калькулятор."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Считаем сколько потратили
        ккал/ денег за сегодня."""
        today_stats = []
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                today_stats.append(record.amount)
        return sum(today_stats)

    def get_week_stats(self) -> float:
        """Считаем сколько потратили
        денег/ккал
        за последнюю неделю."""
        week_stats = []
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        for record in self.records:
            if week_start < record.date <= today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def get_remains(self) -> float:
        """Сколько можно еще потратить."""
        remains = self.limit - self.get_today_stats()
        return remains


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """Считаю могу ли еще что-нибудь съесть."""
        ccal_remained = self.get_remains()
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            message = (f'Сегодня можно съесть что-нибудь ещё, '
                       f'но с общей калорийностью не более '
                       f'{ccal_remained} кКал')
        else:
            message = 'Хватит есть!'
        return message


class CashCalculator(Calculator):
    """Калькулятор денег."""
    EURO_RATE: float = 88.22
    USD_RATE: float = 74.3
    RUB_RATE: float = 1.0

    def get_today_cash_remained(self, currency: str):
        """Сколько ещё могу потратить в разной валюте."""
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        cash_remained = self.get_remains()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Валюта {currency} не поддерживается'
        name, rate = currencies[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message
