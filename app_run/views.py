from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer


@api_view(['GET'])
def company_details(request): 
    return Response({'company_name': settings.COMPANY_NAME, 'slogan': settings.SLOGAN, 'contacts': settings.CONTACTS})

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer