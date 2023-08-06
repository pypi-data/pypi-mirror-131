import logging
from typing import List
import json
import cx_Oracle
from sqlalchemy import create_engine, CLOB
from sqlalchemy.pool import NullPool

from watchmen.boot.config.config import settings
from watchmen.boot.storage.model.data_source import DataSourceParam

SID = "SID"
SERVICE_NAME = "SERVICE_NAME"
log = logging.getLogger("app." + __name__)


class OracleEngine(object):
    cx_Oracle.init_oracle_client(lib_dir=settings.ORACLE_LIB_DIR)

    def find_sid(self, params: List[DataSourceParam]):
        for param in params:
            if param.name == SID:
                return param.value

    def find_service_name(self, params: List[DataSourceParam]):
        for param in params:
            if param.name == SERVICE_NAME.lower():
                return param.value

    def __init__(self, database: DataSource):
        sid = self.find_sid(database.params)
        if sid:
            dsn = cx_Oracle.makedsn(database.host,
                                    database.port, sid=sid)

        service_name = self.find_service_name(database.params)
        if sid is None and service_name is not None:
            dsn = cx_Oracle.makedsn(database.host,
                                    database.port, service_name=service_name)

        pool = cx_Oracle.SessionPool(
            database.username, database.password, dsn=dsn,
            min=3, max=3, increment=0, getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT
        )

        self.engine = create_engine("oracle+cx_oracle://", creator=pool.acquire,
                                    poolclass=NullPool, coerce_to_decimal=False, echo=False, optimize_limits=True,
                                    future=True)

    def get_engine(self):
        return self.engine

    def parse_obj(self, base_model, result, table):
        model = base_model()
        for attr, value in model.__dict__.items():
            if attr[:1] != '_':
                if isinstance(table.c[attr.lower()].type, CLOB):
                    if attr == "on":
                        if result[attr] is not None:
                            setattr(model, attr, json.loads(result[attr]))
                        else:
                            setattr(model, attr, None)
                    else:
                        if result[attr.upper()] is not None:
                            setattr(model, attr, json.loads(result[attr.upper()]))
                        else:
                            setattr(model, attr, None)
                else:
                    setattr(model, attr, result[attr.upper()])
        return base_model.parse_obj(model)