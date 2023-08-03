import urllib

RS_URL = "https://bampfa.resourcespace.com/api"
RS_USER = urllib.parse.quote_plus("jane doe")
RS_USERKEY = "123456789"
# this is defined in RS system config
# there can be arbitrary alt file "types" defined for various uses
AALTERNATIVE_FILE_TYPES = ["Web","Print","Detail"]
