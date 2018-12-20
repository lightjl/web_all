
import requests


login_session = requests.Session()

url='http://127.0.0.1:8000/mv/'

login_session.get(url) 
