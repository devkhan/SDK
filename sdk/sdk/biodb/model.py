#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

# Global imports
from bson.objectid import ObjectId

# Local imports
from sdk import utils


class Software(object):
    def __init__(self, sw_id):
        inst = utils.Database().biodb.find_one({"_id": ObjectId(sw_id)})
        self.k = False

        if inst is not None:
            self.k = True
            self._meta = inst

    @property
    def oid(self):
        return str(self._meta['_id']) if self.k is True else 0x000000000000000000000000

    @property
    def name(self):
        return self._meta['software_name'] if self.k is True else None

    @property
    def tags(self):
        return self._meta['tags'] if self.k is True else None

    @property
    def link(self):
        return self._meta['primary_link'] if self.k is True else None

    @property
    def one_liner(self):
        return self._meta['one_liner'] if self.k is True else None

    @property
    def paid(self):
        return self._meta['paid'] if self.k is True else None

    @property
    def ref(self):
        return self._meta['primary_ref'] if self.k is True else None

    @property
    def remarks(self):
        return self._meta['remarks'] if self.k is True else None

    @property
    def meta(self):
        return self._meta['meta'] if self.k is True else None

    @property
    def person(self):
        return self._meta['person'] if self.k is True else None
    

    @property
    def hash(self):
        return {
            "oid": self.oid,
            "software_name": self.name,
            "tags": self.tags,
            "primary_link": self.link,
            "one_liner": self.one_liner,
            "paid": self.paid,
            "primary_ref": self.ref,
            "remarks": self.remarks,
            "meta": self.meta
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

    def delete(self, software_id):
        "Deletes a software from Database."
        return utils.Database().biodb.remove({"_id": ObjectId(software_id)})['n'] > 0

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

class Feed(object):
    def create(page = 0, tags = None):
        pass
