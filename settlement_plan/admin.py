from django.contrib import admin

from .models import InvestmentPurpose, InvestmentPortfolio, Compare


admin.site.register(InvestmentPurpose)
admin.site.register(InvestmentPortfolio)
admin.site.register(Compare)


