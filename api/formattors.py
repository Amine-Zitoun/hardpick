
import requests
import os
from bs4 import BeautifulSoup as bs



def ram_formattor(url,site):
	if site == "sbs":
		s = requests.get(url)
		html = bs(s.text,'lxml')
		desc = html.find_all('div',{'class': 'descriptonProd'})
		#print(len(desc))
		#print("=======================================")
		caps = []
		typems = []
		freqs= []

		for t in desc:

			for f in t.findChildren('p',recursive=False):
				
				#print(f.text.split("Fréquence"))
				if len(f.text.split('mémoire')) > 1:
					
					#print(f.text.split('mémoire')[1].split(' ')[2].split('\n')[0])
					typems.append(f.text.split('mémoire')[1].split(' ')[2].split('\n')[0].split('\r')[0])
				if len(f.text.split('Capacité')) > 1:
					
					#print(f.text.split('Capacité')[1].split(' ')[2].split('\n')[0])
					caps.append(int(f.text.split('Capacité')[1].split(' ')[2].split('\n')[0]))
				if len(f.text.split('Fréquence')) > 1:
					freqs.append(int(f.text.split('Fréquence')[1].split(' ')[2].split('\n')[0]))
					#print(f.text.split('Fréquence')[1].split(' ')[2].split('\n')[0])


		return caps,typems,freqs
	elif site == "mega":
		# parse all products and according prices
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)
		all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		caps = []
		typems = []
		freqs= []
		for s in all_comp:
			
			print("testing on "+s)
			count = 0

			capd=None
			freqd=None
			typemd=None

			if s.split(' ')[0].lower() == "corsair" and s.split(' ')[3][0] != "8":
				if s.split(' ')[2].lower() == "lpx":
					capd=1
					typemd=6
					freqd=7
				elif s.split(' ')[2].lower() == "rgb":
					if s.split(' ')[4][0] == "3":
						caps.append(32)
						freqs.append(3000)
						typems.append("DDR4")
						pass
					else:
						capd=1
						typemd=5
						freqd=6
			elif s.lower().startswith('gigabyte aorus'):
				capd=2
				typemd=1
				freqd=6
			elif s.lower().startswith('patriot'):
				capd=1
				typemd=5
				freqd=6
			elif s.lower().startswith('g.skill'):
				capd=1
				typemd=5
				freqd=6
			else:
				capd=1
				typemd=4
				freqd=5



			#print(s.lower().startswith('patriot'))

			print(capd,typemd,freqd)
			cap=None
			typem=None
			frq=None
			#print(typemd)
			for i in s:
				if i.isdigit():
					count += 1
					if count == capd:
						if s[s.index(i)+1] == "G":
							caps.append(int(i))
						elif s[s.index(i)+1] != "G":
							caps.append(int(i+''+s[s.index(i)+1]))
						#print("IMPORTANT ON "+i)
					elif count == typemd:
						typems.append("DDR"+i)
					elif count == freqd:
						print(count)
						print(s.index(i))
						print(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3])
						freqs.append(int(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3]))
		print( caps,typems,freqs)
		return caps,typems,freqs
	if site == "extreme":
		res = requests.get(url)
		caps = []
		typems = []
		freqs= []
		html = bs(res.text,'lxml')
		#print(html)
		#all_comp = [x.text.encode('ascii', 'ignore').decode('unicode_escape') for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		products=[]
		s = html.find_all('div',{'id': "tab-ram"})
		for x in s:
			prd = x.find_all('h2')
		#price = x.find_all('span',{'class': 'woocommerce-Price-amount amount'})
			for p in prd:
				products.append(p.text.encode('ascii', 'ignore').decode('unicode_escape'))

		for i in products:
			print("vengeance" == i.lower().split(' ')[0],i.lower().split(' ')[0])
			if "pny" in i.lower() and "8" in i.lower():
				caps.append(8)
				typems.append("DDR4")
				freqs.append(2666)

			elif i.lower().split(' ')[0] == "vengeance":
				if "3000Mhz" in i.lower():
					caps.append(16)
					freqs.append(3000)
					typems.append("DDR4")
				else:
					caps.append(16)
					freqs.append(3200)
					typems.append("DDR4")
			elif i.startswith("16"):
				caps.append(16)
				freqs.append(2666)
				typems.append("DDR4")
			else:
				caps.append(8)
				freqs.append(3000)
				typems.append("DDR4")

		print( caps,typems,freqs)
		return caps,typems,freqs
	if site == "tunisia":
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)

		#s = html.find_all('h2',{'class': 'h3 product-title'})
		temp=[[y.text for y in x.findChildren('a',recursive=False)] for x in html.find_all('h2',{'class': 'h3 product-title'})]
		#print(s)
		all_comp = [x[0] for x in temp]
		#print(all_comp[:-2])
		caps = []
		typems = []
		freqs= []
		capd=1
		freqd=3
		typemd=2

		for s in all_comp[:-1]:
			print(s)
			count = 0
			for i in s:
				print(i)
				if i.isdigit():
					count += 1
					if count == capd:
						if s[s.index(i)+1] == "G":
							caps.append(int(i))
						elif s[s.index(i)+1] != "G":
							caps.append(int(i+''+s[s.index(i)+1]))
						#print("IMPORTANT ON "+i)
					elif count == typemd:
						typems.append("DDR"+i)
					elif count == freqd:
						print(count)
						print(s.index(i))
						print(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3])
						freqs.append(int(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3]))
			print(freqs,typems,caps)
		caps.append(16)
		freqs.append(3000)
		typems.append("DDR4")
		#print(all_comp)
		print(len(caps),len(all_comp))
		return caps,typems,freqs

