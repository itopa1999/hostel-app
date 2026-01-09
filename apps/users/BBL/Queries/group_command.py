from http import HTTPStatus
from django.contrib.auth.models import Group
from utils.base_result import BaseResultWithData
import logging

logger = logging.getLogger(__name__)


class GroupQuery:
    """Handle read operations for Group"""
    
    @staticmethod
    def ListAll():
        """
        Retrieve all groups with ID and name.
        
        Returns:
            BaseResultWithData: Result with list of all groups
        """
        groups = Group.objects.all().values('id', 'name').order_by('name')
        
        result_data = {
            'groups': list(groups)
        }
        
        return BaseResultWithData(
            message="Groups retrieved successfully",
            data=result_data,
            status_code=HTTPStatus.OK
        )
