#!/usr/bin/env python
# -*- coding: utf-8 -*-
#.--. .-. ... .... -. - ... .-.-.- .. -.

import json

from bson.objectid import ObjectId
from flask import Flask, Blueprint, render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from sdk.user import model as user_model
from . import model as biodb_model

from sdk.utils import validate_oid, get_fasta_seq


biodb = Blueprint('biodb', __name__, template_folder='templates')

@biodb.route('/')
def get():
	return "Test"

@biodb.route('/add', methods = ['POST'])
def add():
	# Get form data as an ImmutableMultiDict.
	sw=request.form
	#if biodb_model.Manage().add(sw.get('software_name', type=str), sw.get('tags', type=str).split(','), sw.get('primary_link', type=str), sw.get('one_liner', type=str), True if sw.get('paid', type=str) == 'P' else False):
	#    response = {
	#        'status' : 'ok',
	#        'message' : 'hello there'
	#    }
	#    return jsonify(response), 200
	#else:
	#    response = {
	#        'status' : 'not ok',
	#        'message': 'not working'
	#    }
	#    return jsonify(response), 200


@biodb.route('/cell', methods = ['GET'])
def gets():
	return render_template('index.html')

@biodb.route('/cell/<oid>', methods = ['GET'])
@validate_oid
def get_cell_detail(oid):
	
	cell = biodb_model.Cell(oid)
	if cell.k is True:
		cell_dict = {
		"Cell Name: ": cell.name,
		"Location: ": cell.location,
		"Shape: ": cell.shape,
		"Dimensions: ": cell.dimensions,
		"Function: ": cell.function,
		"Comments: ": cell.comments,
		"Image: ": str(cell.imageURL),
		"Fasta Sequence: ": get_fasta_seq("ANK1")
		}
		return render_template('cell.html', cell_dict=cell_dict)
	else:
		return render_template('404.html'), 404
	

@biodb.route('/cell/<c_id>', methods = ['POST'])
def update_software_detail(sw_id):

	pass

@biodb.route('/search/<query_string>', methods=['POST'])
def search_query(query_string):
	"""Renders the search page with results based on the search query"""
	field = request.args.get('field', 'cell_name')
	results = { "results": biodb_model.Manage().search(query_string, field) }
	return jsonify(results), 200