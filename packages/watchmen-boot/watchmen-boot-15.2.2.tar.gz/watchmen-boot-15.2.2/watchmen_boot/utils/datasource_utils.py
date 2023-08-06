from watchmen_boot.config.config import settings
from watchmen_boot.constants.database.constant import MONGO, MYSQL, ORACLE
from watchmen_boot.storage.model.data_source import DataSource, DataSourceParam


def get_default_datasource():
    datasource = DataSource()
    datasource.dataSourceCode = "default"
    datasource.dataSourceType = settings.STORAGE_ENGINE
    if settings.STORAGE_ENGINE == MONGO:
        datasource.username = settings.MONGO_USERNAME
        datasource.password = settings.MONGO_PASSWORD
        datasource.name = settings.MONGO_DATABASE
        datasource.host = settings.MONGO_HOST
        datasource.port = settings.MONGO_PORT
        datasource.dataSourceType = "mongodb"
        return datasource
    elif settings.STORAGE_ENGINE == MYSQL:
        datasource.username = settings.MYSQL_USER
        datasource.password = settings.MYSQL_PASSWORD
        datasource.name = settings.MYSQL_DATABASE
        datasource.host = settings.MYSQL_HOST
        datasource.port = settings.MYSQL_PORT
        datasource.dataSourceType = "mysql"
        return datasource
    elif settings.STORAGE_ENGINE == ORACLE:
        datasource.username = settings.ORACLE_USER
        datasource.password = settings.ORACLE_PASSWORD
        datasource.name = settings.ORACLE_NAME
        datasource.host = settings.ORACLE_HOST
        datasource.port = settings.ORACLE_PORT
        datasource.dataSourceType = "oracle"
        datasource.params = []
        if settings.ORACLE_SERVICE and settings.ORACLE_SERVICE != "":
            ds_param_service = DataSourceParam(**{
                'name': 'service_name',
                'value': settings.ORACLE_SERVICE
            })
            datasource.params.append(ds_param_service)
        if settings.ORACLE_SID and settings.ORACLE_SID != "":
            ds_param_sid = DataSourceParam(**{
                'name': 'SID',
                'value': settings.ORACLE_SID
            })
            datasource.params.append(ds_param_sid)
        return datasource
