from datetime import datetime


class MongoStorage:

    def __init__(self, engine):
        self.engine = engine
        self.worker_id_table = "snowflake_workerid"

    def insert_one(self, record):
        collection = self.engine.get_collection( self.worker_id_table)
        collection.insert_one(self.__convert_to_dict(record))

    def update_one(self, ip, process_id):
        collections = self.engine.get_collection(self.worker_id_table)
        where_ = {"$and": [{"ip": {"$eq": ip}}, {"processid": {"$eq": process_id}}]}
        update_ = {"$set": {"regdate": datetime.now()}}
        collections.update_one(where_, update_)

    def find_(self, model, ip, process_id):
        collection = self.engine.get_collection(self.worker_id_table)
        where_ = {"$and": [{"ip": {"$eq": ip}}, {"processid": {"$eq": process_id}}]}
        cursor = collection.find(where_)
        result_list = list(cursor)
        return [model.parse_obj(result) for result in result_list]

    def list_all(self, model):
        collection = self.engine.get_collection(self.worker_id_table)
        cursor = collection.find()
        result_list = list(cursor)
        return [model.parse_obj(result) for result in result_list]

    def delete_by_id(self, ip_, process_id):
        collection = self.engine.get_collection(self.worker_id_table)
        where_ = {"$and": [{"ip": {"$eq": ip_}}, {"processid": {"$eq": process_id}}]}
        collection.delete_one(where_)

    def __convert_to_dict(self, instance) -> dict:
        if type(instance) is not dict:
            return instance.dict(by_alias=True)
        else:
            return instance
