from django.contrib import admin
from .models import Investment, Savings, UserInvestmentPlan

# Register your models here.
admin.site.register(Investment)
admin.site.register(Savings)
admin.site.register(UserInvestmentPlan)