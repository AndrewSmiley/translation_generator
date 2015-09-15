__author__ = 'Andrew'
from translator import *


# print process_translation_text("&lt;line&gt;Print Gift&lt;/line&gt;&lt;line&gt;Receipts&lt;/line&gt;", True, "\u6c64\u6c64\u6c64")

e = ElementTree.parse('membership.xml').getroot()
parse(e)
output_file = open( 'lego_translations_zh-CN.xlf', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( e ) )
output_file.close()