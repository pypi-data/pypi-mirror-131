Command line Odoo Downloader
----------------------------------
Command line for download odoo installer or source

Author
---------
[Hadi Cahyadi @cumulus13 team](cumulus13@gmail.com)

Requirements
--------------
- configset
- requests
- make_colors
- pydebugger
- pheader
- bs4
- bitmath
- clipboard
- unidecode
- pywget

Usage
----------
```bash:
$ odoo_downloader -h
  usage: odoo_downloader.py [-h] [-o PLATFORM] [-v VERSION] [-t TYPE]
                          [-p DOWNLOAD_PATH] [-s SAVE_AS] [-d DOWNLOADER]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o PLATFORM, --platform PLATFORM
	                        Operation System type, valid is: 'ubuntu | debian | windows | rpm | 
	                        source | linux', default is current platform
	  -v VERSION, --version VERSION
	                        Odoo version, valid is >= 12
	  -t TYPE, --type TYPE  Odoo type, valid is 'community | enterprise', default is 'community'
	  -p DOWNLOAD_PATH, --download-path DOWNLOAD_PATH
	                        Save download to dir
	  -s SAVE_AS, --save-as SAVE_AS
	                        Save as name, default is base on platform type and version
	  -d DOWNLOADER, --downloader DOWNLOADER
	                        Download app, valid is: "wget | aria2c | persepolis" default is wget 
	                        but if wget not installed then default is pywget
 	  -nd, --no-download    Don't Download just generate it only

$ #example:
$ odoo_downloader -o ubuntu -v 14 -t enterprise -p /home/cumulus13/Download -d aria2c
```

```python:
>> from odoo_downloader import Odoo_downloader as downloader
>> downloader.download("/home/cumulus13/Download", 'windows', '14', 'community', downloader = 'aria2c')
   GENERATED    : https://download.odoocdn.com/download/14/exe?payload=MTYzOTk5NDE2OC4xNC5leGUuQk5MVmFsWlZMWkJiTngxNklTMXVsR2QxVlk0VFVGTkd1UlBhWWQ0SEZKYz0%3D
   DOWNLOAD_PATH: /mnt/licface/f/DOWNLOADS
   DOWNLOAD_PATH (linux): /home/cumulus13/Download
>> #or just
>> downloader.download("/home/cumulus13/Download")
   GENERATED    : https://download.odoocdn.com/download/14/deb?payload=MTYzOTk5NTM3Ni4xNC5kZWIuUDBlOVU4UUc1TnY5U0szUUxpSzJ6azlVS3M1WE9qdXBPaGZDMG1CajV0OD0%3D
   DOWNLOAD_PATH: /mnt/licface/f/DOWNLOADS
   DOWNLOAD_PATH (linux): /home/cumulus13/Download

```

Donate
----------
[Paypal]("paypal.me/licface13")

