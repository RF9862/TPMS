
from pymongo import MongoClient
import time
from app.core.models.imagestobucket import upload_image_toS3, upload_video_toS3

cloud_url = 'mongodb://global_tnms:fkJmzaD0JINWr@tolltax.xyz:27000/?'
local_url = "mongodb://global_tnms:fkJmzaD0JINWr@mongo:27017/?authSource=admin&readPreference=primary&appname=mongodb-vscode%200.6.10&ssl=false"
db_name = 'TNMS_Live'
bucket_name = 'tpmsgsuntec'

class DATABASESERV:
    def __init__(self, cloud_mongodb_url, localdb_url, db_name):
        self.cloud_mongodb_client = MongoClient(cloud_mongodb_url)
        self.localdb_mongodb_client = MongoClient(localdb_url)
        self.cloud_db = self.cloud_mongodb_client[db_name]
        self.local_db = self.localdb_mongodb_client[db_name]

    def update_vehicle_details(self):
        local_coll = self.local_db['vehicle_detail']
        cloud_coll = self.cloud_db['vehicle_detail']
        myquery = {"archived":False}
        docs = list(local_coll.find(myquery, {"_id":0, "archived":0}))
       
        print(len(docs))
        if docs:
            imagepaths = [ele['image'] for ele in docs]
            vidpaths =  [ele['videoclip'] for ele in docs]
            for image in imagepaths:
                upload_image_toS3(bucket_name, image)
            for video in vidpaths:
                upload_video_toS3(bucket_name, video)
            # print(imagepaths)
            # print(vidpaths)
            resp = cloud_coll.insert_many(docs)
            # print(resp.acknowledged)
            if len(resp.inserted_ids) == len(docs):

                resp = local_coll.update_many(myquery, { "$set": { "archived": True} })
        docs = list(cloud_coll.find({}))
        # print(len(docs))


# SuperFastPython.com
# example of a periodic daemon thread
# from time import sleep
# from threading import Thread
 
# # task that runs at a fixed interval
# def background_task(interval_sec):
#     # run forever
#     while True:
#         # block for the interval
#         sleep(interval_sec)
#         # perform the task
#         x.update_vehicle_details()
#         print('Background task!')
 
# # create and start the daemon thread
# print('Starting background task...')
# daemon = Thread(target=background_task, args=(3,), daemon=True, name='Background')
# daemon.start()
# # main thread is carrying on...
# print('Main thread is carrying on...')
# sleep(10)
# print('Main thread done.')