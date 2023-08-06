import multiprocessing as mp

from .utils import _insert_mongo, _update_mongo,  _delete_mongo, _search_mongo, get_pymongo_client


class MongoDataBase:
    def __init__(
        self,
        chunk_size=2048,
        max_parallel=mp.cpu_count(),
        num_procs=4,
        db_name="Dataset",
    ):
        self.db_name = db_name
        self.chunk_size = chunk_size
        self.pool = mp.Pool(num_procs)
        self.tasks = []
        self.max_parallel = max_parallel

    # Api 接口

    # 等待进程完成
    def _wait(self, num_tasks=0):
        while len(self.tasks) > num_tasks:
            for i, task in enumerate(self.tasks):
                if self.tasks[i].ready():
                    del self.tasks[i]
                    break

    # 创建集合
    def create_collection(self, collection_name, user=None, create_time=None, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_col = mongo_db[collection_name]
        mongo_col.insert_one({"User": user, "Create_time": create_time})
        mongoclient.close()

    # 删除集合
    def delete_collection(self, collection_name, mongo_cols, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_col = mongo_db[collection_name]
        mongo_col.drop()
        mongo_col.drop_index("vid")
        mongoclient.close()

    # 返回集合信息
    def get_collection_info(self, collection_name, user=None, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_col = mongo_db[collection_name]
        user_info = mongo_col.find_one({"User": user})
        user = user_info["User"]
        create_time = user_info["Create_time"]
        print(
            f" user [{user}] create collection [{collection_name}] in mongo at [{create_time}]."
        )
        mongoclient.close()

    # 集合列表
    def list_collections(self, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_cols = mongo_db.list_collection_names(session=None)
        print(f"collection [{mongo_cols}] in mongo.")
        mongoclient.close()
        return mongo_cols

    # 获取mongo集合长度
    def get_mongo_length(self, collection_name, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_col = mongo_db[collection_name]
        mongo_length = mongo_col.estimated_document_count()
        mongoclient.close()
        return mongo_length

    # mongo中根据文件名查询
    def search_tag_in_mongo(self, collection_name, data, key, host='9.25.181.135', port=27017):
        data_iter = (
            dict(
                collection_name=collection_name,
                content=data[chunk_beg: chunk_beg + self.chunk_size],
                db_name=self.db_name,
                key=key,
                host=host,
                port=port,
            )
            for chunk_beg in range(0, len(data), self.chunk_size)
        )
        outs = []
        for res in self.pool.map(_search_mongo, data_iter):
            outs.extend(res)
        return outs
    
    # mongo中根据文件名删除
    def delete_tag_in_mongo(self, collection_name, data, key, host='9.25.181.135', port=27017):
        data_iter = (
            dict(
                collection_name=collection_name,
                content=data[chunk_beg: chunk_beg + self.chunk_size],
                db_name=self.db_name,
                key=key,
                host=host,
                port=port,
            )
            for chunk_beg in range(0, len(data), self.chunk_size)
        )
        for res in data_iter :
            self._wait(self.max_parallel - 1)
            task = self.pool.apply_async(
                _delete_mongo, (res, )
            )
            self.tasks.append(task)
    
    # 删除落盘
    def flush_delete(self):
        self._wait()
        print('deleting done!', flush=True)
    
    # mongo中根据文件名更新
    def update_tags_to_mongo(self, collection_name, data, keys, host='9.25.181.135', port=27017):
        data_iter = (
            dict(
                collection_name=collection_name,
                content=data[chunk_beg: chunk_beg + self.chunk_size],
                db_name=self.db_name,
                keys=keys,
                host=host,
                port=port,
            )
            for chunk_beg in range(0, len(data), self.chunk_size)
        )
        for res in data_iter :
            self._wait(self.max_parallel - 1)
            task = self.pool.apply_async(
                _update_mongo, (res, )
            )
    # 更新落盘
    def flush_update(self):
        self._wait()
        print('updating done!', flush=True)

    # 根据文件名插入
    def insert_tags_to_mongo(self, collection_name, data, host='9.25.181.135', port=27017):
        self._wait(self.max_parallel - 1)
        task = self.pool.apply_async(
            _insert_mongo, (collection_name, data, self.db_name, host, port)
        )
        self.tasks.append(task)

    # 插入落盘
    def flush_insert(self):
        self._wait()
        print('inserting done!', flush=True)
    
    # 创建索引
    def create_index(self, collection_name, index, host='9.25.181.135', port=27017):
        mongoclient = get_pymongo_client(host, port)
        mongo_db = mongoclient[self.db_name]
        mongo_col = mongo_db[collection_name]
        for key in index:
            mongo_col.create_index(key)
        mongoclient.close()
