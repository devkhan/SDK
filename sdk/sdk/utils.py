#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

from pymongo import MongoClient
from sdk.config import config
from flask import jsonify
from bson.objectid import ObjectId
import json, requests

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
        return self.db['cell']

def validate_oid(func):
    def wrapper(oid, *args, **kwargs):
        if ObjectId.is_valid(oid):
            return func(oid, *args, **kwargs)
        return jsonify({'errors': True, 'msg': "Invalid OID"}), 400
    return wrapper

def retrieve_uniprot_id(geneid):
    try:
        req = requests.get(config['MYGENE_URL']+'query?q=' + geneid)
        json_object = req.json()
        req = requests.get(config['MYGENE_URL']+'gene/'+str(json_object['hits'][0]['entrezgene'])+'?fields=uniprot')
        json_object = req.json()
        return str(json_object['uniprot']['Swiss-Prot'])
    except:
        return False

def get_fasta_seq(gene_id):
    try:
        req = requests.get(config['UNIPROT_URL']+retrieve_uniprot_id(gene_id)+'.fasta')
        return req.text
    except:
        return False
