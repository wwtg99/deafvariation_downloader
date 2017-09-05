"""
Store json data to mongodb
"""

from pymongo import MongoClient
import json
import os
import argparse


def connect(args):
    """

    :param args:
    :return:
    :rtype pymongo.collection.Collection
    """
    conn = MongoClient(host=args.host, port=args.port)
    return conn.get_database(args.database).get_collection(args.collection)


def insert_data(file, conn, replace=False):
    """

    :param file:
    :param pymongo.collection.Collection conn:
    :param replace
    :return:
    """
    n = 0
    with open(file) as fh:
        data = json.load(fh)
        for d in data:
            mid = d['id']
            d['_id'] = mid
            if replace:
                res = conn.replace_one({'_id': mid}, d, upsert=True)
                if res.modified_count > 0 or res.upserted_id:
                    n += 1
            else:
                res = conn.insert_one(d)
                n += 1
    print("Insert file %s, success %d" % (file, n))
    return n


def insert_directory(directory, conn, replace=False):
    """

    :param directory:
    :param conn:
    :param replace:
    :return:
    """
    for rt, dirs, files in os.walk(directory):
        for fs in files:
            st = os.path.splitext(fs)
            if len(st) > 1 and st[1] == '.json':
                insert_data(os.path.realpath(os.path.join(rt, fs)), conn, replace)


def parse(args):
    """

    :param args:
    :return:
    """
    files = args.files
    conn = connect(args)
    replace = args.replace
    for f in files:
        if os.path.isdir(f):
            insert_directory(f, conn, replace)
        else:
            insert_data(f, conn, replace)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', help='File or directory to store in mongodb.', nargs='+')
    parser.add_argument('-t', '--host', help='Mongodb host (default localhost)', default='localhost')
    parser.add_argument('-p', '--port', help='Mongodb port (default 27017)', default=27017, type=int)
    parser.add_argument('-d', '--database', help='Mongodb database (default test)', default='test')
    parser.add_argument('-c', '--collection', help='Mongodb collection (default deafv)', default='deafv')
    parser.add_argument('-r', '--replace', help='Whether to replace old data (default false)', action='store_true')
    args = parser.parse_args()
    parse(args)
