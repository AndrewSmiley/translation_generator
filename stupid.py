__author__ = 'pridemai'
output_file = open( 'shit.xlf', 'r' ).read()
import HTMLParser
txt=HTMLParser.HTMLParser().unescape(output_file)

out = open("fml.xlf", "w")
out.write(unicode(txt))
out.close()