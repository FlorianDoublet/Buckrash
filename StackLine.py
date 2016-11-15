#!/usr/bin/python3


class StackLine:
	"""
	A StackLine is a sub-part of a StackTrace
	"""

	def __init__(self, parent_stacktrace, line_number, address_list, method_list, file_list, var_list):
		"""
		:param parent_stacktrace: parent of this stackline
		:param line_number: current line number in stacktrace
		:param address_list: list of the addresses of the stacklines
		:param method_list: list of the methods of the stackline
		:param file_list: list of the files of the stackline
		:param var_list: list of vars of the stackline
		"""
		self.parent_stacktrace = parent_stacktrace
		self.line_number = line_number
		self.address_list = address_list
		self.method_list = method_list
		self.file_list = file_list
		self.var_list = var_list
		self.init_global_dict_with_stackline_objects()

	def init_global_dict_with_stackline_objects(self):
		"""
		used the populate the global crash dict of the parent stacktrace witch different objects from the stackline
		"""

		method = None
		file = None
		for address in self.address_list:
			# the second argument is the number of points
			self.add_into_global_dict(address, 8)

		for method_i in self.method_list:
			method = method_i

		for file_i in self.file_list:
			file = file_i

		if method and file:
			self.add_into_global_dict((method, file), 12)
		elif method:
			self.add_into_global_dict(method,1)
		elif file:
			self.add_into_global_dict(file, 10)

	def add_into_global_dict(self, object, point):
		"""
		Method used to add an object with their points to the crash global dict
		:param object: can be anything from the stackline (ex: a method, a file, a tuple...)
		:param point: attributed point for the object
		:return:
		"""
		p_crash_object_dict = self.parent_stacktrace.crash_object_dict

		if object in p_crash_object_dict:
			object_dict = p_crash_object_dict[object]
			object_dict["lines"].append(self.line_number)

		else:
			stack_dict = {"lines" : [self.line_number], "point" : point}
			p_crash_object_dict[object] = stack_dict


