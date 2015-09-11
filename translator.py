__author__ = 'smileya'
import requests
import urllib
import HTMLParser
import cgi
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

def fetch_translation(english_text):
    # key=trnsl.1.1.20150911T175348Z.9da4e8f8a4e6a6b4.c6451ebd664034a0ae11e170add76df0c2969470&lang=en-zh&text=Hello+,+world+!
    f = {'key': 'trnsl.1.1.20150911T175348Z.9da4e8f8a4e6a6b4.c6451ebd664034a0ae11e170add76df0c2969470', 'lang':"en-zh", 'text': english_text}
    r = requests.get('https://translate.yandex.net/api/v1.5/tr/translate?{0}'.format(urllib.urlencode(f)))
    # r.content
    # e = ElementTree.parse(r.content).getroot()
    print ElementTree.fromstring(r.content).getchildren()[0].text
    return ElementTree.fromstring(r.content).getchildren()[0].text

def process_translation_text(txt, should_translate, insert_value):
    #just to unescape
    txt=HTMLParser.HTMLParser().unescape(txt)
    if "<" in txt:
        # print "We have tags in it"
        tag_name = txt[txt.find("<")+1:txt.find(">")]
        tag_value=txt[txt.find(">")+1:len(txt)-(len(tag_name)+3)]
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
        # print split_values
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
            # print(child.getchildren()[0].text)
            try:
                # print 'counter value : {0}'.format(counter)
                # if "SalePanels" in child.attrib.get('extradata')  or child.attrib.get('extradata')[0:2] == "TD":
                if 'MYMEMORY WARNING:' in child.getchildren()[1].text:
                    child.getchildren()[1].text=process_translation_text(child.getchildren()[0].text, True, "\u6c64\u6c64\u6c64")
                # child.getchildren()[1].text = "\u6c64"
            except Exception as e:
                print e.message
                print "Adding soup"
                child.getchildren()[1].text = process_translation_text(child.getchildren()[0].text, False, "\u6c64\u6c64\u6c64")
        else:
            parse(child)
#this is the part we actually need
# fetch_translation("Load up on guns, bring your friends, It's fun to lose and to pretend, She's over bored and self assured, Oh no, I know a dirty word")
e = ElementTree.parse('membership.xml').getroot()
parse(e)
output_file = open( 'new_translations.xlf', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( e ) )
output_file.close()

#ok, here's just some proof of concept...


