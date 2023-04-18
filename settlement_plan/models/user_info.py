from django.contrib.auth.models import User
from django.db import models

from .investment import InvestmentPurpose, InvestmentPortfolio


class UserInfo(models.Model):

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(help_text='возраст')
    initial_sum = models.PositiveIntegerField(help_text='начальный капитал')
    investment_purpose = models.ForeignKey(
        InvestmentPurpose,
        related_name='investment_purpose_list',
        blank=False,
        null=False,
        on_delete=models.PROTECT
    )
    other_info = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        help_text='другая информация'
    )
    investment_portfolio = models.ForeignKey(
        InvestmentPortfolio,
        null=True,
        blank=True,
        related_name='investment_portfolio_list',
        on_delete=models.PROTECT,
    )
