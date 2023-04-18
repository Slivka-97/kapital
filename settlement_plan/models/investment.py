#from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User

TYPE = [
    ('investment_sum', 'Какую сумму необходимо инвестировать ежемесячно в течение'),
    ('sum_rent', 'Какую сумму ежемесячной ренты'),
    ('age_rent', 'В каком возрасте я смогу получить ренту'),
    ('invest_year', 'С какой годовой доходностью я должен инвестировать'),
]


class InvestmentPortfolio(models.Model):

    class Meta:
        verbose_name = 'Инвестиционный портфель'
        verbose_name_plural = 'Инвестиционные портфели'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_portfolio'
    )
    is_removed = models.BooleanField(
        verbose_name='Удалено',
        default=False,
        db_index=True,
    )
    name = models.CharField(max_length=50)
    active_sum = models.IntegerField(blank=False, default=0)
    # stocks = ArrayField(
    #     models.CharField(max_length=50, blank=True),
    # )
    stocks = models.CharField(max_length=50, blank=True),


class InvestmentPurpose(models.Model):

    class Meta:
        verbose_name = 'Инвестиционная цель'
        verbose_name_plural = 'Инвестиционные цели'

    type = models.CharField(
        max_length=254,
        choices=TYPE,
        null=False,
        blank=False,
        verbose_name='Вариант вопроса инвестиционных целей'
    )
    is_removed = models.BooleanField(
        verbose_name='Удалено',
        default=False,
        db_index=True,
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












