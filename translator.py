__author__ = 'smileya'
import requests
import urllib
import xml.etree.ElementTree
def fetch_translation(english_text):
    f = {'q': english_text, 'langpair':"zh-CN"}
    r = requests.get('http://api.mymemory.translated.net/get?{0}'.format(urllib.urlencode(f)))
    return r.json().get('responseData').get('translatedText')
def parse(e_tree):
    for child in e_tree:
        # print(child.tag)
        if child.tag == "trans-unit":
            print(child.getchildren()[0].text)
            child.getchildren()[1].text=fetch_translation(child.getchildren()[0].text)
        else:
            parse(child)





# print(str(r.json().get('responseData').get('translatedText')))
# print(r.json().get('resultData').get('translatedText'))
# print(r.status_code)

e = xml.etree.ElementTree.parse('lego_translations_zh-CN.xlf').getroot()
parse(e)
e.write("output.xlf")
# for child in e:
#     print(child.tag)


