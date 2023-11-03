from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Entity(models.Model):
    name_of_manufacture = models.CharField(max_length=50)
    created_at = models.DateField(auto_now=True)
    email = models.EmailField(max_length=254)
    country = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    street = models.CharField(max_length=25)
    number_of_house = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )

    def __str__(self):
        return self.name_of_manufacture


class Product(models.Model):
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    data_of_issue = models.DateField()
    selling_at = models.ForeignKey(
        "Entity", on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.data_of_issue >= timezone.now().date():
            raise ValidationError(
                "Дата выхода продукта на рынок должна быть меньше текущей даты."
            )


class Employee(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=25)
    working_at = models.ForeignKey(
        "Entity", on_delete=models.CASCADE, related_name="employees"
    )

    def __str__(self):
        return self.name


class Factory(Entity):
    pass


class Distributor(Entity):
    provider = models.ForeignKey(
        Factory, on_delete=models.CASCADE, related_name="distributor"
    )
    debt = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )


class Dealer(Entity):
    provider = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, related_name="dealer"
    )
    debt = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )


class Retailer(Entity):
    provider = models.ForeignKey(
        Dealer, on_delete=models.CASCADE, related_name="retailer"
    )
    debt = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )


class Individual(Entity):
    provider = models.ForeignKey(
        Retailer, on_delete=models.CASCADE, related_name="individual"
    )
    debt = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
