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
		if len(args) > 1:
			return "Sorry, acronyms may not contain spaces."
		elif not self.input_valid(args[0]):
			return "Sorry, nothing but letters and dots is allowed in an acronym."
		else:
			self.send(mess.getFrom(), "Thinking...", message_type=mess.getType())
			self.lookup_stack(args[0], mess.getFrom(), mess.getType())
			return
		return "Whoa, something broke O_O"
	
	def input_valid(self, input):
		p = re.compile('.*[^a-zA-z\\.].*')
		return not p.match(input)

	@botcmd(split_args_with=None)
	def acro(self, mess, args):
		if len(args) > 1:
			return "Sorry, acronyms may not contain spaces."
		elif not self.input_valid(args[0]):
			return "Sorry, nothing but letters and dots is allowed in an acronym."
		else:
			ret = args[0] + ": "
			expanded = self.lookup_acro(args[0])
			if len(expanded) > 0:
				ret += expanded
			else:
				ret += "-"
		return ret


	def lookup_acro(self, term):
		r = requests.get("http://acronyms.silmaril.ie/cgi-bin/uncgi/xaa?" + term.strip(".()"))
		element = etree.fromstring(r.text)
		if int(element.find('found').attrib['n']) > 0:
			expanded = next(element.iter('acro')).find('expan').text
			return expanded
		else:
			return ""
			
	
	def lookup(self, term, fromwho, type, depth):
		if depth < 5: # constant for now, might add config parameter later
			expanded = self.lookup_acro(term.strip(".()"))
			if len(expanded) > 0:
				self.send(fromwho, expanded, message_type=type)
				for word in expanded.split():
					self.lookup(word, fromwho, type, depth+1)
		else:
			self.send(fromwho, "Reached recursion limit.", message_type=type)

	def lookup_stack(self, term, fromwho, type):
		depth = 0
		words = []
		back_in = [1]
		words.append([term])
		ret = "Results:"
		while len(words) > 0:
			current = words[-1]
			if len(current) == 0:
				words.pop() # can't do this after processing the last word in the group ir depth counting (and thus, formatting) would be off
				continue
		
			while len(current) > 0:
				word = current.pop(0) # need the first, not the last, element
				ret += "\n" + "\t" * (len(words) - 1) +  word + ": "
				
				expanded = self.lookup_acro(word.strip(".()"))
				if len(expanded) > 0 and len(words) < 5:
					ret += expanded
					words.append(expanded.split())
					break # leave the rest of this group until after the new group is processed
				else:
					ret += "-"
		self.send(fromwho, ret, message_type=type)
