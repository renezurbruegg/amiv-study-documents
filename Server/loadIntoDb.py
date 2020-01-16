# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pickle
import time
from datetime import date, datetime
from datetime import timedelta

import feedparser
from pylogging import HandlerType, setup_logger
import json
from pymongo import MongoClient

from Server import mat_loader

logger = logging.getLogger(__name__)
setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER, allow_console_logging=True,
             console_log_level=logging.DEBUG, max_file_size_bytes=1000000)
from os import listdir
from os.path import isfile, join

client = MongoClient("localhost", 27017)
mydb = client["amivmat"]
mydb['links'].drop()

def insert(dictObject, db):
    """ Inserts a given menu Object into the menus database.<br>
    If an object with the current id, date, mensaName and lang allready exists, it will be updated """

    """ res = db["menus"].update_one(
        {"id": dictObject["id"],
         "date": dictObject["date"],
         "mensaName": dictObject["mensaName"],
         "lang": dictObject["lang"]
         }, {"$set": dictObject}, upsert=True)

    print("modifed: id: " + str(dictObject["id"].encode('utf-8')) + " Date: " + dictObject["date"] + " lang: " +
          dictObject["lang"])
    if res.upserted_id is None:
        print("res: modified: " + str(res.modified_count) + " matched: " + str(res.matched_count))
    else:
        print("res: inserted") """


def parse(data):
    entries = []
    cats = {'Prüfungen': 'exams', 'Zusammenfassungen':'cheat sheets', 'Skripts und ähnliches': 'lecture documents', 'Übungsserien und ähnliches': 'exercises'}

    db = mydb['links']
    info = data['info']
    sem = ""
    if(len(info['sem']) > 0):
        sem = info['sem'][0]
    name = info['name']
    dep = info['dep']
    master = False
    if 'master' in data:
        master = data['master']

    for entry in data:
        elem = data[entry]
        if(entry == 'info' or entry == 'master'):
            continue

        for el in elem:
            if(entry in cats):
                cat = cats[entry]
            else:
                cat = entry
                print("not found " + entry)
            obj = {
                'fach': name,
                'category' : cat,
                'title': el['title'],
                'author': el['author'],
                'year': el['year'],
                'files': el['links'],
                'sem': sem,
                'department': dep,
                'master': master
            }
            db.update_one(
                {"title": obj["title"],
                 "year": obj["year"],
                 "author": obj["author"],
                 "fach": obj['fach']
                 }, {"$set": obj}, upsert=True)

def main():

    masters = ["Biomedical Engineering", "Information Techn", "Energy Science", "Micro and", "Robotics"]

    onlyfiles = [f for f in listdir('res') if isfile(join('res', f))]
    
    for file in onlyfiles:
        """for m in masters:
          if m in str(file):
            print(file)
            """
        if("json" not in str(file)):
            continue
        with open('res/'+str(file)) as json_file:
            data = json.load(json_file)
            parse(data)

            """with open('res/'+str(file), 'w') as outfile:
                text = json.dumps(data, sort_keys=True, indent=4)
                outfile.write(text)"""

    """Main entry point of the app
    .

    client = MongoClient("localhost", 27017)
    mydb = client["amivmat"]
    for entry in mat_loader.getEntries():
        insert(entry, mydb)"""

if __name__ == '__main__':
    main()
