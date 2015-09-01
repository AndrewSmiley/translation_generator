__author__ = 'smileya'
import requests
import urllib
import HTMLParser
import cgi
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

def fetch_translation(english_text):
    f = {'q': english_text, 'langpair':"en|zh-CN"}
    r = requests.get('http://api.mymemory.translated.net/get?{0}'.format(urllib.urlencode(f)))
    print r.json().get('responseData').get('translatedText')
    return r.json().get('responseData').get('translatedText')

def process_translation_text(txt):
    #just to unescape
    txt=HTMLParser.HTMLParser().unescape(txt)
    if "<" in txt:
        print "We have tags in it"
        tag_name = txt[txt.find("<")+1:txt.find(">")]
        #tag_value=txt[txt.find(">")+1:len(txt)-(len(tag_name)+3)]
        #ok so all we really care about here is the tag name not the value
        values = txt.split("<line>")
        split_values=[]
        for s in values:
            if "</line>" in s:
                new = s.split("</line>")
                split_values.append(new[0])
            else:
                if len(s) > 1:
                    split_values.append(s)
                else:
                    #this seems redundant
                    continue
        print split_values
        translated_values=[]
        for value in split_values:
            translated_values.append(fetch_translation(value))
            translated_values.append('<{0}>{1}</{2}>'.format(tag_name, fetch_translation(value),tag_name))

        print(translated_values)
        #do what we need to get the translations
        return cgi.escape("".join(translated_values))
    else:
        return fetch_translation(txt)


def parse(e_tree):
    for child in e_tree:
        # print(child.tag)
        if child.tag == "trans-unit":
            print(child.getchildren()[0].text)
            try:
                # print 'counter value : {0}'.format(counter)
                child.getchildren()[1].text=process_translation_text(child.getchildren()[0].text)
                # child.getchildren()[1].text = "\u6c64"
            except:
                print "Adding soup"
                child.getchildren()[1].text = "\u6c64\u6c64\u6c64"
        else:
            parse(child)
# unescaped="&lt;line&gt;FUCK YOU FUCK YOU FUCK YOU FUCK YOU&lt;/line&gt;"
# escaped=HTMLParser.HTMLParser().unescape(unescaped)
# values = escaped.split("<line>")
# split_values=[]
# for s in values:
#     if "</line>" in s:
#         new = s.split("</line>")
#         split_values.append(new[0])
#     else:
#         if len(s) > 1:
#             split_values.append(s)
#         else:
#             #this seems redundant
#             continue
#
# print split_values






# print(str(r.json().get('responseData').get('translatedText')))
# print(r.json().get('resultData').get('translatedText'))
# print(r.status_code)

#this is the part we actually need
e = ElementTree.parse('lego_translations_zh-CN.xlf').getroot()
parse(e)
output_file = open( 'membership.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( e ) )
output_file.close()



