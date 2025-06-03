"""
URL configuration for project_run project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from app_run import views
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api/runs", views.RunViewSet)
router.register("api/users", views.UserViewSet)
router.register("api/challenges", views.ChallengeViewSet)
router.register("api/positions", views.PositionViewSet)
router.register("api/collectible_item", views.CollectibleItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/company_details/", views.company_details),
    path("api/runs/<int:id>/start/", views.RunStart.as_view()),
    path("api/runs/<int:id>/stop/", views.RunStop.as_view()),
    path("api/athlete_info/<int:user_id>/", views.Athlete.as_view()),
    path("api/subscribe_to_coach/<int:coach_id>/", views.SubscribeViewSet.as_view()),
    path("api/upload_file/", views.upload_file),
    path("", include(router.urls)),
]
