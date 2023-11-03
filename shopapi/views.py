from django.conf import settings
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shopapi.models import *
from shopapi.serializers import *
from shopapi.tasks import send_qr_code_email_task


class DistributorViewSet(ModelViewSet):
    serializer_class = DistributorSerializer
    queryset = Distributor.objects.all()

    @action(detail=False, methods=["GET"])
    def above_average_debt(self, request):
        average_debt = Distributor.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        distributors_above_average = Distributor.objects.filter(debt__gt=average_debt)
        serializer = DistributorSerializer(distributors_above_average, many=True)
        return Response(
            {
                "average_debt": average_debt,
                "distributors_above_average": serializer.data,
            }
        )

    def list(self, request):
        print(settings.STATIC_URL + 'admin/js/copy_email.js')
        country = request.GET.get("country", None)
        product_id = request.GET.get("product_id", None)

        distributors = Distributor.objects.all()

        if country:
            distributors = distributors.filter(country=country)

        if product_id:
            distributors = distributors.filter(products__id=product_id)

        serializer = DistributorSerializer(distributors, many=True)
        return JsonResponse(serializer.data, safe=False)


class DealerViewSet(ModelViewSet):
    serializer_class = DealerSerializer
    queryset = Dealer.objects.all()

    @action(detail=False, methods=["GET"])
    def above_average_debt(self, request):
        average_debt = Dealer.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        dealers_above_average = Dealer.objects.filter(debt__gt=average_debt)
        serializer = DealerSerializer(dealers_above_average, many=True)
        return Response(
            {
                "average_debt": average_debt,
                "dealers_above_average": serializer.data,
            }
        )

    def list(self, request):
        country = request.GET.get("country", None)
        product_id = request.GET.get("product_id", None)
        dealers = Dealer.objects.all()
        if country is not None:
            dealers = Dealer.objects.filter(country=country)

        if product_id:
            dealers = dealers.filter(products__id=product_id)

        serializer = DealerSerializer(dealers, many=True)
        return JsonResponse(serializer.data, safe=False)


class FactoryViewSet(ModelViewSet):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()

    def list(self, request):
        country = request.GET.get("country", None)
        product_id = request.GET.get("product_id", None)
        factorys = Factory.objects.all()
        if country is not None:
            factorys = Factory.objects.filter(country=country)
        if product_id:
            factorys = factorys.filter(products__id=product_id)

        serializer = FactorySerializer(factorys, many=True)
        return JsonResponse(serializer.data, safe=False)


class RetailerViewSet(ModelViewSet):
    serializer_class = RetailerSerializer
    queryset = Retailer.objects.all()

    @action(detail=False, methods=["GET"])
    def above_average_debt(self, request):
        average_debt = Retailer.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        retailers_above_average = Retailer.objects.filter(debt__gt=average_debt)
        serializer = RetailerSerializer(retailers_above_average, many=True)
        return Response(
            {
                "average_debt": average_debt,
                "retailers_above_average": serializer.data,
            }
        )

    def list(self, request):
        country = request.GET.get("country", None)
        product_id = request.GET.get("product_id", None)
        retailers = Retailer.objects.all()

        if country is not None:
            retailers = Retailer.objects.filter(country=country)
        if product_id:
            retailers = retailers.filter(products__id=product_id)

        serializer = RetailerSerializer(retailers, many=True)
        return JsonResponse(serializer.data, safe=False)


class IndividualViewSet(ModelViewSet):
    serializer_class = IndividualSerializer
    queryset = Individual.objects.all()

    @action(detail=False, methods=["GET"])
    def above_average_debt(self, request):
        average_debt = Individual.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        individuals_above_average = Individual.objects.filter(debt__gt=average_debt)
        serializer = IndividualSerializer(individuals_above_average, many=True)
        return Response(
            {
                "average_debt": average_debt,
                "individuals_above_average": serializer.data,
            }
        )

    def list(self, request):
        country = request.GET.get("country", None)
        product_id = request.GET.get("product_id", None)
        individuals = Individual.objects.all()
        if country is not None:
            individuals = Individual.objects.filter(country=country)
        if product_id:
            individuals = individuals.filter(products__id=product_id)

        serializer = IndividualSerializer(individuals, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


def send_qr_code_view(request, distributor_id):
    try:
        distributor = Distributor.objects.get(pk=distributor_id)
    except Distributor.DoesNotExist:
        return HttpResponse("Distributor not found", status=404)

    send_qr_code_email_task.delay(distributor_id)

    return HttpResponse(f"QR code sent to {distributor.email}")
