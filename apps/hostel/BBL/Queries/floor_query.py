from http import HTTPStatus
from apps.hostel.models import Floor, Room
from apps.hostel.serializers import FloorSerializer
from utils.base_result import BaseResultWithData
from utils.enums import RoomStatus


class FloorQuery:
    
    @staticmethod
    def GetAll():
        try:
            floors = Floor.objects.all()
            serializer = FloorSerializer(floors, many=True)
            
            # Add room counts to each floor
            data = serializer.data
            for floor_data in data:
                floor = Floor.objects.get(id=floor_data['id'])
                total_rooms = floor.rooms.all().count()
                occupied_rooms = floor.rooms.filter(
                    status=RoomStatus.OCCUPIED.value
                ).count()
                floor_data['total_rooms'] = total_rooms
                floor_data['occupied_rooms'] = occupied_rooms
            
            return BaseResultWithData(
                data=data,
                status_code=HTTPStatus.OK,
                message="Floors retrieved successfully"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
    
    @staticmethod
    def GetById(floor_id):
        try:
            floor = Floor.objects.get(id=floor_id)
            serializer = FloorSerializer(floor)
            
            # Add room counts
            data = serializer.data
            total_rooms = floor.rooms.all().count()
            occupied_rooms = floor.rooms.filter(
                status=RoomStatus.OCCUPIED.value
            ).count()
            data['total_rooms'] = total_rooms
            data['occupied_rooms'] = occupied_rooms
            
            return BaseResultWithData(
                data=data,
                status_code=HTTPStatus.OK,
                message="Floor retrieved successfully"
            )
        except Floor.DoesNotExist:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.NOT_FOUND,
                message="Floor not found"
            )
        except Exception as e:
            return BaseResultWithData(
                data=None,
                status_code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )
