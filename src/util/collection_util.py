from src.db.soul import SoulDB
from pymongo import IndexModel


class CollectionUtil:
    @classmethod
    def collection_swap(cls, db_obj, collection_name, insert_docs):
        collection_names = db_obj.collection_names()
        exist_col = (f'{collection_name}' in collection_names)
        if not exist_col:
            col = db_obj.get_collection(f'{collection_name}')
            col.insert(insert_docs)
            return
        exist_bak_col = (f'{collection_name}_bak' in collection_names)
        temp_col = db_obj.get_collection(f'{collection_name}_temp')
        col = db_obj.get_collection(f'{collection_name}')
        temp_col.insert(insert_docs)
        if exist_bak_col:
            db_obj.drop_collection(f'{collection_name}_bak')
        if exist_col:
            col.rename(f'{collection_name}_bak')
        temp_col.rename(f'{collection_name}')

    @classmethod
    def create_collection_index(cls, db_collection, index_fields, unique=False):
        index_field_infos = []
        index_name = ''
        for field in index_fields:
            index_field_infos.append((field, 1))
            index_name = f"{index_name}_{field}"
        model = IndexModel(index_field_infos, name=index_name, unique=unique)
        db_collection.create_indexes([model])

    @classmethod
    def check_exist_collection(cls, db_obj, collection_name):
        if collection_name in db_obj.collection_names():
            return True
        return False
