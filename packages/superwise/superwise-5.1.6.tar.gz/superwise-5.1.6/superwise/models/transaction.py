""" This module implement Transaction model  """
from typing import List
from typing import Optional

from superwise.models.base import BaseModel


class Transaction(BaseModel):
    """Transaction model"""

    def __init__(
        self,
        id: Optional[int] = None,
        task_id: Optional[int] = None,
        task_name: Optional[str] = None,
        version_id: Optional[str] = None,
        origin_url: Optional[str] = None,
        transaction_id: str = None,
        integration_type: Optional[str] = None,
        file_type: Optional[str] = None,
        status: Optional[str] = None,
        created_at: int = None,
        details: Optional[str] = None,
        num_of_records: Optional[str] = None,
        is_reviewed: bool = None,
    ):
        """
        :param task_id:
        :param task_name:
        :param version_id:
        :param origin_url:
        :param transaction_id:
        :param integration_type:
        :param file_type:
        :param status:
        :param created_at:
        :param details:
        :param num_of_records:
        :param is_reviewed:
        """
        self.id = id
        self.task_id = task_id
        self.task_name = task_name
        self.version_id = version_id
        self.origin_url = origin_url
        self.transaction_id = transaction_id
        self.integration_type = integration_type
        self.file_type = file_type
        self.status = status
        self.created_at = created_at
        self.details = details
        self.num_of_records = num_of_records
        self.is_reviewed = is_reviewed
