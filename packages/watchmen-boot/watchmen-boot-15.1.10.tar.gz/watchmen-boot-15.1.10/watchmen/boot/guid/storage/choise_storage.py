from watchmen.boot.config.config import settings
from watchmen.boot.constants.database.constant import MONGO, MYSQL, ORACLE
from watchmen.boot.utils.datasource_utils import get_default_datasource


def find_template():
    default_datasource = get_default_datasource()
    if settings.STORAGE_ENGINE == MONGO:
        from watchmen.boot.storage.mongo.mongo_client import MongoEngine
        from watchmen.boot.guid.storage.mongo.mongo_template import MongoStorage
        engine = MongoEngine(default_datasource)
        return MongoStorage(engine.get_engine())
    elif settings.STORAGE_ENGINE == MYSQL:
        from watchmen.boot.storage.mysql.mysql_client import MysqlEngine
        from watchmen.boot.guid.storage.mysql.mysql_template import MysqlStorage
        engine = MysqlEngine(default_datasource)
        return MysqlStorage(engine.get_engine())
    elif settings.STORAGE_ENGINE == ORACLE:
        from watchmen.boot.storage.oracle.oracle_client import OracleEngine
        from watchmen.boot.guid.storage.oracle.oracle_template import OracleStorage
        engine = OracleEngine(default_datasource)
        return OracleStorage(engine.get_engine())