# This is a skeleton for Err plugins, use this to get started quickly.

from errbot import BotPlugin, botcmd
import re
import requests
import xml.etree.ElementTree as etree

class Orrrrr(BotPlugin):
	"""Orrrrr recursive^3 recursor"""
	min_err_version = '1.6.0' # Optional, but recommended
	max_err_version = '2.0.0' # Optional, but recommended

	# Passing split_args_with=None will cause arguments to be split on any kind
	# of whitespace, just like Python's split() does
	@botcmd(split_args_with=None)
	def orrrrr(self, mess, args):
		"""A command that looks up acronyms at the Internet Acronym Server ( http://acronyms.silmaril.ie )"""
		p = re.compile('.*[^a-zA-z\\.].*')
		if len(args) > 1:
			return "Sorry, acronyms may not contain spaces."
		elif p.match(args[0]):
			return "Sorry, nothing but letters and dots is allowed in an acronym."
		else:
			r = requests.get("http://acronyms.silmaril.ie/cgi-bin/uncgi/xaa?" + args[0].strip("."))
			element = etree.fromstring(r.text)
			if int(element.find('found').attrib['n']) > 0:
				return next(element.iter('acro')).find('expan').text
			else:
				return "Didn't find any definitions, sorry."
		return "Whoa, something broke O_O"