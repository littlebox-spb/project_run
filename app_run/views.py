from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Run
from .serializers import RunSerializer, UserSerializer


@api_view(["GET"])
def company_details(request):
    return Response(
        {
            "company_name": settings.COMPANY_NAME,
            "slogan": settings.SLOGAN,
            "contacts": settings.CONTACTS,
        }
    )


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get("type", None)
        if type:
            if type == "coach":
                qs = qs.filter(is_staff=True, is_superuser=False)
            else:
                qs = qs.filter(is_staff=False, is_superuser=False)
        else:
            qs = qs.filter(is_superuser=False)
        return qs
