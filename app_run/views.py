from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
from .models import Run
from .serializers import RunSerializer, UserSerializer
from django.shortcuts import get_object_or_404


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

class RunStart(APIView):

    def post(self, request, id):
        run_ = get_object_or_404(Run, id=id)
        if run_.status == 'init':
            run_.status = 'in_progress'
            run_.save()
        else:
            return Response({"detail":"Забег не может быть начат"}, status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class RunStop(APIView):

    def post(self, request, id):
        run_ = get_object_or_404(Run, id=id)
        if run_.status == 'in_progress':
            run_.status = 'finished'
            run_.save()
        else:
            return Response({"detail":"Забег не может быть завершен"}, status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['last_name', 'first_name']    

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
