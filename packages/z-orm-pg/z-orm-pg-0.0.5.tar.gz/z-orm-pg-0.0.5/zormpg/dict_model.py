from __future__ import annotations
from typing import Any, Dict, Iterable
from zormpg.base import DataModel
import peewee as pee
import json
import logging
logger = logging.getLogger(__name__)


class DictValue:

    def __init__(self, default=None, typ: type = None, jsonify=False) -> None:
        """
        default: default value
        typ: result will be called by. eg: str, int, float
        jsonify: result will be jsonify. to save simple list, tuple, dict
        """
        self.default = default
        if typ == None:
            typ = type(default)
        self.typ = typ
        self.jsonify = jsonify
        self.key = None
        self.owner: DictModel = None

    def _get_row(self) -> DictModel:
        return self.owner.select().where(self.owner.__class__._model_key == self.key).get()

    def _get(self):
        v = self.default
        n = self._count()
        # if n > 0:0._model_value
        if v is None and n == 0:
            raise Exception(f"表{self.owner._table_name}的键{self.key}无初始值,必须先赋值")
        if n == 0:
            return self.default
        try:
            v = self._get_row()._model_value
            if self.jsonify:
                return json.loads(v)
            else:
                if self.typ != type(None):
                    return self.typ(v)
                else:
                    logger.warning(f'表{self.owner._table_name}的键{self.key}未指定类型.返回原始值')
                    return v
        except:
            logger.warning(f'表{self.owner._table_name}的键{self.key}的值{v}转化为{self.typ}失败.返回原始值')
            return v

    def _count(self):
        return self.owner.select().where(self.owner.__class__._model_key == self.key).count()

    def _set(self, value):
        if self._count() == 0:
            row = self.owner.__class__()
            row._model_key = self.key
        else:
            row = self._get_row()
        if self.jsonify:
            row._model_value = json.dumps(value)
        else:
            row._model_value = str(value)
        row.save()
        logger.debug(f'设置表 {self.owner._table_name} 的 {self.key} 为 {value}')


class DictModel(DataModel):

    _model_key = pee.CharField()
    _model_value = pee.TextField()

    def __init__(self, *args, **kwargs):
        self._stored_dict: Dict[str, DictValue] = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, DictValue):
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
