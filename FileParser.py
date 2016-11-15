#!/usr/bin/python3
import re


class FileParser:
	"""
	Utility to parse files
	"""
	def __init__(self, path="/"):
		self.path = path

	def set_file_path(self, path):
		self.path = path

	def read_file(self):
		"""
		read the file in self.path
		:return:
		"""
		try:
			f = open(self.path, 'r')
			file_content = f.read()
			f.close()
		except:
			try:
				f = open(self.path, 'r', encoding="utf8")
				file_content = f.read()
				f.close()
			except:
				f = open(self.path, 'r', encoding="ISO-8859-1")
				file_content = f.read()
				f.close()

		return file_content

	def split_stack_trace(self):
		"""
		Split a StackTrace into part-lines (future StackLine)
		:return: A list of part-line of a StackTrace file
		"""
		file = self.read_file()
		return re.split("^#[0-9]+\s*", file, flags=re.MULTILINE)

	@staticmethod
	def print_splited_stack_trace(m):
		for item in m:
			print(item)
			print("\r\n")

	def run(self): # Simple example
		m = self.split_stack_trace()
		self.print_spited_stack_trace(m)

if __name__ == '__main__':
	pass