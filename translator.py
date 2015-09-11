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

def process_translation_text(txt, should_translate, insert_value):
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
            if "</%s>" % tag_name in s:
                new = s.split("</%s>" % tag_name)
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
            # translated_values.append(fetch_translation(value))
            if should_translate:
                translated_values.append('&lt;{0}&lg;{1}&lt;/{2}&gt;'.format(tag_name, fetch_translation(value),tag_name))
            else:
                translated_values.append('&lt;{0}&lg;{1}&lt;/{2}&gt;'.format(tag_name, insert_value,tag_name))

        # print(translated_values)
        #do what we need to get the translations
        return "".join(translated_values)
    else:
        if should_translate:
            return fetch_translation(txt)
        else:
            return insert_value


def parse(e_tree):
    for child in e_tree:
        # print(child.tag)
        if child.tag == "trans-unit":
            print(child.getchildren()[0].text)
            try:
                # print 'counter value : {0}'.format(counter)
                # if "SalePanels" in child.attrib.get('extradata')  or child.attrib.get('extradata')[0:2] == "TD":
                if 'MYMEMORY WARNING:' in child.getchildren()[1].text:
                    child.getchildren()[1].text=process_translation_text(child.getchildren()[0].text, False, "\u6c64\u6c64\u6c64")
                # child.getchildren()[1].text = "\u6c64"
            except:
                print "Adding soup"
                child.getchildren()[1].text = process_translation_text(child.getchildren()[0].text, False, "\u6c64\u6c64\u6c64")
        else:
            parse(child)
#this is the part we actually need
e = ElementTree.parse('membership.xml').getroot()
parse(e)
output_file = open( 'shit.xlf', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( e ) )
output_file.close()

#ok, here's just some proof of concept...


