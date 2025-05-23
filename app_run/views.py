from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view(['GET'])
def company_details(request): 
    company = setting.COMPANY_NAME
    slogan = setting.SLOGAN
    contacts = setting.CONTACTS
    return Response({'company': company, 'slogan': slogan, 'contacts': contacts})
