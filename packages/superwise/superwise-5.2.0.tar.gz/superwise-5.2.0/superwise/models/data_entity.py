""" This module implement DataEntity model  """
import json

import pandas as pd

from superwise.models.base import BaseModel
from superwise.resources.superwise_enums import get_enum_value


class DataEntity(BaseModel):
    """ data entity model class """

    def __init__(
        self,
        id=None,
        dimension_start_ts=None,
        type=None,
        name=None,
        role=None,
        feature_importance=None,
        summary=None,
        secondary_type=None,
        data_type=None,
        **kwargs
    ):
        """
        constructor for DataEntity class

        :param id: id if dataentity
        :param dimension_start_ts
        :param type:
        :param name:
        :param is_dimension:
        :param role:
        :param feature_importance:
        :param summary:
        :param secondary_type:
        :data_type:

        """
        self.name = name.lower() if name else None
        self.type = get_enum_value(type)
        self.role = get_enum_value(role)
        self.feature_importance = feature_importance
        self.summary = summary
        self.secondary_type = secondary_type
        self.id = id
        self.dimension_start_ts = self.from_datetime(dimension_start_ts)
        self.data_type = data_type

    @staticmethod
    def list_to_df(data_entities):
        """
        get list of DataEntity objects and return them as pandas dataframe

        :return dataframe
        """
        data = [d.get_properties() for d in data_entities]
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def df_to_list(data_entities_df):
        """
        Get data entities dataframe and return list of DataEntity objects
        :param data_entities_df: a df of data entities

        :return list of DataEntity
        """
        data = json.loads(data_entities_df.to_json(orient="records"))
        entities = []
        [entities.append(DataEntity(**d)) for d in data]
        return entities


class DataEntitySummary(BaseModel):
    """ summary model class """

    def __init__(self, idx=None, summary=None):
        """
        constructer for DataEntitySummary class

        :param idx:
        :param summary:
        """
        self.id = idx
        self.summary = summary
