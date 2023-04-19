from django.contrib import admin

from .models import InvestmentPurpose, InvestmentPortfolio


@admin.register(InvestmentPurpose, InvestmentPortfolio,)
class AuthorAdmin(admin.ModelAdmin):
    pass


