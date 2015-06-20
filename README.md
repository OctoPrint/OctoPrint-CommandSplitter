# OctoPrint CommandSplitter Plugin

This is a small GCODE preprocessor that makes sure that uploaded GCODE file contain only one command per line.

GCODE allows putting multiple commands on one line, separated by a <code>:</code> (colon). Since it is currently a bit
unclear how firmware should process such lines with regards to included line numbers or checksums, in order to
avoid any confusion this plugin can be used to make sure that all such multi-command-lines in uploaded GCODE files
are split into multiple lines first.

## Example

If an uploaded GCODE file contains these lines:

    G28 X0 Y0 : G28 Z0 ; home all axes
    ; this is a comment with a colon : in the middle
    M117 Hello there \:)

this plugin will turn them into these lines:

    G28 X0 Y0
    G28 Z0; home all axes
    ; this is a comment with a colon in the middle
    M117 Hello there \:)

Note that it will touch neither colons in comments nor escaped ones. Be careful though, it is currently not completely
clear if all firmwares support escaping the colon as shown above. Better not use any : within your commands if possible.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-CommandSplitter/archive/master.zip

