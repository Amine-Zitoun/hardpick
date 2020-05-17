
import requests
import os
from bs4 import BeautifulSoup as bs
from formattors import *

def search_intense(key,l):
	print("zbi?")
	c = 0
	if ''.join(key.split(' ')) in [''.join(i.split('@')[0].split(' ')) for i in l]:
		for i in l:
			if ''.join(i.split('@')[0].split(' ')) == ''.join(key.split(' ')):
				return i
			else:
				pass
	else:
		for i in l:
			#print("CHECKING "+key+" with "+i)
			print("checking ",i,"with ",key)
			if key in i:
				#print("CHECKING "+key+" with "+i)
				print('FOUND MATCH')
				return i
			else:
				pass
		return "not found"


def benchmark(c1,c2,comp):
	print(c1,c2)
	if comp == "gpu":
		# GET ALL THE PARTS FROM THE LEADERBOARD

		url = "https://www.videocardbenchmark.net/high_end_gpus.html"
		res = requests.get(url)
		html = bs(res.text,'lxml')
		parts = [(x.text).lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]

		final_res = dict(zip(parts,points))

		# FORMATS THE NAME OF THE PRODUCT 
		print("[*] FOUND ON SITE: "+c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'))
		if c1['pr'] == "higher":
			vl1 = 0
		else:
			key1 = gpu_val(c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c1['site'])

			print("[*] TURNED IT INTO: "+key1)
			#print(parts)

			# searches in the learderboard

			res1= search_intense(key1.lower(),parts)
			print("[*] CHCKED ON DB AND FOUND: "+res1)

			# gets value
			if res1 == "not found":	
				vl1=0
			else:
				vl1 = final_res[res1]
		#same process for 2
		if c2['pr'] == "higher":
			vl2 = 0
		else:
			key2 = gpu_val(c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c2['site'])
			print("[*] TURNED IT INTO: "+key2)
			print(parts)
			res2= search_intense(key2.lower(),parts)
			print("[*] CHCKED ON DB AND FOUND: "+res2)
			if res2 == "not found":	
				vl2=0
			else:
				vl2 = final_res[res2]

		#compares values

		if vl1 >= vl2:
			return c1
		else:
			return c2


	elif comp == "cpu":
		url = "https://www.cpubenchmark.net/high_end_cpus.html"
		#print(url)
		# GET ALL THE PARTS FROM THE LEADERBOARD


		res = requests.get(url)
		html = bs(res.text,'lxml')
		parts = [(x.text).lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]
		final_res = dict(zip(parts,points))


		# FORMATS THE NAME OF THE PRODUCT 
		if c1['pr'] == "higher":
			vl1 = 0
		else:
			key1 = cpu_formattor(c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c1['site'])
			print("[*]  FOUND ON SITE: "+c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'))
			print("[*] TURNED IT INTO: "+key1)
			res1= search_intense(key1.lower(),parts)
			print("[*] CHCKED ON DB AND FOUND: "+res1)
			# gets value
			if res1 == "not found":	
				vl1=0
			else:
				vl1 = final_res[res1]

		# same process
		if c2['pr'] == "higher":
			vl2 = 0
		else:
			key2 = cpu_formattor(c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c2['site'])
			print("[*]  FOUND ON SITE: "+c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'))
			print("[*] TURNED IT INTO: "+key2)
			print(parts)
			res2= search_intense(key2.lower(),parts)
			print("[*] CHCKED ON DB AND FOUND: "+res2)
			if res2 == "not found":	
				vl2=0
			else:
				vl2 = final_res[res2]

		# compares vls
		if vl1 >= vl2:
			return c1
		else:
			return c2

		
	
	elif comp == "ram":
		# gets ram data from both
		if c1['pr'] == "lower":
			frq1 = int(c1['frq'])
			cap1 = int(c1['cap'])
			typem1 = c1['typem']
		else:
			frq1 = 0
			cap1=0
			typem1="DDR0"


		if c2['pr'] == "lower":
			frq2 = int(c2['frq'])
			cap2 = int(c2['cap'])
			typem2 = c2['typem']
		else:
			frq2 = 0
			cap2=0
			typem2="DDR0"

		pt1=0
		pt2=0
		# compares data

		if frq1 > frq2:
			pt1 += 1
		elif frq1 < frq2:
			pt2 += 1
		else:
			pass

		if cap1 > cap2:
			pt1 += 1
		elif cap1 < cap2:
			pt2 += 1
		else:
			pass

		if int(typem1[-1]) > int(typem2[-1]):
			pt1 += 1
		elif int(typem1[-1]) < int(typem2[-1]):
			pt2 += 1
		else:
			pass

		# compares vls
		if pt1 >= pt2:
			return c1
		else:
			return c2
