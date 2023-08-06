import re
import hashlib

def get_cms_id(url):
    '''Takes an URL and returns a found CMS-ID or a md5 hash, if no CMS-ID
        was found'''
    #Tries to extract a CMS-ID with regex:
    #- GUID (used by SPON)
    #- at least 7 digits in a row (used by BILD, t-online, watson, FOCUS)
    #- a string that starts with id_ (used by t-online)
    #- a string with at least 7 digits or uppercase letters (used by RND)
    try:
        regex_string = '|'.join(
            [
                '[^\da-zA-Z](\d{8}\-\d{6}\-\d{2}\-\d{6})',
                '(?!\d*\-|[a-z]*\-)[^\da-zA-Z]([\da-zA-Z]{24}\-[\da-zA-Z]{8})',
                '[^\da-zA-Z]((?!\d*\-|[a-z]*\-)[\dA-Za-z]{8}\-(?!\d*\-|[a-z]*\-)[\dA-Za-z]{4}\-(?!\d*\-|[a-z]*\-)[\dA-Za-z]{4}\-(?!\d*\-|[a-z]*\-)[\dA-Za-z]{4}\-(?!\d*\-|[a-z]*\-)[\dA-Za-z]{12})',
                '(\d{7,})',
                'id_([0-9a-zA-Z\-]+)',
                '([A-Z0-9]{7,})',
                '\/(\d{5})\-'
            ]
        )
        cms_id = re.search( regex_string, url )
        cms_id = cms_id.group(cms_id.lastindex)
    #If no CMS-ID is found, the complete URL is hashed with md5
    except:
        to_md5 = url.encode('utf-8').lower()
        cms_id = hashlib.md5()
        cms_id.update(to_md5)
        cms_id = cms_id.hexdigest()
    return cms_id
