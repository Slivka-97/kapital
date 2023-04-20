from django.contrib import admin

from .models import InvestmentPurpose, InvestmentPortfolio, Compare


@admin.register(InvestmentPurpose, InvestmentPortfolio, Compare)
class AuthorAdmin(admin.ModelAdmin):
    pass


