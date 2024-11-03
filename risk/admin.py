from django.contrib import admin
from .models import Company, UserCompany, Prj, Category, Risk

# Register your models here.
admin.site.register(Company)
admin.site.register(UserCompany)
admin.site.register(Prj)
admin.site.register(Category)
admin.site.register(Risk)