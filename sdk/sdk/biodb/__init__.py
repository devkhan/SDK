#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

import json

from bson.objectid import ObjectId
from flask import Flask, Blueprint, render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from user import model as user_model
from . import model as biodb_model
from utils import validate_oid

biodb = Blueprint('biodb', __name__, template_folder='templates')

@biodb.route('/')
def get():
    return "Test"

@biodb.route('/software/add', methods = ['POST'])
def add():
    # Get form data as an ImmutableMultiDict.
    sw=request.form
    if biodb_model.Manage().add(sw.get('software_name', type=str), sw.get('tags', type=str).split(','), sw.get('primary_link', type=str), sw.get('one_liner', type=str), True if sw.get('paid', type=str) == 'P' else False):
        response = {
            'status' : 'ok',
            'message' : 'hello there'
        }
        return jsonify(response), 200
    else:
        response = {
            'status' : 'not ok',
            'message': 'not working'
        }
        return jsonify(response), 200


@biodb.route('/software', methods = ['GET'])
def gets():
    return render_template('software.html')

@biodb.route('/software/<oid>', methods = ['GET'])
@validate_oid
def get_software_detail(oid):
    sw = biodb_model.Software(oid)
    return render_template('software.html', oid=sw.oid, software_name=sw.name, added_date="100000 BC", primary_link=sw.link, tags=['one','two','three'], person=sw.person, primary_ref=sw.ref, one_liner=sw.one_liner, paid=sw.paid, remarks=sw.remarks)

@biodb.route('/software/<sw_id>', methods = ['POST'])
def update_software_detail(sw_id):

    pass