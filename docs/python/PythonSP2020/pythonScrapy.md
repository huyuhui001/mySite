### Initialize the project and `scrapy.cfg` will be created automatically
```
# /opt/projects/myPython/scrapy startproject pythonScrapy
```
File `scrapy.cfg`:
```
[settings]
default = pythonScrapy.settings

[deploy]
#url = http://localhost:6800/
project = pythonScrapy
```

### Define pipeline via fie `pipeline.py`
`class JsonPipeline(object)`
`class MongoPipeline(object)`

### Configure `settings.py` by adding two pipelines defined above two classes
```
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'pythonScrapy.pipelines.PythonscrapyPipeline': 300,
    'pythonScrapy.pipelines.JsonPipeline': 1,
    'pythonScrapy.pipelines.MongoPipeline': 2,
}

# Configure Mongo DB
MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'mydb'
```

### File `items.py` is to define which labels will be captured
```
class TedItem(scrapy.Item):
    talk = scrapy.Field()
    link = scrapy.Field()
```

### Start MongoDB Server
```
# mongod --config "/opt/mongodb/mongod.cfg" --fork
```

### Run the application
```
# /opt/projects/myPython/pythonScrapy/scrapy crawl ted
```
File `ted.json` was generated and all records were inserted into MongoDB
```
> use mydb
switched to db mydb

> show collections
Employee
ted

> db.ted.find().pretty()
```



