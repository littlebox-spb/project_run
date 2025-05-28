import app_run
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Run, AthleteInfo, Challenge, Position
from .serializers import AthleteSerializer, RunSerializer, UserSerializer, ChallengeSerializer, PositionSerializer


@api_view(["GET"])
def company_details(request):
    return Response(
        {
            "company_name": settings.COMPANY_NAME,
            "slogan": settings.SLOGAN,
            "contacts": settings.CONTACTS,
        }
    )


class ConfigPagination(PageNumberPagination):
    page_size_query_param = "size"


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related("athlete").all()
    serializer_class = RunSerializer
    pagination_class = ConfigPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "athlete"]
    ordering_fields = ["created_at"]
    ordering = ["id"]


class RunStart(APIView):

    def post(self, request, id):
        run_ = get_object_or_404(Run, id=id)
        if run_.status == "init":
            run_.status = "in_progress"
            run_.save()
        else:
            return Response(
                {"detail": "Забег не может быть начат"}, status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Забег успешно начат"}, status=status.HTTP_200_OK)


class RunStop(APIView):

    def post(self, request, id):
        run_ = get_object_or_404(Run, id=id)
        if run_.status == "in_progress":
            run_.status = "finished"
            run_.save()
        else:
            return Response(
                {"detail": "Забег не может быть завершен"}, status.HTTP_400_BAD_REQUEST
            )
        athlete=run_.athlete
        if Run.objects.filter(status="finished", athlete=athlete).count() == 10:
            challenge = Challenge.objects.create(full_name="Сделай 10 Забегов!",athlete=athlete)
            challenge.save()
        return Response({"detail": "Забег успешно завершен"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ConfigPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["last_name", "first_name"]
    ordering_fields = ["date_joined"]
    ordering = ["id"]

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


class Athlete(APIView):

    def get(self, request, user_id):
        user_ = get_object_or_404(User, id=user_id)
        athlete, created = AthleteInfo.objects.get_or_create(user_id=user_)
        serializer = AthleteSerializer(athlete)
        return Response(serializer.data)

    def put(self, request, user_id):
        user_ = get_object_or_404(User, id=user_id)
        weight=request.data.get('weight')
        if weight.isdigit():
            weight=int(weight)
        else:
            return Response(
                {"detail": "Вес должен быть числом"}, status.HTTP_400_BAD_REQUEST)
        if 0<weight<900:
            athlete, created = AthleteInfo.objects.update_or_create(
                user_id=user_,
                defaults={
                    'weight': weight,
                    'goals': request.data.get('goals'),
                }
            )
        else:
            return Response(
                {"detail": "Вес введен неправильно"}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Операция завершилась успешно"}, status=status.HTTP_201_CREATED)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        qs = self.queryset
        athlete = self.request.query_params.get("athlete", None)
        if athlete:
            user_ = get_object_or_404(User, id=athlete)
            qs = qs.filter(athlete=user_)
        return qs


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_queryset(self):
        qs = self.queryset
        run_id = self.request.query_params.get("run", None)
        if run_id:
            try:
                run_ = Run.objects.get(id=run_id)
            except Run.DoesNotExist:
                return []
            qs = qs.filter(run=run_)
        return qs

    def create(self, request, pk=None):
        data = request.data
        run_id = data.get("run", None)
        try:
            run = Run.objects.get(id=run_id)
        except Run.DoesNotExist:
            return Response(
                {"detail": "Забег не найден"}, status.HTTP_400_BAD_REQUEST)
        if run.status != "in_progress":
            return Response(
                {"detail": "Забег должен быть в статусе 'in_progress'"}, status.HTTP_400_BAD_REQUEST
            )        
        serializer = PositionSerializer(run,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()  
            super().create(request, pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        position = Position.objects.filter(id=pk)
        if position:
            super().destroy(request, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
