__author__ = 'smileya'
import requests
import urllib
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

def fetch_translation(english_text):
    f = {'q': english_text, 'langpair':"en|zh-CN"}
    r = requests.get('http://api.mymemory.translated.net/get?{0}'.format(urllib.urlencode(f)))
    return r.json().get('responseData').get('translatedText')

def process_translation_text(txt):
    if "<" in txt:
        print "We have tags in it"
        tag_name = txt[txt.find("<")+1:txt.find(">")]
        tag_value=txt[txt.find(">")+1:len(txt)-(len(tag_name)+3)]
        print tag_name
        print tag_value
        #do what we need to get the translations
        return '<{0}>{1}</{2}>'.format(tag_name, fetch_translation(tag_value),tag_name)
    else:
        return fetch_translation(txt)


def parse(e_tree, counter):


    for child in e_tree:
        # print(child.tag)
        if child.tag == "trans-unit":
            print(child.getchildren()[0].text)
            try:
                print 'counter value : {0}'.format(counter)
                # child.getchildren()[1].text=fetch_translation(child.getchildren()[0].text)
                child.getchildren()[1].text = "\u6c64"
            except:
                print "Adding soup"
                child.getchildren()[1].text = "\u6c64"
        else:
            parse(child,counter)

# print(process_translation_text("<fuckery>We have liftoff</fuckery>"))
# print(u"\u6c64")



# print(str(r.json().get('responseData').get('translatedText')))
# print(r.json().get('resultData').get('translatedText'))
# print(r.status_code)

e = ElementTree.parse('lego_translations_zh-CN.xlf').getroot()
parse(e,1)
output_file = open( 'membership.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( e ) )
output_file.close()
# e.write("output.xlf")
# for child in e:
#     print(child.tag)


