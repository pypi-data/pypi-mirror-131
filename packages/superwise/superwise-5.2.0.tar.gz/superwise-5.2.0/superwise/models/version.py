""" This module implement version  model  """
import pandas as pd

from superwise.models.base import BaseModel


class Version(BaseModel):
    """ Version model class, model  for version data """

    def __init__(
        self,
        id=None,
        task_id=None,
        name=None,
        created_at=None,
        data_entities=None,
        baseline_df=None,
        status=None,
        **kwargs
    ):
        """
        constructor for Version class
        :param id:
        :param task_id:
        :param name:
        :param client_name:
        :param external_id:
        :param created_at:
        :param data_entities:
        """
        self.id = id
        self.task_id = task_id
        self.name = name
        self.baseline_files = []
        self.created_at = created_at
        self.data_entities = data_entities or []
        self.status = status
        self.baseline_df = baseline_df
