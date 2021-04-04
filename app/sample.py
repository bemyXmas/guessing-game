import os
import random

import pymongo
import redis

from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient

# App
app = Flask(__name__, template_folder='templates')

# connect to MongoDB
mongoClient = MongoClient(
    'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ[
        'MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379),
                          db=os.environ.get("REDIS_DB", 0))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/start', methods=["POST"])
def start():
    stat = {
        "question": ["_", "_", "_", "_"],
        "answer": ["_", "_", "_", "_"],
        "guess_times": 0,
    }
    str_list = ['A', 'B', 'C', 'D']
    for num in range(4):
        stat["question"][num] = str_list[random.randint(0, 3)]
    db.test.insert_one(stat)
    question_num = db.test.find_one(sort=[('_id', pymongo.DESCENDING)])
    return render_template('set.html', question_num=question_num)


@app.route('/set', methods=["GET", "POST"])
def guess():
    question_num = db.test.find_one(sort=[('_id', pymongo.DESCENDING)])
    if request.method == "POST":
        if question_num["question"][0] != question_num["answer"][0]:
            while request.form['button'] != question_num["question"][0]:
                db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
                return redirect("/set")
            db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
            db.test.update_one({"_id": question_num["_id"]}, {"$set": {f"answer.{0}": question_num["question"][0]}})
            return redirect("/set")
        elif question_num["question"][1] != question_num["answer"][1]:
            while request.form['button'] != question_num["question"][1]:
                db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
                return redirect("/set")
            db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
            db.test.update_one({"_id": question_num["_id"]}, {"$set": {f"answer.{1}": question_num["question"][1]}})
            return redirect("/set")
        elif question_num["question"][2] != question_num["answer"][2]:
            while request.form['button'] != question_num["question"][2]:
                db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
                return redirect("/set")
            db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
            db.test.update_one({"_id": question_num["_id"]}, {"$set": {f"answer.{2}": question_num["question"][2]}})
            return redirect("/set")
        elif question_num["question"][3] != question_num["answer"][3]:
            while request.form['button'] != question_num["question"][3]:
                db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
                return redirect("/set")
            db.test.update_one({"_id": question_num["_id"]}, {"$inc": {"guess_times": 1}})
            db.test.update_one({"_id": question_num["_id"]}, {"$set": {f"answer.{3}": question_num["question"][3]}})
            return redirect("/set")
    elif request.method == "GET":
        return render_template('set.html', question_num=question_num)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)
