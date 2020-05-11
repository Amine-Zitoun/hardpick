
import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from parsers import *
from formattors import *
from benchmark import *


app = Flask(__name__)
app.debug = True
api = Api(app)




@app.route('/api/',methods=['GET'])
def res():
	comp= request.args.get('comp',None)
	budget = request.args.get('budget',None)
	print(comp,budget)
	# Searches for mega pc 
	mega = search_megapc(comp,budget)
	mega_prd= mega['prd'].encode('ascii', 'ignore').decode('unicode_escape')

	# Searches for sbs 
	sbs = search_sbs(comp,budget)
	sbs_prd =sbs['prd'].encode('ascii', 'ignore').decode('unicode_escape')
		
	# Search extreme
	extrme = search_extreme(comp,budget)
	extrme_prd =extrme['prd'].encode('ascii', 'ignore').decode('unicode_escape')
	
	# Search tunisianet
	tn = search_tunisia(comp,budget)
	tn_prd =tn['prd'].encode('ascii', 'ignore').decode('unicode_escape')


	win1 = benchmark(sbs,tn,comp)
	win2 = benchmark(mega,extrme,comp)

	final = benchmark(win1,win2,comp)
	result = {'data': [mega,sbs,extrme,tn],'win': final}
	return jsonify(result)


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"
if __name__ == "__main__":
	app.run(port='5000')
