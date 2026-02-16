from http import HTTPStatus
from django.contrib.auth.models import Group
from utils.base_result import BaseResultWithData
from utils.cache_helper import GlobalCache
from utils.enums import CacheKeys
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
        # Try cache first
        cached_data = GlobalCache.get(CacheKeys.GROUP_ALL.value)
        if cached_data:
            return BaseResultWithData(
                message="Groups retrieved successfully (cached)",
                data=cached_data,
                status_code=HTTPStatus.OK
            )
        
        groups = Group.objects.all().values('id', 'name').order_by('name')
        
        result_data = {
            'groups': list(groups)
        }
        
        # Cache the result
        GlobalCache.set(CacheKeys.GROUP_ALL.value, result_data)
        
        return BaseResultWithData(
            message="Groups retrieved successfully",
            data=result_data,
            status_code=HTTPStatus.OK
        )
