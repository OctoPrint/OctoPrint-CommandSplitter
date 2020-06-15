# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

def process_line(line):
	if b':' not in line:
		# no :, bail
		return line

	# extract comments
	comment = b''
	if b';' in line:
		line, comment = line.split(b';', maxsplit=1)
		if line == b'' and len(comment):
			# comment is the only thing on the line, bail
			return comment + b'\n'

	result = b''
	for l in line.split(b':'):
		result += l.lstrip()
		if l.endswith(b'\\'):
			# escaped :, add back
			result += b':'
		else:
			result = result.rstrip() + b'\n'

	if comment:
		result = result[:-1] + b' ;' + comment

	return result.rstrip() + b'\n'

def split_all_commands(path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
	import octoprint
	class CommandSplitterStream(octoprint.filemanager.util.LineProcessorStream):
		def process_line(self, line):
			return process_line(line)

	if not octoprint.filemanager.valid_file_type(path, type="gcode"):
		return file_object

	return octoprint.filemanager.util.StreamWrapper(file_object.filename, CommandSplitterStream(file_object.stream()))

__plugin_name__ = "CommandSplitter"
__plugin_description__ = "Splits multiple commands on one GCODE line with \":\" separator into multiple lines."
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_hooks__ = {
	"octoprint.filemanager.preprocessor": split_all_commands
}
