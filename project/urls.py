"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from . import settings
from django.urls import path
from app.views import DashboardView,SignUpView,LoginView,ShareAppView,Logout,Products,ProductDetailView,ShareProduct,Buy


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", DashboardView.as_view(),name="dashboard"),
    path("sign-up", SignUpView.as_view(), name = "signup"),
    path('sign-in', LoginView.as_view(), name = "login"),
    path("share", ShareAppView.as_view(), name = "share"),
    path("logout", Logout, name = "logout"),
    path("products", Products.as_view(), name = "products"),
    path("product/<int:pk>", ProductDetailView.as_view(), name = "product-detail"),
    path("product/<str:pk>", ProductDetailView.as_view()),
    path("buy/<int:pk>", Buy.as_view(), name = "buy"),
    path("buy/<str:pk>",Buy.as_view(),name="buy"),
    path("share/<int:pk>",ShareProduct.as_view(),name="share")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
