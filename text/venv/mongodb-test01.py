import pymongo

#创建MongoDB的连接对象
client = pymongo.MongoClient('mongodb://localhost:27017/')

#指定数据库
db = client.mydemo

#指定集合Collection对象
collection = db.students

# 一条数据
student = {
    'id': '20170101',
    'name': '小明',
    'age': 22,
    'gender': '男性'
}

#插入数据
result = collection.insert_one(student)   #<pymongo.results.InsertOneResult object at 0x00000260E589E7C8>
print(result)  # <pymongo.results.InsertOneResult object at 0x1034e08c8>
print(result.inserted_id)  #5fc6009d975b99593a36aeb4

# 多条数据
student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}

result = collection.insert_many([student1, student2])
print(result)  # <<pymongo.results.InsertManyResult object at 0x000001F3BCFDAF88>>
print(result.inserted_ids) #[ObjectId('5fc600e15bd8c71d1dbe5e65'), ObjectId('5fc600e15bd8c71d1dbe5e66')]

#查询数据库

# 查询一条数据
result = collection.find_one({"name": "Mike"})
print(type(result))  # <class 'dict'>
print(result)   #{'_id': ObjectId('5fc600e15bd8c71d1dbe5e66'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}

# 通过_id属性来查询， 不存在则返回None
from bson.objectid import ObjectId
result = collection.find_one({'_id': ObjectId('5fc600e15bd8c71d1dbe5e66')})
print(result)  #{'_id': ObjectId('5fc600e15bd8c71d1dbe5e66'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}

# 查询多条数据, 返回一个生成器
results = collection.find({"age": 21})
print(results)  # <pymongo.cursor.Cursor object at 0x000001B160B4B4C8>
for result in results:
    print(result)
'''{'_id': ObjectId('5fc600e15bd8c71d1dbe5e66'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('5fc60117f0d5c79dc4025667'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('5fc602ba3ad9ca76a34c1aca'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('5fc602fbcff55fa12b486e4e'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('5fc603477a1033ab1c18a24a'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}'''

# 条件查询
results = collection.find({"age": {"$gt": 20}})  #大于20岁
for result in results:
    print(result)

# 正则匹配查询
results = collection.find({"name": {"$regex": "^M.*"}})
for result in results:
    print(result)

## 转为list
print(db.collection.find())  #<pymongo.cursor.Cursor object at 0x0000017C4A59A188>

'''符号	表示	含义	          示例
:	    =	    等于         {“age”: 20}
$lt	    <	    小于	     {“age”: {"$lt": 20}}
$gt  	>	    大于	     {“age”: {"$gt": 20}}
$lte	<=	    小于等于     {“age”: {"$lte": 20}}
$gte	>=	    大于等于     {“age”: {"$gte": 20}}
$ne	    !=	    不等于	     {“age”: {"$ne": 20}}
$in	    in	    范围内	     {“age”: {"$in": [20, 30]}}
$nin	not in	不在范围内	 {“age”: {"$nin": [20, 30]}}'''

'''
符号	   含义	                 示例	                    示例说明
$regex	匹配正则表达式	{“name”: {"$regex": “^M.*”}}	name以M开头
$exists	属性是否存在	{“name”: {"$exists": True}}    	name属性存在
$type	类型判断	    {“age”: {"$type": “int”}}	   age的类型为int
$mod	数字模操作      {“age”: {"$mod": [5, 0]}}      	年龄模5余0
$text	文本查询	    {“text”: {"$search": “Mike”}}	text类型的属性中包含字符串Mike
$where	高级条件查询	{“name”: {"$where": “obj.age==obj.count”}}	自身年龄等于自身数量'''

#查询计数
count = collection.find().count()
print(count)

#数据排序
# 升序pymongo.ASCENDING 降序pymongo.DESCENDING
results = collection.find().sort("name", pymongo.ASCENDING)
print([result["name"] for result in results])

#数据的偏移
results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
print([result['name'] for result in results])
# ['小明']

results = collection.find().sort('name', pymongo.ASCENDING).skip(1).limit(1)
print([result['name'] for result in results])
# # ['Mike']
#
# # 数据库数量非常庞大的时候，不要使用大的偏移量
from bson.objectid import ObjectId
results = collection.find({'_id': {'$gt': ObjectId('5b1209ccd7696c437c51d5bb')}})
print([result['name'] for result in results])

#更新数据库
# update_one(filter, update, upsert=False,
# bypass_document_validation=False, collation=None, array_filters=None, session=None)
#
# update_many(filter, update, upsert=False,
# array_filters=None, bypass_document_validation=False, collation=None, session=None)

# 过时了
# update(spec, document, upsert=False,
# manipulate=False, multi=False, check_keys=True, **kwargs)


condition = {'name': 'Mike'}
student = collection.find_one(condition)
student['age'] = 25
# 全部用student字典替换
# result = collection.update(condition, student)
# 只更新student字典内存在的字段
result = collection.update(condition, {'$set': student})
print(result)
# {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}

condition = {'name': 'Mike'}
student = collection.find_one(condition)
student['age'] = 26
result = collection.update_one(condition, {'$set': student})
print(result)
# <pymongo.results.UpdateResult object at 0x1034de708>

print(result.matched_count, result.modified_count)
# 1 1

condition = {'age': {'$gt': 20}}
result = collection.update_one(condition, {'$inc': {'age': 1}})
print(result)
# <pymongo.results.UpdateResult object at 0x1034e8588>
print(result.matched_count, result.modified_count)

#数据删除
result = collection.remove({'name': 'Jordan'})
print(result)

# 删除一条
result = collection.delete_one({'name': 'Kevin'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$lt': 25}})
print(result.deleted_count)

# 删除多条
result = collection.delete_many({'name': 'Kevin'})