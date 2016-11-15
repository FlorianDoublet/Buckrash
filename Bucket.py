#!/usr/bin/python3
from Buckrash import *

import difflib

class Bucket:
	"""
	A Bucket is a 'folder' which contain a list of StackTrace which is considered from the same bug
	"""

	def __init__(self, bucket_id, stacktrace_list):
		self.bucket_id = bucket_id
		self.stacktrace_list = stacktrace_list

	def sub_calculus_score_for_stackline_similarities(self, unsorted_stacktrace):
		"""
		calculus the matching-score beetween a stacktrace and stacktraces from the bucket
		:param unsorted_stacktrace: stacktrace to compare to the bucket's stacktraces
		:return: current_score: the score for the bucket (in fact for the most similar stacktraces from the bucket)
		"""

		current_score = 0

		for sorted_stack in self.stacktrace_list:
			score = 0
			nb_match = 0
			for obj, val in unsorted_stacktrace.crash_object_dict.items():

				unsort_lines_cpy = list(val["lines"])
				# check if the objet is into the sorted stacktrace to
				if obj in sorted_stack.crash_object_dict:
					sort_lines_cpy = list(sorted_stack.crash_object_dict[obj]["lines"])
					# then increase the number of matches
					nb_match += min(len(sort_lines_cpy), len(unsort_lines_cpy))
					# get the point value from the matching object
					p = sorted_stack.crash_object_dict[obj]["point"]
					# then calculus points peer matching object into the two stacktraces thanks to the lines list
					# the final value for a match depends of the position of the two matching object
					points = [ p / float((x * y)) for x, y in zip(unsort_lines_cpy, sort_lines_cpy)]
					for point in points:
						score += point

			# percent of match for the sorted stacktrace
			sort_percent = nb_match * float(100) / len(sorted_stack.stack_lines)
			# percent of match for the unsorted stacktrace
			unsort_percent = nb_match * float(100) / len(unsorted_stacktrace.stack_lines)

			# average of the matching percents
			matching_percent_average = (sort_percent + unsort_percent) / float(2)
			# default attributed point for matching percentage
			matching_percentage_point = 7
			score += matching_percent_average / matching_percentage_point

			if score >= current_score:
				current_score = score

		return current_score



