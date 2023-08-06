#!/usr/bin/env python
from __future__ import print_function

from configset import configset
import requests
import platform as plat
import argparse
import sys
import os
from make_colors import make_colors
from pydebugger.debug import debug
try:
	from . import downloader as dwn
except:
	import downloader as dwn
import pheader
from bs4 import BeautifulSoup as bs
import re
if sys.version_info.major == 3:
	raw_input = input
# import random
from pprint import pprint
try:
	from pause import pause
except:
	def pause(*args, **kwargs):
		return None

class Odoo_downloader(object):
	URL = ""
	configname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'odoo_downloader.ini')
	CONFIG = configset(configname)
	session = requests.Session()

	def __init__(self):
		super(Odoo_downloader, self)

	@classmethod
	def format_number(self, number, length = 10):
		number = str(number).strip()
		if not str(number).isdigit():
			return number
		zeros = len(str(length)) - len(number)
		r = ("0" * zeros) + str(number)
		if len(r) == 1:
			return "0" + r
		return r

	@classmethod
	def get(self, system = None, version = None, dtype = 'community'):
		platforms = {}
		if version: version = str(version)
		if system:
			if 'linux' in system:
				system = list(filter(None, plat.linux_distribution() or (plat.system(), )))[0]
			debug(system = system)
			#pause()
			if (not 'debian' in system.lower() and not 'debian' in system.lower() and not 'window' in system.lower()) or 'linux' in system or 'arc' in system or 'arm' in system or 'darwin' in system or 'mac' in system:
				system = 'Sources'
			elif 'red' in system or'slax' in system:
				system = 'RPM'
		debug(system = system)
		# pause()

		data = {}
		url1 = "https://www.odoo.com/id_ID/page/download"
		url2 = "https://www.odoo.com/id_ID/thanks/download"
		b = None

		headers = pheader.set_header(accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", Sec_Fetch_Mode= "navigate")
		debug(headers = headers)
		a = self.session.get(url1, headers = headers)
		content = a.content
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'get1.html'), 'wb') as f: f.write(content)
		b = bs(content, 'lxml')
		
		card_platforms = b.find_all('div', {'class':'card mt64'})
		for card in card_platforms:
			debug(card = card)
			title = card.find('table').find('thead').find('th', {'width':"15%",'class':'border-top-0'}).text
			debug(title = title)
			# if title: title.text
			table = card.find('table')
			debug(table = table)
			all_tr = table.find_all('tr')
			add = {}
			for tr in all_tr[1:]:
				platform_string = tr.find('td', {'class':'o-v-middle fw_medium'}).text
				debug(platform_string = platform_string)
				# platform = {data_platform_string[data_platforms.index(i)].text : i.get('value') for i in data_platform}
				platform = tr.find('button', {'name':'platform_version'}).get('value')
				debug(platform = platform)
				platform_ent = tr.find('a', {'data-target':'#oe_download_modal'}).get('data-platform-version')
				debug(platform_ent = platform_ent)
				add.update({platform_string: {'community': platform, 'enterprise': platform_ent}})
				debug(add = add)
			platforms.update({title: add})
		debug(platforms = platforms)	
		if os.getenv('DEBUG') or os.getenv('DEBUG_SERVER'):
			pprint(platforms)
	
		data_q = []		
		n = 1
		bg = ['lg', 'ly', 'lc', 'r', 'bl']
		if not version:
			for p in platforms:
				print(make_colors(p, 'b', 'lc') + ":")
				for pp in platforms.get(p):
					print(" " * 2 + make_colors(pp, 'b', 'lg') + ":")
					for ppp in platforms.get(p).get(pp):
						print(" " * 4 + make_colors(self.format_number(n) + ".") + " " + make_colors(ppp, 'lg'))
						n+= 1
						data_q.append(platforms.get(p).get(pp).get(ppp))
				
			q = raw_input(make_colors("Select dtype of Operation System:", 'lw', 'r') + " ")
			if q:
				q = q.strip()
			if q.isdigit():
				version = data_q[int(q) - 1]
			elif q in ["exit", 'x', 'q', 'quit']:
				sys.exit(make_colors("system exit !",'lw', 'r'))
		else:
			data_version = None
			data_system = None
			data_dtype = None
			data_version = list(filter(lambda k: str(version).lower() in k.lower() or k.lower() in str(version).lower(), [p for p in platforms]))
			debug(data_version = data_version)
			#pause()
			debug(system = system)
			debug(data_version = data_version)
			if data_version:
				debug(system = system)
				data_system = list(filter(lambda k: str(system).lower() in k.lower() or k.lower() in str(system).lower(), platforms.get(data_version[0]).keys()))
				if data_system:
					system = data_system[0]
					debug(system = system)
				else:
					system = list(filter(None, plat.linux_distribution() or (plat.system(), )))[0]
					debug(system = system)
			if system and data_version:
				try:
					data_system = list(filter(lambda k: str(system).lower() in k.lower() or k.lower() in str(system).lower(), platforms.get(data_version[0]).keys()))
				except:
					data_system = list(filter(lambda k: system in k or k in system, platforms.get(data_version[0]).keys()))
				system = data_system[0]
			debug(system = system)
			# pause()
			dtype = dtype or "community"
			debug(data_system = data_system)
			debug(data_version = data_version)
			debug(dtype = dtype)
			if system and data_version and dtype:
				debug(test = platforms.get(data_version[0]).get(data_system[0]).keys())	
				debug(dtype = dtype)
				data_dtype = list(filter(lambda k: str(dtype).lower() in k.lower() or k.lower() in str(dtype).lower(), platforms.get(data_version[0]).get(data_system[0]).keys()))
				debug(data_dtype = data_dtype)
				#pause()
				debug(data_dtype = data_dtype)
				#pause()
				if data_dtype:
					data_dtype = data_dtype[0]
					version = platforms.get(data_version[0]).get(data_system[0]).get(data_dtype)
					debug(version = version)
					#pause()		
				else:
					version = None
			debug(version = version)
			#pause()
				
		debug(version = version)
		#pause()

		if not version and not data_version:
			debug(system = system)
			if system:
				data_system = list(filter(lambda k: str(system).lower() in k.lower() or k.lower() in str(system).lower(), platforms.get(max(platforms.keys())).keys()))
				if data_system:
					system = data_system
				debug(systemx = system)
			else:
				system = list(filter(None, plat.linux_distribution() or (plat.system(), )))
			debug(systemx = system)
			# print("SYSTEM:", system)
			# print("DATA SYSTEM:", data_system)
			debug(data_system = data_system)
			#pause()
			
			if system:
				for p in platforms.get(max(platforms.keys())).keys():
					for k in system:
						if k.lower() in p.lower() or p.lower() in k.lower():
							data_system = p
							break
					if data_system:
						break
			debug(data_system = data_system)
			version = platforms.get(max(platforms.keys())).get(data_system[0]).get('community')
			debug(version = version)
		debug(version = version)
		#pause()

		form = b.find('form', {'class':'form-horizontal mb32'})
		debug(form = form)
		inputs = form.find_all('input', {'type':'hidden'})
		debug(inputs = inputs)
		data = {i.get('name'): i.get('value') for i in inputs}
		debug(data = data)
		# {'csrf_token': '39cefa951ba6668f805b917221028252712c4dc8o1671458605', 'team_id': '-1', 'force_scope': 'x_Download', 'description': 'Download'}

		data.update({
			'partner_name':     'cumulus13',
			'contact_name':     'cumulus13',
			'phone':            '+6285795023412',
			'email_from':       'cumulus13@gmail.com',
			'plan':             'plan_to_use',
			'company_size':     '1-5',
			'platform_version': version,
		})
		debug(data = data)
		# sys.exit()
		a1 = self.session.post(url2, data = data)
		content1 = a1.content
		b1 = bs(content1, 'lxml')
		script = b1.find('script', text = re.compile("download.odoocdn.com/download"))
		debug(script = script)
		url_download = None
		if script:
			url_download = re.findall("window.location.assign\('(.*?)'\)", script.text)
		debug(url_download = url_download)
		if url_download:
			return url_download[0], system, version, dtype
		return '', system, version, dtype

	@classmethod
	def download(self, download_path = None, system = None, version = None, dtype = 'community', saveas = None, downloader = 'wget', nodownload = False):
		download_path = download_path or os.getcwd()
		debug(system = system)
		debug(version = version)
		debug(dtype = dtype)
		url_download, system, version, dtype = self.get(system, version, dtype)
		debug(system = system)
		debug(version = version)
		debug(dtype = dtype)
		debug(url_download = url_download)
		debug(saveas = saveas)
		if not url_download:
			print(make_colors("No URL Download !", 'lw', 'r'))
			return False
		if not saveas and system and version:
			ext = ""
			if 'deb' in system.lower() or 'ubuntu' in system.lower():
				ext = ".deb"
			elif 'rpm' in system.lower():
				ext = ".rpm"
			elif 'source' in system.lower():
				ext = ".tar.gz"
			elif 'window' in system.lower():
				ext = ".exe"
			saveas = "Odoo" + "-" + version + "-" + system + "-" + dtype + ext
			debug(saveas = saveas)
		
		print(make_colors("GENERATED", 'b', 'lg') + "    : " + make_colors(url_download, 'ly'))
		print(make_colors("DOWNLOAD_PATH:", 'b', 'lc') + " " + make_colors(download_path, 'lc'))
		# pause()
		if not nodownload:
			dwn.download(url_download, self.CONFIG, download_path, saveas, downloader = downloader)
		return True


	@classmethod
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
		parser.add_argument('-o', '--platform', help = "Operation System type, valid is: 'ubuntu | debian | windows | rpm | source | linux', default is current platform", action = 'store')
		parser.add_argument('-v', '--version', help = "Odoo version, valid is >= 12", action = 'store')
		parser.add_argument('-t', '--type', help = "Odoo type, valid is 'community | enterprise', default is 'community'", action = 'store', default = 'community')
		parser.add_argument('-p', '--download-path', help = 'Save download to dir', action = 'store')
		parser.add_argument('-s', '--save-as', help = 'Save as name, default is base on platform type and version', action = 'store')
		parser.add_argument('-d', '--downloader', help = 'Download app, valid is: "wget | aria2c | persepolis" default is wget but if wget not installed then default is pywget', action = 'store', default = 'wget')
		parser.add_argument('-nd', '--no-download', action = 'store_true', help = 'Don\'t Download just generate it only')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			self.download(args.download_path, args.platform, args.version, args.type, args.save_as, args.downloader, args.no_download)

def usage():
	return Odoo_downloader.usage()

if __name__ == '__main__':
	# def get(self, system = None, version = None, dtype = 'cummunity'):
	# Odoo_downloader.get(system = "linux", version = 16, dtype = 'enterprise')
	Odoo_downloader.usage()