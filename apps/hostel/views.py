from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from apps.hostel.BBL.Commands.hotel_command import HotelCommand
from apps.hostel.BBL.Queries.dashboard_query import DashboardQuery
from apps.hostel.serializers import *
import logging

logger = logging.getLogger(__name__)


# Hotel Endpoints
class HotelCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelCreateSerializer
    
    def post(self, request, *args, **kwargs):
        result = HotelCommand.Create(data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)
            


class HotelUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelUpdateSerializer
    
    def put(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update(hotel_id=hotel_id, data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)
    
    def patch(self, request, hotel_id, *args, **kwargs):
        result = HotelCommand.Update(hotel_id=hotel_id, data=request.data, user=request.user)
        return Response(result.to_dict(), status=result.status_code)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        result = DashboardQuery.GetDashboardMetrics()
        return Response(result.to_dict(), status=result.status_code)

