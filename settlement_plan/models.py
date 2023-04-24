import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.DateField(default=datetime.date.today())
    currency = models.CharField(max_length=3, choices=TYPE_CURRENCY, null=False, blank=False, verbose_name='валюта')
    fact_price = models.IntegerField(null=False, blank=False, verbose_name='Фактическая стоимость портфеля на начало года')
    plan_price = models.IntegerField(null=False, blank=False, verbose_name='Планируемая стоимость портфеля на начало года')

    class Meta:
        verbose_name = 'Инвестиционный портфель'
        verbose_name_plural = 'Инвестиционные портфели'

    def __str__(self):
        return f'Портфель user: {self.user}'


class InvestmentPurpose(models.Model):

    age = models.PositiveIntegerField(help_text='возраст')
    initial_sum = models.PositiveIntegerField(help_text='начальный капитал')
    type = models.CharField(max_length=254, choices=TYPE, verbose_name='Вариант инвестирования')
    period_intensity_invest = models.IntegerField(default=0, verbose_name='период активного ежемесячного инвестирования')
    start_data_invest = models.DateField(blank=True, null=True, verbose_name='дата начала инвестирования')
    age_goal_achievement = models.PositiveIntegerField(blank=True, null=True, verbose_name='планируемый возраст достижения цели')
    year_achievement_goal = models.IntegerField(blank=True, null=True, verbose_name='год достижения цели')
    annual_return_investment = models.IntegerField(blank=True, null=True, verbose_name='средняя годовая доходность инвестирования')
    percent_rent_month = models.IntegerField(blank=True, null=True, verbose_name='% ежемесячной ренты по достижению возраста')
    sum_rent_month = models.IntegerField(blank=True, null=True, verbose_name='размер ежемесячной ренты')
    investment_portfolio = models.ForeignKey(InvestmentPortfolio, related_name='investment_purposes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Инвестиционная цель'
        verbose_name_plural = 'Инвестиционные цели'

    def __str__(self):
        return f'Инвестиционная цель {self.age} {self.initial_sum}'

    @staticmethod
    def get_year_achievement_goal(data: dict):
        current_year = datetime.datetime.now().year
        res = None
        if data['age_goal_achievement']:
            res = current_year + (data['age_goal_achievement'] - data['age'])
        return res


class Compare(models.Model):
    data = models.DateField()
    monthly_payment_plan = models.IntegerField(default=0, verbose_name='Ежемесячный взнос план', blank=True, null=True,)
    monthly_payment_fact = models.IntegerField(default=0, verbose_name='Ежемесячный взнос Факт', blank=True, null=True,)
    invested_funds_plan = models.IntegerField(default=0, verbose_name='Вложено средств с накопительным итогом план', blank=True, null=True,)
    invested_funds_fact = models.IntegerField(default=0, verbose_name='Вложено средств с накопительным итогом Факт', blank=True, null=True,)
    portfolio_value_end_month_plan = models.IntegerField(default=0, verbose_name='Стоимость портфеля на конец месяца план', blank=True, null=True,)
    portfolio_value_end_month_fact = models.IntegerField(default=0, verbose_name='Стоимость портфеля на конец месяца Факт', blank=True, null=True,)
    average_monthly_value_plan = models.IntegerField(default=0, verbose_name='Среднемесячная доходность план', blank=True, null=True,)
    average_monthly_value_fact = models.IntegerField(default=0, verbose_name='Среднемесячная доходность Факт', blank=True, null=True,)
    profit_month_plan = models.IntegerField(default=0, verbose_name='Прибыль за месяц план', blank=True, null=True,)
    profit_month_fact = models.IntegerField(default=0, verbose_name='Прибыль за месяц Факт', blank=True, null=True,)
    loss_month_plan = models.IntegerField(default=0, verbose_name='Убыток за месяц план', blank=True, null=True,)
    loss_month_fact = models.IntegerField(default=0, verbose_name='Убыток за месяц Факт', blank=True, null=True,)
    purpose = models.ForeignKey(InvestmentPurpose, on_delete=models.CASCADE, related_name='compares')

    class Meta:
        verbose_name = 'Сравнение план/факт'
        verbose_name_plural = 'Сравнение план/факт'

    def __str__(self):
        return f'Сравнение {self.data} {self.purpose}'

    @staticmethod
    def get_sum_invested_funds_fact(purpose):
        res = Compare.objects.filter(purpose=purpose.id).aggregate(Sum("monthly_payment_fact"))
        return res['monthly_payment_fact__sum']


