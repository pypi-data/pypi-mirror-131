import os, sys
import bitmath
import traceback
import subprocess
import clipboard
from unidecode import unidecode
import re
from make_colors import make_colors
from pydebugger.debug import debug
from datetime import datetime

def logger(config, message, status="info"):
	logfile = os.path.join(os.path.dirname(__file__), os.path.splitext(os.path.basename(config.configname))[0] + '.log')
	if not os.path.isfile(logfile):
		lf = open(logfile, 'wb')
		lf.close()
	real_size = bitmath.getsize(logfile).kB.value
	max_size = config.get_config("LOG", 'max_size')
	debug(max_size = max_size)
	if max_size:
		debug(is_max_size = True)
		try:
			max_size = bitmath.parse_string_unsafe(max_size).kB.value
		except:
			max_size = 0
		if real_size > max_size:
			try:
				os.remove(logfile)
			except:
				print("ERROR: [remove logfile]:", traceback.format_exc())
			try:
				lf = open(logfile, 'wb')
				lf.close()
			except:
				print("ERROR: [renew logfile]:", traceback.format_exc())

	str_format = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S.%f") + " - [{}] {}".format(status, message) + "\n"
	if sys.version_info.major == 3:
		with open(logfile, 'ab') as ff: ff.write(bytes(str_format, encoding='utf-8'))
	else:
		with open(logfile, 'ab') as ff: ff.write(str_format)

def download(url, config, download_path=os.getcwd(), saveas=None, headers = {}, downloader = 'wget'):

	if not download_path or not os.path.isdir(download_path):
		if config.get_config('DOWNLOAD', 'path', os.getcwd()):
			download_path = config.get_config('DOWNLOAD', 'path')

	print(make_colors("DOWNLOAD_PATH (linux):", 'lw', 'bl') + " " + make_colors(download_path, 'b', 'ly'))

	if sys.version_info.major == 3:
		aria2c = subprocess.getoutput("aria2c")
		wget = subprocess.getoutput("wget")
		persepolis = subprocess.getoutput("persepolis --help")
	else:
		aria2c = os.popen3("aria2c")[2].read()
		wget = os.popen3("wget")[2].read()
		persepolis = os.popen3("persepolis --help")[2].read()
    			
	if downloader == 'aria2c' and not re.findall("not found\n", aria2c):
		if saveas:
			saveas = '-o "{0}"'.format(saveas.encode('utf-8', errors = 'ignore'))
		cmd = 'aria2c -c -d "{0}" "{1}" {2} --file-allocation=none'.format(os.path.abspath(download_path), url, saveas)
		logger(config, "[aria2c] DOWNLOADING: {} --> {}".format(url, os.path.join(download_path, saveas)))
		os.system(cmd)
		logger(config, "[aria2c] DOWNLOADED: {} --> {}".format(url, os.path.join(download_path, saveas)))
	elif downloader == 'wget' and not re.findall("not found\n", wget):
		if saveas:
			try:
				saveas = ' -O "{}"'.format(os.path.join(os.path.abspath(download_path), saveas.decode('utf-8', errors = 'ignore')))
			except:
				saveas = ' -O "{}"'.format(os.path.join(os.path.abspath(download_path), unidecode(saveas)))
		else:
			saveas = '-P "{0}"'.format(os.path.abspath(download_path))

		headers_download = ''
		if headers:
			for i in headers: header +=str(i) + "= " + headers.get(i) + "; "
			headers_download = ' --header="Cookie: ' + header[:-2] + '"'

		cmd = 'wget -c "{}" {}'.format(url, saveas) + headers_download
		# cmd = 'wget -c "{}" {}'.format(url, saveas)
		print(make_colors("CMD:", 'lw', 'lr') + " " + make_colors(cmd, 'lw', 'r'))
		logger(config, "[wget] DOWNLOADING: {} --> {}".format(url, os.path.join(download_path, saveas)))
		os.system(cmd)
		logger(config, "[wget] DOWNLOADED: {} --> {}".format(url, os.path.join(download_path, saveas)))
	elif downloader == 'persepolis'  and not re.findall("not found\n", persepolis):
		cmd = 'persepolis --link "{0}"'.format(url)
		logger(config, "[persepolis] DOWNLOADING: {} --> {}".format(url, os.path.join(download_path, saveas)))
		os.system(cmd)
		logger(config, "[persepolis] DOWNLOADED: {} --> {}".format(url, os.path.join(download_path, saveas)))
	else:
		try:
			from pywget import wget as d
			logger(config, "[pywget] DOWNLOADING: {} --> {}".format(url, os.path.join(download_path, saveas)))
			d.download(url, download_path, saveas.decode('utf-8', errors = 'ignore'))
			logger(config, "[pywget] DOWNLOADED: {} --> {}".format(url, os.path.join(download_path, saveas)))
		except:
			print(make_colors("Can't Download this file !, no Downloader supported !", 'lw', 'lr', ['blink']))
			clipboard.copy(url)
			logger(config, "COPY TO CLIPBOARD: {}".format(url))