def cpu_formattor(cpu,site):
	word= cpu.split(' ')
	if site == "sbs" or site == "mega":
		if cpu[0].lower() == "p":
			res_word=word[1:]
		else:
			res_word = word
		print(res_word[2])
		if res_word[0].lower() == "intel":
			key = res_word[0] +' '+ res_word[1] +' '+ res_word[2] 
		elif res_word[0].lower() == "amd":
			key = res_word[0] + ' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		return key
	if site == "extreme":
		res_word = word
		if res_word[0].lower() == "amd":
			key = cpu.lower()
		if res_word[0].lower() == "cpu":
			key = res_word[1]+' '+'core'+' '+res_word[2]+'-'+res_word[3]
		if res_word[0].lower() == "intel":
			if res_word[1].lower() == "i9":
				key = res_word[1]+'-'+res_word[2]
			else:
				key = cpu.lower().split('-')[0]+cpu.lower().split('-')[1]+cpu.lower().split('-')[2]
		if res_word[0].lower().startswith('pent'):
			key = cpu.lower()
		if res_word[0].lower().startswith('ry'):
			key = "amd"+' '+cpu.lower()
		if res_word[0].lower().startswith('pro'):
			key = ' '.join(res_word[1:])
		return key
	if site == "tunisia":
		word = cpu.split(' ')
		res_word = word[1:]
		if res_word[0].lower() == "intel":
			if res_word[1].lower() == "core":
				if res_word[2].lower().startswith('c'):
					key = res_word[0] + ' '+res_word[1] + ' '+res_word[4]
				else:
					key = res_word[0] + ' '+res_word[1]+ ' '+res_word[2]
			else:
				key= "idk"

		if res_word[0].lower() == "amd":
			if res_word[2].lower() == "tm":
				key = res_word[0]+ ' '+res_word[1]+ ' '+res_word[3]+ ' '+res_word[4]
			else:
				key = res_word[0]+ ' '+res_word[1]+ ' '+res_word[2]+ ' '+res_word[3]
		return key

	#return res_cpu.lower()

