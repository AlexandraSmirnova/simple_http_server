from noseapp import Suite
from noseapp import TestCase
from noseapp.ext.requests import RequestsEx, make_config
import noseapp
import json

suite = noseapp.Suite(__name__)

endpoint = make_config()
endpoint.configure(
	base_url='http://localhost:5000',
	key='httpbin'
)
endpoint.session_configure(
	always_return_json=True,
	raise_on_http_error=True
)

requests_ex = RequestsEx(endpoint)
api = requests_ex.get_endpoint_session('httpbin')
			  

@suite.register
class StepByStepCase(noseapp.ScreenPlayCase):	
	
	@noseapp.step(1, 'Delete old value if exist')
	def step_one(self):
		api.delete('dictionary/hello')       

	@noseapp.step(2, 'new value in dictionary')
	def step_two(self):
		api.post('dictionary', {'key': 'hello', 'value': 'Hello World'})

	@noseapp.step(3, 'put value')
	def step_three(self):
		api.put('dictionary/hello', {'value': 'I am Flask Server!'})

	@noseapp.step(4, 'check value')
	def step_four(self):
		api.get('dictionary/hello')		


@suite.register
class StepByStepCase(noseapp.ScreenPlayCase):	
	
	@noseapp.step(1, 'Delete old value if exist')
	def step_one(self):
		api.delete('dictionary/name')       

	@noseapp.step(2, 'new value in dictionary')
	def step_two(self):
		api.post('dictionary', {'key': 'name', 'value': 'My name is Flask Server'})

	@noseapp.step(3, 'put value')
	def step_three(self):
		api.put('dictionary/name', {'value': 'Flask Server'})

	@noseapp.step(4, 'check value')
	def step_four(self):
		api.get('dictionary/name')



@suite.register
class TestCase(noseapp.TestCase):

	def test_delete_one(self):        
		api.delete('dictionary/hello') 

	def test_delete_two(self):        
		api.delete('dictionary/name') 


app = noseapp.NoseApp('example')
app.register_suite(suite)

app.run()