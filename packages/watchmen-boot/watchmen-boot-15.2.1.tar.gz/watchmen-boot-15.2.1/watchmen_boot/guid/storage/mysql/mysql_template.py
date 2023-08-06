from datetime import datetime
from operator import eq

from sqlalchemy import MetaData, Table, Column, String, Integer, Date, insert, update, and_, select, delete

from watchmen_boot.storage.mysql.mysql_utils import parse_obj


class MysqlStorage:

    def __init__(self, engine):
        self.engine = engine
        self.metadata = MetaData()
        self.worker_id_table = Table("snowflake_workerid", self.metadata,
                                     Column('ip', String(100), primary_key=True),
                                     Column('processid', String(60), primary_key=True),
                                     Column('workerid', Integer, nullable=False),
                                     Column('regdate', Date, nullable=True)
                                     )

    def insert_one(self, record):
        table = self.worker_id_table
        stmt = insert(table).values(record)
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(stmt)

    def update_one(self, ip, process_id):
        table = self.worker_id_table
        stmt = update(table)
        filter_ = [eq(table.c["ip"], ip), eq(table.c["processid"], process_id)]
        stmt = stmt.where(and_(*filter_))
        stmt = stmt.values({"regdate": datetime.now()})
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(stmt)

    def find_(self, model, ip, process_id):
        table = self.worker_id_table
        filter_ = [eq(table.c["ip"], ip), eq(table.c["processid"], process_id)]
        stmt = select(table).where(and_(*filter_))
        with self.engine.connect() as conn:
            cursor = conn.execute(stmt).cursor
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                result = {}
                for index, name in enumerate(columns):
                    result[name] = row[index]
                return parse_obj(model, result, table)

    def list_all(self, model):
        table = self.worker_id_table
        stmt = select(table)
        with self.engine.connect() as conn:
            cursor = conn.execute(stmt).cursor
            columns = [col[0] for col in cursor.description]
            res = cursor.fetchall()
        results = []
        for row in res:
            result = {}
            for index, name in enumerate(columns):
                result[name] = row[index]
            results.append(parse_obj(model, result, table))
        return results

    def delete_by_id(self, ip_, process_id):
        table = self.worker_id_table
        filter_ = [eq(table.c["ip"], ip_), eq(table.c["processid"], process_id)]
        stmt = delete(table).where(and_(*filter_))
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(stmt)
