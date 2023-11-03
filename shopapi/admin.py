import json

from django.conf import settings
from django.contrib import admin

from shopapi.models import *
from shopapi.tasks import clear_debt_task


@admin.action(description="Clear the debt of selected object")
def clear_debt(self, request, queryset):
    if queryset.count() > 20:
        model_name = queryset.model.__name__
        queryset_pks = list(queryset.values_list("pk", flat=True))
        clear_debt_task.delay(model_name, queryset_pks)
    else:
        queryset.update(debt=0)


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ("name_of_manufacture", "provider")
    list_display_links = ("name_of_manufacture", "provider")
    list_filter = ("city",)
    actions = [clear_debt]
    js = (settings.STATIC_URL + 'admin/js/copy_email.js',)



@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("name_of_manufacture",)
    list_filter = ("city",)
    actions = [clear_debt]


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ("name_of_manufacture", "provider")
    list_display_links = ("name_of_manufacture", "provider")
    list_filter = ("city",)
    actions = [clear_debt]


@admin.register(Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ("name_of_manufacture", "provider")
    list_display_links = ("name_of_manufacture", "provider")
    list_filter = ("city",)
    actions = [clear_debt]


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name_of_manufacture", "provider")
    list_display_links = ("name_of_manufacture", "provider")
    list_filter = ("city",)
    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
