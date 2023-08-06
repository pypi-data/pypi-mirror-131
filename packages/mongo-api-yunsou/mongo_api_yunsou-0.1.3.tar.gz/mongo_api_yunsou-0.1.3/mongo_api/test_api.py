from client import MongoDataBase
from tqdm import tqdm
import time

mongodb = MongoDataBase(num_procs=8)
collection_name = 'test'
host = '9.25.181.135' 
mongo_cols = mongodb.list_collections(host=host)
#对需要的字段建索引
index = ['vid']
print(f'mongo_cols:{mongo_cols}')
if collection_name in mongo_cols:
    while True:
        print('%s already exist, delete or not? [Y/n]' % collection_name)
        Yn = input().strip()
        if Yn in ['Y', 'y']:
            mongodb.delete_collection(collection_name, mongo_cols, host=host)    
            exit()
            break
        elif Yn in ['N', 'n']:
            mongodb.get_collection_info(collection_name, user='yanxp', host=host)
            break 
else: 
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    mongodb.create_collection(collection_name, user='yanxp', create_time=create_time, host=host)
    mongodb.create_index(collection_name, index, host=host)

data = []
chunk_size = 500000
maxlen = 10000000
for i in tqdm(range(maxlen)):
    for name in ['电视剧','电影','综艺']:
        data.append({'vid':'vid'+str(i), 'tag':name})
        if len(data) == chunk_size or i == maxlen - 1:
            mongodb.insert_tags_to_mongo(collection_name, data, host=host)
            data = []
mongodb.flush_insert()

mongo_length = mongodb.get_mongo_length(collection_name, host=host)
print(f'mongo_length:{mongo_length}')

vids = ['vid'+ str(i) for i in range(100000)]
result = mongodb.search_tag_in_mongo(collection_name, vids, 'vid', host=host)
print(f'search vid length:{len(result)}')

result = mongodb.search_tag_in_mongo(collection_name, ['电视剧'], 'tag', host=host)
print(f'search tag length:{len(result)}')

maxlen = 500000
for i in range(maxlen):
	for name in ['腾讯','阿里','百度']:
		data.append({'vid':'vid'+str(i), 'tag':name})

mongodb.update_tags_to_mongo(collection_name, data, ['vid', 'tag'], host=host)
print(f'update vid-tag pairs length:{len(result)}')

vids = ['vid'+ str(i) for i in range(500000)]

mongodb.delete_tag_in_mongo(collection_name, vids, 'vid', host=host)
mongodb.flush_delete()

result = mongodb.search_tag_in_mongo(collection_name, ['腾讯'], 'tag', host=host)
print(f'search new tags length:{len(result)}')

mongo_length = mongodb.get_mongo_length(collection_name, host=host)
print(f'delete and update mongo_length:{mongo_length}')

mongodb.delete_tag_in_mongo(collection_name, ['阿里'], 'tag', host=host)
mongodb.flush_delete()

mongo_length = mongodb.get_mongo_length(collection_name, host=host)
print(f'delete and update mongo_length:{mongo_length}')
