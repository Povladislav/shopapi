from rest_framework import serializers

from shopapi.models import Dealer, Distributor, Employee, Factory, Individual, Product


class EmployeeInManufactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["name", "position"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductInManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "data_of_issue"]


class DealerSerializer(serializers.ModelSerializer):
    employees = EmployeeInManufactorSerializer(read_only=True, many=True)
    products = ProductInManufactureSerializer(many=True)
    provider = serializers.CharField(source="provider.name_of_manufacture")

    class Meta:
        model = Dealer
        fields = "__all__"

    debt = serializers.ReadOnlyField()


class DistributorSerializer(serializers.ModelSerializer):
    employees = EmployeeInManufactorSerializer(read_only=True, many=True)
    products = ProductInManufactureSerializer(many=True)
    provider = serializers.CharField(source="provider.name_of_manufacture")

    class Meta:
        model = Distributor
        fields = "__all__"

    debt = serializers.ReadOnlyField()


class RetailerSerializer(serializers.ModelSerializer):
    employees = EmployeeInManufactorSerializer(read_only=True, many=True)
    products = ProductInManufactureSerializer(many=True)
    provider = serializers.CharField(source="provider.name_of_manufacture")

    class Meta:
        model = Individual
        fields = "__all__"

    debt = serializers.ReadOnlyField()


class IndividualSerializer(serializers.ModelSerializer):
    employees = EmployeeInManufactorSerializer(read_only=True, many=True)
    products = ProductInManufactureSerializer(many=True)
    provider = serializers.CharField(source="provider.name_of_manufacture")

    class Meta:
        model = Individual
        fields = "__all__"

    debt = serializers.ReadOnlyField()


class FactorySerializer(serializers.ModelSerializer):
    employees = EmployeeInManufactorSerializer(read_only=True, many=True)
    products = ProductInManufactureSerializer(many=True)

    class Meta:
        model = Factory
        fields = "__all__"
