from sqlalchemy import create_engine, JSON
import json

from watchmen.boot.storage.model.data_source import DataSource
from watchmen.boot.storage.utility.date_utils import dumps


class MysqlEngine(object):

    def __init__(self, datasource: DataSource):
        self.connection_url = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (datasource.username,
                                                                       datasource.password,
                                                                       datasource.host,
                                                                       datasource.port,
                                                                       datasource.name)
        self.engine = create_engine(self.connection_url,
                                    echo=False,
                                    future=True,
                                    pool_recycle=3600,
                                    json_serializer=dumps, encoding='utf-8')

    def get_engine(self):
        return self.engine

    def parse_obj(self, base_model, result, table):
        model = base_model()
        for attr, value in model.__dict__.items():
            if attr[:1] != '_':
                if isinstance(table.c[attr.lower()].type, JSON):
                    if attr == "on":
                        if result[attr] is not None:
                            setattr(model, attr, json.loads(result[attr.lower()]))
                        else:
                            setattr(model, attr, None)
                    else:
                        if result[attr.lower()] is not None:
                            setattr(model, attr, json.loads(result[attr.lower()]))
                        else:
                            setattr(model, attr, None)
                else:
                    setattr(model, attr, result[attr.lower()])

        # print(model)
        return base_model.parse_obj(model)
