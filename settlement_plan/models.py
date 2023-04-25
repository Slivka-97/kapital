import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, TextChoices


class InvestmentPortfolio(models.Model):

    class TypeCurrency(TextChoices):
        RUB = 'RUB', 'рубль'
        USD = 'USD', 'доллар'
        EUR = 'EUR', 'евро'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.DateField(default=datetime.date.today())
    currency = models.CharField('валюта', max_length=3, choices=TypeCurrency.choices)
    fact_price = models.IntegerField('Фактическая стоимость портфеля на начало года')
    plan_price = models.IntegerField('Планируемая стоимость портфеля на начало года')

    class Meta:
        verbose_name = 'Инвестиционный портфель'
        verbose_name_plural = 'Инвестиционные портфели'

    def __str__(self):
        return f'Портфель user: {self.user}'


class InvestmentPurpose(models.Model):
    class Type(TextChoices):
        INVESTMENT_SUM = 'investment_sum', 'Какую сумму необходимо инвестировать ежемесячно в течение'
        SUM_RENT = 'sum_rent', 'Какую сумму ежемесячной ренты'
        AGE_RENT = 'age_rent', 'В каком возрасте я смогу получить ренту'
        INVEST_YEAR = 'invest_year', 'С какой годовой доходностью я должен инвестировать'

    age = models.PositiveIntegerField('возраст')
    initial_sum = models.PositiveIntegerField('начальный капитал')
    type = models.CharField('Вариант инвестирования', max_length=254, choices=Type.choices)
    period_intensity_invest = models.IntegerField('период активного ежемесячного инвестирования', default=0)
    start_data_invest = models.DateField('дата начала инвестирования', blank=True, null=True)
    age_goal_achievement = models.PositiveIntegerField('планируемый возраст достижения цели', blank=True, null=True)
    year_achievement_goal = models.IntegerField('год достижения цели', blank=True, null=True)
    annual_return_investment = models.IntegerField('средняя годовая доходность инвестирования', blank=True, null=True)
    percent_rent_month = models.IntegerField('% ежемесячной ренты по достижению возраста', blank=True, null=True)
    sum_rent_month = models.IntegerField('размер ежемесячной ренты', blank=True, null=True)
    investment_portfolio = models.ForeignKey(InvestmentPortfolio, related_name='investment_purposes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Инвестиционная цель'
        verbose_name_plural = 'Инвестиционные цели'

    def __str__(self):
        return f'Инвестиционная цель {self.age} {self.initial_sum}'

    @staticmethod
    def get_year_achievement_goal(data: dict):
        current_year = datetime.datetime.now().year
        if data.get('age_goal_achievement', None):
            return current_year + (data.get('age_goal_achievement') - data.get('age', 0))
        return None


class Compare(models.Model):
    data = models.DateField()
    monthly_payment_plan = models.IntegerField('Ежемесячный взнос план', default=0, blank=True, null=True)
    monthly_payment_fact = models.IntegerField('Ежемесячный взнос Факт', default=0, blank=True, null=True)
    invested_funds_plan = models.IntegerField('Вложено средств с накопительным итогом план', default=0, blank=True, null=True)
    invested_funds_fact = models.IntegerField('Вложено средств с накопительным итогом Факт', default=0, blank=True, null=True)
    portfolio_value_end_month_plan = models.IntegerField('Стоимость портфеля на конец месяца план', default=0, blank=True, null=True)
    portfolio_value_end_month_fact = models.IntegerField('Стоимость портфеля на конец месяца Факт', default=0, blank=True, null=True)
    average_monthly_value_plan = models.IntegerField('Среднемесячная доходность план', default=0, blank=True, null=True)
    average_monthly_value_fact = models.IntegerField('Среднемесячная доходность Факт', default=0, blank=True, null=True)
    profit_month_plan = models.IntegerField('Прибыль за месяц план', default=0, blank=True, null=True)
    profit_month_fact = models.IntegerField('Прибыль за месяц Факт', default=0, blank=True, null=True)
    loss_month_plan = models.IntegerField('Убыток за месяц план', default=0, blank=True, null=True)
    loss_month_fact = models.IntegerField('Убыток за месяц Факт', default=0, blank=True, null=True)
    purpose = models.ForeignKey(InvestmentPurpose, on_delete=models.CASCADE, related_name='compares')

    class Meta:
        verbose_name = 'Сравнение план/факт'
        verbose_name_plural = 'Сравнение план/факт'

    def __str__(self):
        return f'Сравнение {self.data} {self.purpose}'

    @staticmethod
    def get_sum_invested_funds_fact(purpose):
        res = Compare.objects.filter(purpose=purpose.id).aggregate(Sum("monthly_payment_fact"))
        return res.get('monthly_payment_fact__sum', 0)


