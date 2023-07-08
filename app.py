from flask import Flask, jsonify, abort,request
from pydantic import BaseModel
import pymongo
import json

db = "testdb"
url = "localhost"
port = 27017

mycol = None
def connect():
    global mycol
    myclient = pymongo.MongoClient(url + ":" + str(port))
    
    if db not in myclient.list_database_names():
        myclient[db]
       
    mydb = myclient[db]
    mycol = mydb["Community"]
    
    return "Connected"

connect()
app = Flask(__name__, static_url_path='')
@app.route("/", methods=["GET"])
def root():
    return app.send_static_file('index.html')

@app.route("/items", methods=["GET"])
def get_items():
    result = []
    for x in mycol.find():
        result.append({
            "_id":str((x["_id"])),
            "title":x["title"],
            "content":x["content"],
            }
        )
    return jsonify({"success": True,"data":result})

@app.route("/", methods=["POST"])
def post_add():
    x = mycol.insert_one(dict(request.get_json()))
    return jsonify({"data":"","success":True}), 201

if __name__ == "__main__":
    app.run(debug=True)
