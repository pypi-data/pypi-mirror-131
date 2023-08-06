
from typing import Any, Dict
from zormpg.base import DataModel
import peewee as pee

import logging
logger = logging.getLogger(__name__)

class DictValue:

    def __init__(self, default='' ,type:type=str) -> None:
        """
        default: default value
        type: result will be called by. eg: str,int,float
        """
        self.default = default
        self.type = type
        self.key = None
        self.owner:DictModel = None
    
    def _get_row(self):
        return self.owner.select().where(self.owner.__class__._model_key==self.key).get()

    def _get(self):
        if self._count() == 0:
            return self.type(self.default)
        return self.type(self._get_row()._model_value)

    def _count(self):
        return self.owner.select().where(self.owner.__class__._model_key==self.key).count()

    def _set(self,value):
        if self._count() == 0:
            row = self.owner.__class__()
            row._model_key = self.key
        else:
            row = self._get_row()
        row._model_value = str(value)
        row.save()
        logger.debug(f'设置表 {self.owner._table_name} 的 {self.key} 为 {value}')
        
class DictModel(DataModel):
 
    _model_key = pee.CharField()
    _model_value = pee.CharField()

    def __init__(self, *args, **kwargs):
        self._stored_dict:Dict[str,DictValue] = {}
        for k,v in self.__class__.__dict__.items():
            if isinstance(v,DictValue):
                v.key = k
                v.owner = self
                self._stored_dict[k] = v
        super().__init__(*args, **kwargs)

    def __getattribute__(self, _name: str) -> Any:
        if _name == '_stored_dict':
            return super().__getattribute__(_name)
        if _name in self._stored_dict:
            return self._stored_dict[_name]._get()
        return super().__getattribute__(_name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_stored_dict':
            return super().__setattr__(__name, __value)
        if __name in self._stored_dict:
            return self._stored_dict[__name]._set(__value)
        else:
            return super().__setattr__(__name, __value)
    



    

