import os

from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_path = ("/admin/",)

    def __call__(self, request):
        api_key = request.headers.get("Key")
        expected_api_key = os.environ.get("API_KEY")

        if request.path.startswith(self.exclude_path):
            print(1)
            response = self.get_response(request)
            return response
        elif api_key != expected_api_key:
            return JsonResponse({"error": "Invalid API key"}, status=403)

        response = self.get_response(request)
        return response
