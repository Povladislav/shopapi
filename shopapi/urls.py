from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from shopapi.views import *

router_distributor = routers.SimpleRouter()
router_factory = routers.SimpleRouter()
router_individual = routers.SimpleRouter()
router_dealer = routers.SimpleRouter()
router_product = routers.SimpleRouter()
router_retailer = routers.SimpleRouter()

router_distributor.register(r"distributors", DistributorViewSet)
router_factory.register(r"factorys", FactoryViewSet)
router_individual.register(r"individuals", IndividualViewSet)
router_dealer.register(r"dealers", DealerViewSet)
router_product.register(r"products", ProductViewSet)
router_retailer.register(r"retailers", RetailerViewSet)

urlpatterns = [
    path("api/v1/", include(router_factory.urls)),
    path("api/v1/", include(router_distributor.urls)),
    path("api/v1/", include(router_individual.urls)),
    path("api/v1/", include(router_dealer.urls)),
    path("api/v1/", include(router_product.urls)),
    path("api/v1/", include(router_retailer.urls)),
    path(
        "api/distributors/above_average_debt/",
        DistributorViewSet.as_view({"get": "above_average_debt"}),
        name="distributors-above-average-debt",
    ),
    path(
        "api/dealers/above_average_debt/",
        DealerViewSet.as_view({"get": "above_average_debt"}),
        name="dealers-above-average-debt",
    ),
    path(
        "api/retailers/above_average_debt/",
        RetailerViewSet.as_view({"get": "above_average_debt"}),
        name="retailers-above-average-debt",
    ),
    path(
        "api/individuals/above_average_debt/",
        IndividualViewSet.as_view({"get": "above_average_debt"}),
        name="individuals-above-average-debt",
    ),
    path("send_qr_code/<int:distributor_id>/", send_qr_code_view, name="send_qr_code"),
]
