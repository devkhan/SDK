#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

from pymongo import MongoClient
from config import config
from flask import jsonify
from bson.objectid import ObjectId
import json

class Database:
    """
    This class gets the database instance, and exposes the collections.
    """

    def __init__(self, uri = False):        
        if type(uri) is str:
            self.client = MongoClient(uri)
        else:
            self.client = MongoClient(config['MONGODB_URL'])

        self.db = self.client[config['Database']]

    @property
    def user(self):
        """
        Returns the User Database collection
        """
        return self.db['user']

    @property
    def biodb(self):
        """
        Returns the biodb Database collection
        """
        print(type(self.db['softwares']))
        return self.db['softwares']

def validate_oid(func):
    def wrapper(oid, *args, **kwargs):
        if ObjectId.is_valid(oid):
            return func(oid, *args, **kwargs)
        return jsonify({'errors': True, 'msg': "Invalid OID"}), 400
    return wrapper