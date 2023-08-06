""" This module contain BaseModel class  """
import datetime
from enum import Enum

import pandas as pd


class BaseModel:
    """ Base model """

    def __init__(self, **kwargs):
        self.id = kwargs("id", None)

    def from_datetime(self, date):
        """
        convert datetime helper

        :param: date - a datetime.datetime object
        """
        if pd.isna(date):
            return None
        elif isinstance(date, datetime.datetime):
            return date.isoformat()
        else:
            return date

    def get_properties(self):

        """
        get properties of model as a dictionary

        :return: properties dict
        """
        return dict(
            (name, getattr(self, name))
            for name in dir(self)
            if not name.startswith("__") and not callable(getattr(self, name))
        )