def gpu_val(gpu,site):
	#print("\n\n\n\n"+gpu+"\n\n\n")
	res_gpu = ''
	arr = gpu.split(' ')
	if site == "sbs":
		word = gpu.split(' ')
		#for i in word:
		res_word = word[2:]
		if res_word[0] == "Palit":
			if res_word[1] == "GeForce":
				if res_word[2] == "GT":
					key = res_word[2]+' '+res_word[3]
				elif res_word[2] == "RTX":
					key = res_word[2]+' '+res_word[3]+' '+res_word[4]
			elif res_word[1] == "RTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			elif  res_word[1] == "GT":
				key = res_word[1]+' '+res_word[2]
			elif res_word[1] == "GTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
		elif res_word[0] == "MSI":
			if res_word[1] == "GeForce":
				if res_word[2] == "GT":
					key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
			elif res_word[1] == "GTX":
				key = res_word[1]+' '+res_word[2]+' '
				if res_word[3] == "SUPER":
					key += res_word[3]
			elif res_word[1] == "Radeon":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			elif res_word[1] == "RTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
		elif res_word[0] == "ASUS":
			if res_word[1].lower() == "rog":
				if res_word[2].lower() == "strix":
					if res_word[3].lower()[:2] == "RX":
						key = res_word[3]
					else:
						key = res_word[3] + ' '+res_word[4] + ' '+res_word[5]
			elif res_word[1].lower() == "tuf":
				if c:
					key  = res_word[2] + ' '+res_word[3]+' '+res_word[4]
				elif res_word[2].lower() == "3-":
					key = res_word[3]
			elif res_word[1].lower() == "gtx":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
	if site == "mega":
		word = gpu.split(' ')
		res_word = word[1:]

		if res_word[3].lower() == "super":
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		else:
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]
		return key.lower()
	if site == "extreme":
		res_word = gpu.split(' ')
		if res_word[0].lower() == "geforce":
			if res_word[1].lower() == "rtx":
				if res_word[3].lower() == "super" or res_word[3].lower() == "ti":
					key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[0]+' '+res_word[1]+' '+res_word[2]
			elif res_word[1].lower() == "gt":
				key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gtx":
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gtx1660":
			key = "gtx 1660"
		if res_word[0].lower() == "pny":
			if res_word[1].lower() == "1660":
				key = "gtx 1660 super"
			else:
				key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		if res_word[0].lower() == "msi":
			key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "asus":
			key = res_word[2]
		return key
	if site == "tunisia":
		word =gpu.split(' ')
		res_word =word[2:]
		print(res_word)
		if res_word[0].lower() == "palit":
			if res_word[1].lower() == "geforce":
				if res_word[2].lower() == "gt":
					key = res_word[2] + ' '+res_word[3]
				elif res_word[2].lower() == "gtx":
					if res_word[4].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
					else:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key =res_word[1]+' '+res_word[2]
			elif res_word[1].lower() == "gtx":
				if res_word[3].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
						key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gigabyte":
			if res_word[1].lower() == "geforce":
				if res_word[2].lower() == "gtx":
					if res_word[4].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
					else:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[1]+' '+res_word[2]
			if res_word[1].lower() == "gtx": 
				if res_word[3].lower() in ['ti','super']:
					key = res_word[1]+' '+res_word[2]+' '+res_word[3] 
				else:
					key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "msi":
			if res_word[1].lower() == "geforce":
				if res_word[4].lower() in ['ti','super']:
					key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
				else:
					key =res_word[1]+' '+res_word[2]+' '+res_word[3]
			if res_word[1].lower() == "radeon":
				key =res_word[1]+' '+res_word[2]+' '+res_word[3]
			if res_word[1].lower() == "gtx":
				key =res_word[1]+' '+res_word[2]+' '+res_word[3]
		if res_word[0].lower() == "asus":
			if res_word[1].lower() == "geforce":
				key =res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
			else:
				key ="radeon rx 5700 xt"
		return key


			
