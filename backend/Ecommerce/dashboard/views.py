from django.shortcuts import render
from .services import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from monitoring.models import ActivityLogs
from monitoring.utils import create_log

# Create your views here.

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = DashboardService.get_data(request.user)
        create_log(
            user=self.request.user,
            action='view',
            model_name='Dashboard',
            description='Dashboard viewed successfully'
        )
        return Response(data)