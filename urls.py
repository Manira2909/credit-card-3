from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Credit Card Django API is RUNNING da! ✅",
        "routes": ["/admin/", "/api/auth/register/", "/api/auth/login/", "/api/auth/dashboard/summary/"]
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('credit_django.cards.urls')),
]