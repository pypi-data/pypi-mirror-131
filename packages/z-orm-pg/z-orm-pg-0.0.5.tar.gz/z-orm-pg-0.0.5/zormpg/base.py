from typing import Dict
import peewee as pee
from zormpg.connect import ZormPgConnect
from playhouse.migrate import PostgresqlMigrator, migrate

import logging
logger = logging.getLogger(__name__)

TYPE_MAP = {
    pee.CharField: "character varying",
    pee.IntegerField: "integer",
    pee.PrimaryKeyField: "integer",
    pee.BigIntegerField: "bigint",
    pee.TextField: "text",
    pee.DoubleField: "double precision",
    pee.ForeignKeyField: "integer"
}

DEFAULT_VALUE = {
    pee.CharField: "",
    pee.IntegerField: 0,
    pee.BigIntegerField: 0,
    pee.TextField: "",
    pee.DoubleField: 0
}

db = ZormPgConnect.db

class DataModel(pee.Model):

    _table_name:str = 'data_model'

    id = pee.PrimaryKeyField()

    class Meta:
        database = db
        def table_function(c): return c._table_name

    @classmethod
    def migrate(cls):
        if cls.table_exists():
            logger.info(f"已存在表: {cls.__name__}")
            cls.migrate_columns()
        else:
            logger.info(f"创建表:   {cls.__name__}")
            db.create_tables([cls])

    @classmethod
    def get_fields(cls):
        fields: Dict[str, pee.Field] = {}
        for key, value in cls.__dict__.items():
            field = getattr(value, "field", False)
            if isinstance(field, pee.Field):
                fields[key] = field
        return fields

    @classmethod
    def migrate_columns(cls):
        fields = cls.get_fields()
        table = cls._table_name
        sql = """ SELECT column_name, data_type
            FROM information_schema.COLUMNS
            WHERE table_name = '%s'; """ % table
        existed_cols = dict(db.execute_sql(sql).fetchall())
        col_to_field = {}
        for field in fields.values():
            if isinstance(field, pee.ForeignKeyField):
                if field.model != cls:
                    continue
            if field.default == None:
                field.default = DEFAULT_VALUE.get(type(field),None)
            col_to_field[field.column_name] = field
        need_drop = []
        need_add = []
        for col, field in col_to_field.items():
            if col in existed_cols:
                if TYPE_MAP[type(field)] == existed_cols[col]:
                    continue
                need_drop.append(col)
            need_add.append(col)

        for col in existed_cols:
            if col not in col_to_field:
                need_drop.append(col)

        migrator = PostgresqlMigrator(db)
        operations = []
        for name in need_drop:
            operations.append(migrator.drop_column(table, name))
        for name in need_add:
            operations.append(migrator.add_column(table, name, col_to_field[name]))
        migrate(*operations)
