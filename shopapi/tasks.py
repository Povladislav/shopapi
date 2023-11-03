import random

from celery import shared_task
from django.apps import apps

from shopapi.models import *
from shopapi.utils import generate_qr_code, send_qr_code_email


@shared_task
def increase_debt():
    distributors = Distributor.objects.all()
    for distributor in distributors:
        distributor.debt += random.randint(5, 500)
        distributor.save()


@shared_task
def decrease_debt():
    distributors = Distributor.objects.all()
    for distributor in distributors:
        distributor.debt -= random.randint(100, 10000)
        distributor.save()


@shared_task
def send_qr_code_email_task(distributor_id):
    try:
        distributor = Distributor.objects.get(pk=distributor_id)
        send_qr_code_email(distributor)
    except Distributor.DoesNotExist:
        print("Distributor not found")


@shared_task
def clear_debt_task(model_name, queryset_pks):
    model = apps.get_model(app_label="admin", model_name=model_name)
    queryset = model.objects.filter(pk__in=queryset_pks)
    queryset.update(debt=0)
