#!/usr/bin/python3
import re
from StackLine import *


class StackTrace:
	"""
	A StackTrace is the trace of a captured assert bug
	"""

	def __init__(self, line_list, file_id=""):
		self.fileId = file_id
		self.line_list = line_list
		self.crash_object_dict = {}
		self.stack_lines = self.build_stack_line()

	def build_stack_line(self):
		"""
		Used to build the stackline of the stacktrace.
		:return: stack_lines
		"""
		stack_lines = []
		for i, line in enumerate(self.line_list):
			address_list = self.fill_address_list(line)
			method_list = self.fill_method_list(line)
			file_list = self.fill_file_list(line)
			var_list = self.fill_var_list(line)

			# create the stackline and add it into the list
			stack_lines.append(StackLine(self, i, address_list, method_list, file_list, var_list))

		return stack_lines

	@staticmethod
	def fill_address_list(line):
		"""
		:param line: line of a stacktrace
		:return: list of addresses of a line
		"""
		list_address = re.findall("^0x[0-9a-fA-F]+\s", line)

		return list_address

	@staticmethod
	def fill_file_list(line):
		"""
		:param line: line of a stacktrace
		:return: file_list: list of files of a stacktrace
		"""

		temp_file_list = re.findall("from /*.*\S", line) + re.findall(" at /*.*\S", line) # Some files start with from and some with at
		file_list = []

		char_to_consume_regex_dict = {re.compile("at"): "", re.compile(":[0-9]+"): "", re.compile("from"): "", re.compile("/.*/") : "", re.compile("\..*"): ""}
		for file in temp_file_list:

			file_list.append(StackTrace.replace_key_by_value_for_string(char_to_consume_regex_dict, file).strip())

		return file_list

	@staticmethod
	def fill_var_list(line):
		"""
		:param line: line of a stacktrace
		:return: list of vars of a stacktrace
		"""
		regex = re.compile("[a-zA-Z_$][a-zA-Z_$0-9]* = ")
		return re.findall(regex, line)

	@staticmethod
	def fill_method_list(line):
		"""
		:param line: line of a stacktrace
		:return: method_list: list of methods of a stacktrace
		"""

		# get all methods from line
		tmp_method_list = re.findall(" in .* \(", line) + re.findall("^[^0-9].* \(", line)

		# final list
		method_list = []
		char_to_consume_regex_dict = {" in ": "", re.compile("\("): "", "<IA__": "", re.compile(">$"): ""}
		# We remove all the unwanted chars in our methods string
		for method in tmp_method_list:
			method_list.append(StackTrace.replace_key_by_value_for_string(char_to_consume_regex_dict, method).strip())

		return method_list

	@staticmethod
	def replace_key_by_value_for_string(dictionary, string):
		"""
		:param dictionary: dictionary with keys match that have to be replaced by the value into the string
		:param string: string to format
		:return: string: the formatted string
		"""
		for k, v in dictionary.items():
			string = re.sub(k, "", string)
		return string


if __name__ == '__main__':
	pass
