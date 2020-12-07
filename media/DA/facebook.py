from setting.function import *

def facebook_load():
    facebook_raw = media_raw_read('facebook')
    facebook_raw['매체'] = 'Facebook'
    return facebook_raw