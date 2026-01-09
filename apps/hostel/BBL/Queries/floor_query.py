from apps.hostel.models import Floor
from utils.base_result import BaseResultWithData


class FloorQuery:
    
    @staticmethod
    def GetAll():
        try:
            floors = Floor.objects.filter(is_deleted=False)
            return BaseResultWithData(True, "Floors retrieved successfully", list(floors), 200)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
    
    @staticmethod
    def GetById(floor_id):
        try:
            floor = Floor.objects.get(id=floor_id, is_deleted=False)
            return BaseResultWithData(True, "Floor retrieved successfully", floor, 200)
        except Floor.DoesNotExist:
            return BaseResultWithData(False, "Floor not found", None, 404)
        except Exception as e:
            return BaseResultWithData(False, str(e), None, 400)
