# coding=utf-8
from __future__ import absolute_import

import re

import octoprint.plugin

class CommandSplitterStream(octoprint.filemanager.util.LineProcessorStream):

	comment_split_re = re.compile(b"(?<!\\\\);")
	command_split_re = re.compile(b"(?<!\\\\):")

	def process_line(self, line):
		line, comment = self.split_comment(line.strip())
		if line == b"" and len(comment):
			return comment + b"\n"

		lines = self.split_line(line)
		if len(lines) == 0:
			return None

		return b"\n".join(filter(lambda x: x is not None and x != b"", lines)) + comment + b"\n"

	def split_comment(self, line):
		if line.startswith(b";"):
			return b"", line

		if not b";" in line:
			return line, b""

		line, comment = self.__class__.comment_split_re.split(line, maxsplit=1)
		if comment != b"":
			comment = b";" + comment

		return line, comment

	def split_line(self, line):
		if line == b"":
			return []

		if not b":" in line:
			return [line]

		return map(lambda x: x.strip(), self.__class__.command_split_re.split(line.strip()))

def split_all_commands(path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
	if not octoprint.filemanager.valid_file_type(path, type="gcode"):
		return file_object

	return octoprint.filemanager.util.StreamWrapper(file_object.filename, CommandSplitterStream(file_object.stream()))

__plugin_name__ = "CommandSplitter"
__plugin_description__ = "Splits multiple commands on one GCODE line with \":\" separator into multiple lines."
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_hooks__ = {
	"octoprint.filemanager.preprocessor": split_all_commands
}
