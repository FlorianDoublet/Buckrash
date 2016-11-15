#!/usr/bin/python3
from DirectoryParser import *
from StackTrace import *
from FileParser import *
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print(f.__name__ + " function took " + str((time2-time1)*1000.0) + " ms ")
        return ret
    return wrap

class Buckrash:

	"""
	Main class which is the center of our software
	"""

	def __init__(self):

		# path for the training folder of a dataset
		self.path_training = "dataset/training"
		# path for the testing folder of a dataset
		self.path_testing = "dataset/testing"

		self.drp = DirectoryParser(self.path_training, self.path_testing)
		self.buckets = self.drp.create_all_buckets() # Recovers all files and create a Bucket list
		self.stack_trace_to_sort = self.drp.get_unsorted_stack_traces() # Recovers the stack traces to sort

	@timing
	def run(self):
		print("Wait for process...")
		# calculus the right bucket for each stacktrace, and print it
		for stacktrace in self.stack_trace_to_sort:
			self.score_calculus_process(stacktrace)

	def score_calculus_process(self, stacktrace):
		"""
		calculus the right bucket for a stacktrace, then print it
		:param stacktrace: StackTrace we went to put into a bucket
		:return:
		"""

		current_score = 0
		bucket_target_id = 0
		for bucket in self.buckets:
			score = 0

			res = bucket.sub_calculus_score_for_stackline_similarities(stacktrace)
			score += res

			if score >= current_score:  # We store the best bucket's score ID
				bucket_target_id = bucket.bucket_id
				current_score = score

		print(stacktrace.fileId + " -> " + str(bucket_target_id))  # We print the result where the stack trace has to go

if __name__ == '__main__':
	Buckrash().run()

