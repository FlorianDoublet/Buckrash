#!/usr/bin/python3
import os, re
from Bucket import Bucket
from FileParser import FileParser
from StackTrace import StackTrace


class DirectoryParser:
	"""
	Class used to
	"""

	def __init__(self, path_training, path_testing):
		self.path_training = path_training
		self.path_testing = path_testing

	@staticmethod
	def get_directory_subdirectories(path):
		return [os.path.join(path, f) for f in os.listdir(path)]

	def create_all_buckets(self):
		"""
		Creates a list of buckets using self.path as the source directory
		:return: buckets: list of Bucket
		"""
		buckets = []		

		for directory in self.get_directory_subdirectories(self.path_training):
			stack_traces = self.get_all_stack_traces_from_directory(directory)
			bucket = Bucket(os.path.basename(directory), stack_traces)
			buckets.append(bucket)

		return buckets

	def get_all_stack_traces_from_directory(self, path):
		"""
		Creates a list of StackTrace using the given path
		:param path: path of the Bucket directory
		:return: stack_traces: list of StackTrace
		"""
		stack_traces = []
		file_parser = FileParser()

		for subDirectory in self.get_directory_subdirectories(path):
			# stack_trace_path = subDirectory + "\\Stacktrace.txt"  # WINDOWS
			stack_trace_path = subDirectory + "/Stacktrace.txt"  # LINUX
			subDirectory = re.sub(r".*\\", "", subDirectory)
			file_parser.set_file_path(stack_trace_path)
			stack_traces.append(StackTrace(file_parser.split_stack_trace(), subDirectory))

		return stack_traces

	def get_unsorted_stack_traces(self):
		"""
		get the unsorted stacktraces
		:return: stack_traces: List of the unsorted stacktraces
		"""
		stack_traces = []
		file_parser = FileParser()

		for file in os.listdir(self.path_testing):
			file_parser.set_file_path(self.path_testing + '/' + file)
			stack_traces.append(StackTrace(file_parser.split_stack_trace(), file[:-4]))

		return stack_traces

if __name__ == '__main__':
	pass