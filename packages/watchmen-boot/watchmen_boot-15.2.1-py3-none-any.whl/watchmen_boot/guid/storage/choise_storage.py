from watchmen_boot.config.config import settings
from watchmen_boot.constants.database.constant import MONGO, MYSQL, ORACLE
from watchmen_boot.utils.datasource_utils import get_default_datasource


def find_template():
    default_datasource = get_default_datasource()
    if settings.STORAGE_ENGINE == MONGO:
        from watchmen_boot.storage.mongo.mongo_client import MongoEngine
        from watchmen_boot.guid.storage.mongo.mongo_template import MongoStorage
        engine = MongoEngine(default_datasource)
        return MongoStorage(engine.get_engine())
    elif settings.STORAGE_ENGINE == MYSQL:
        from watchmen_boot.storage.mysql.mysql_client import MysqlEngine
        from watchmen_boot.guid.storage.mysql.mysql_template import MysqlStorage
        engine = MysqlEngine(default_datasource)
        return MysqlStorage(engine.get_engine())
    elif settings.STORAGE_ENGINE == ORACLE:
        from watchmen_boot.storage.oracle.oracle_client import OracleEngine
        from watchmen_boot.guid.storage.oracle.oracle_template import OracleStorage
        engine = OracleEngine(default_datasource)
        return OracleStorage(engine.get_engine())