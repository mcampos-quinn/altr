# standard library imports
import hashlib
import re
import urllib
# third party imports
import requests
# local imports
import config

class RSpaceRequest:
	"""builds a request to rs"""
	def __init__(self,
		rs_api_function=None,
		parameters=None):

		self.status = None
		self.rs_api_function = rs_api_function
		self.parameters = parameters
		self.rs_user = config.RS_USER
		self.rs_userkey = config.RS_USERKEY
		self.rs_url = config.RS_URL
		self.query_url = None

		# self.check_status()

	def check_status(self):
		self.rs_api_function = "get_system_status"
		self.make_query()
		response = self.post_query()
		if not response:
			self.status = None
		else:
			self.status = True

	def format_params(self,parameters):
		params = "&".join(["{}={}".format(k,v) for k,v in parameters.items()])
		return params

	def get_resource_field_data(self,resource_id=None):
		self.rs_api_function = "get_resource_field_data"
		self.parameters = self.format_params({"resource":f"{resource_id}"})
		self.make_query()
		response = self.post_query()

		return response

	def update_field(self,resource_id=None,field_id=None,value=None):
		self.rs_api_function = "update_field"
		self.parameters = self.format_params({
			"resource":resource_id,
			"field":field_id,
			"value":urllib.parse.quote_plus(value)
		})
		self.make_query()
		response = self.post_query()

		return response

	def make_query(self):
		query = "user={}&function={}&{}".format(
			self.rs_user,
			self.rs_api_function,
			self.parameters
			)
		sign = hashlib.sha256(self.rs_userkey.encode()+query.encode())
		sign = sign.hexdigest()
		self.query_url = "{}/?{}&sign={}".format(
			self.rs_url,
			query,
			sign
			)
		print(self.query_url)

	def post_query(self):
		if not self.query_url:
			sys.exit(1) # lol this needs to be less extreme
		response = requests.post(self.query_url)
		if str(response.status_code).startswith('20'):
			try:
				response = response.json()
			except:
				pass
		else:
			response = None

		return response

def filter_field_data_list(field_list,field_to_find):
	# print([x['value'] for x in field_list if x['name'] == field_to_find])
	try:
		value = "".join([x['value'] for x in field_list if x['name'] == field_to_find])
	except:
		value = None

	return value
