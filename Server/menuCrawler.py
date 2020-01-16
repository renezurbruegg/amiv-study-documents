# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pickle
import time
from datetime import date, datetime
from datetime import timedelta

import feedparser
from pylogging import HandlerType, setup_logger
from pymongo import MongoClient

from Server import mat_loader

logger = logging.getLogger(__name__)
setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER, allow_console_logging=True,
             console_log_level=logging.DEBUG, max_file_size_bytes=1000000)



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



def main():
    """Main entry point of the app. """
    client = MongoClient("localhost", 27017)
    mydb = client["amivmat"]
    for entry in mat_loader.getEntries():
        insert(entry, mydb)

if __name__ == '__main__':
    main()
