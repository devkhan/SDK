#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

# Global imports
from bson.objectid import ObjectId
from bson import json_util

import json
# Local imports
from sdk import utils


class Cell(object):
    def __init__(self, c_id):
        inst = utils.Database().biodb.find_one({"_id": ObjectId(c_id)})
        self.k = False

        if inst is not None:
            self.k = True
            self._meta = inst

    @property
    def oid(self):
        return str(self._meta['_id']) if self.k is True else 0x000000000000000000000000

    @property
    def name(self):
        return self._meta['cell_name'] if self.k is True else None

    @property
    def tags(self):
        return self._meta['tags'] if self.k is True else None

    @property
    def location(self):
        return self._meta['location'] if self.k is True else None

    @property
    def shape(self):
        return self._meta['shape'] if self.k is True else None

    @property
    def dimensions(self):
        return self._meta['dimension'] if self.k is True else None

    @property
    def dimensionComments(self):
        return (self._meta['dimensionComment'], None)[self.k]

    @property
    def function(self):
        return (self._meta['function'], None)[self.k]

    @property
    def imageURL(self):
        return (self._meta['image_url'], '#')[self.k]

    @property
    def inferences(self):
        return (self._meta['inferences'], None)[self.k]

    @property
    def polarityIndex(self):
        return (self._meta['polarity_index'], None)[self.k]

    @property
    def sourceLink(self):
        return (self._meta['link_of_source'], None)[self.k]

    @property
    def comments(self):
        return (self._meta['comments'], None)[self.k]

    @property
    def hash(self):
        return {
            "oid": self.oid,
            "cell_name": self.name,
            "tags": self.tags,
            "location": self.location,
            "shape": self.shape,
            "dimensions": self.dimensions,
            "dimensionComments": self.dimensionComments,
            "function": self.function,
            "imageURL": self.imageURL,
            "inferences": self.inferences,
            "polarityIndex": self.polarityIndex,
            "sourceLink": self.sourceLink,
            "comments": self.comments
        }

class Manage(object):
    def add(self, software_name, tags, primary_link, one_liner, paid, primary_ref = "N.A", remarks = "N.A", meta = None):
        """
        Adds the software into the Database. Any additional properties should
        only be added into `meta`.
        """
        if all([
            type(software_name) is str,
            type(tags) is list,
            type(primary_link) is str,
            type(one_liner) is str,
            type(paid) is bool,
            type(primary_ref) is str,
            type(remarks) is str,
            type(meta) is dict or meta is None
        ]):
            sw = {
                "software_name": software_name,
                "tags": tags,
                "primary_link": primary_link,
                "one_liner": one_liner,
                "paid": paid,
                "primary_ref": primary_ref,
                "remarks": remarks,
                "meta": meta
            }

            # Add document to collection and return the objectId.
            return utils.Database().biodb.insert_one(sw).inserted_id

        return False

    def delete(self, cell_id):
        "Deletes a software from Database."
        return utils.Database().biodb.remove({"_id": ObjectId(cell_id)})['n'] > 0

    def update(
        self,
        software_id,
        software_name = None,
        primary_link = None,
        one_liner = None,
        paid = None,
        primary_ref = None,
        remarks = None,
        meta = None
        ):

        update = {}

        def __update_macro(key, val, _type):
            if all([
                val is not None,
                type(val) is _type
            ]):
                update[key] = val

        __update_macro('software_name', software_name, str)
        __update_macro('primary_link', primary_link, str)
        __update_macro('one_liner', one_liner, str)
        __update_macro('paid', paid, bool)
        __update_macro('primary_ref', primary_ref, str)
        __update_macro('remarks', remarks, str)
        __update_macro('meta', meta, dict)

        if len(update) is not 0:
            utils.Database().biodb.update(
                {'_id': ObjectId(software_id)},
                {'$set': update},
                upsert = False,
                multi = False
            )
            return True

        return False

    def search(self, query_string):
        results = utils.Database().biodb.find({"cell_name":{"$regex": query_string}})
        serialized_results = [json.dumps(result, default=json_util.default, separators=(',', ':')) for result in results]
        results = utils.Database().biodb.find({"function":{"$regex": query_string}})
        serialized_results = [json.dumps(result, default=json_util.default, separators=(',', ':')) for result in results]
        return serialized_results

class Feed(object):
    def create(page = 0, tags = None):
        pass
