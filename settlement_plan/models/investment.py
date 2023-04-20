#from django.contrib.postgres.fields import ArrayField
from datetime import date

from django.db import models
from django.contrib.auth.models import User

TYPE = [
    ('investment_sum', 'Какую сумму необходимо инвестировать ежемесячно в течение'),
    ('sum_rent', 'Какую сумму ежемесячной ренты'),
    ('age_rent', 'В каком возрасте я смогу получить ренту'),
    ('invest_year', 'С какой годовой доходностью я должен инвестировать'),
]


TYPE_CURRENCY = [
    ('RUB', 'рубль'),
    ('USD', 'доллар'),
    ('EUR', 'евро'),
]


class InvestmentPortfolio(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    year = models.DateField(
        default=date.today()
    )
    currency = models.CharField(
        max_length=3,
        choices=TYPE_CURRENCY,
        null=False,
        blank=False,
        verbose_name='валюта'
    )
    fact_price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Фактическая стоимость портфеля на начало года'
    )
    plan_price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Планируемая стоимость портфеля на начало года'
    )


class InvestmentPurpose(models.Model):

    class Meta:
        verbose_name = 'Инвестиционная цель'
        verbose_name_plural = 'Инвестиционные цели'

    age = models.PositiveIntegerField(
        help_text='возраст'
    )
    initial_sum = models.PositiveIntegerField(
        help_text='начальный капитал'
    )
    type = models.CharField(
        max_length=254,
        choices=TYPE,
        null=False,
        blank=False,
        verbose_name='Вариант вопроса инвестиционных целей'
    )
    period_monthly_invest = models.IntegerField(
        default=0,
        verbose_name='период активного ежемесячного инвестирования'
    )
    start_data_invest = models.DateField(
        blank=True,
        null=True,
        verbose_name='дата начала инвестирования'
    )
    age_goal_achievement = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='планируемый возраст достижения цели'
    )
    year_achievement_goal = models.IntegerField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='год достижения цели'
    )
    average_sum = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='средняя годовая доходность инвестирования'
    )
    percent_rent_month = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='% ежемесячной ренты по достижению возраста'
    )
    sum_rent_month = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='размер ежемесячной ренты'
    )
    investment_portfolio = models.ForeignKey(
        InvestmentPortfolio,
        blank=False,
        null=False,
        related_name='investment_purposes',
        on_delete=models.CASCADE
    )


class Compare(models.Model):
    data = models.DateField()
    monthly_payment_plan = models.IntegerField(
        default=0,
        verbose_name='Ежемесячный взнос план'
    )
    monthly_payment_fact = models.IntegerField(
        default=0,
        verbose_name='Ежемесячный взнос Факт'
    )
    invested_funds_plan = models.IntegerField(
        default=0,
        verbose_name='Вложено средств с накопительным итогом план'
    )
    invested_funds_fact = models.IntegerField(
        default=0,
        verbose_name='Вложено средств с накопительным итогом Факт'
    )
    portfolio_value_end_month_plan = models.IntegerField(
        default=0,
        verbose_name='Стоимость портфеля на конец месяца план'
    )
    portfolio_value_end_month_fact = models.IntegerField(
        default=0,
        verbose_name='Стоимость портфеля на конец месяца Факт'
    )
    average_monthly_value_plan = models.IntegerField(
        default=0,
        verbose_name='Среднемесячная доходность план'
    )
    average_monthly_value_fact = models.IntegerField(
        default=0,
        verbose_name='Среднемесячная доходность Факт'
    )
    profit_month_plan = models.IntegerField(
        default=0,
        verbose_name='Прибыль за месяц план'
    )
    profit_month_fact = models.IntegerField(
        default=0,
        verbose_name='Прибыль за месяц Факт'
    )
    loss_month_plan = models.IntegerField(
        default=0,
        verbose_name='Убыток за месяц план'
    )
    loss_month_fact = models.IntegerField(
        default=0,
        verbose_name='Убыток за месяц Факт'
    )
    id_portfolio = models.ForeignKey(
        InvestmentPortfolio,
        on_delete=models.CASCADE,
        related_name='compare'
    )








