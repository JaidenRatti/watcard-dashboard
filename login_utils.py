import requests
from bs4 import BeautifulSoup

def get_login_data(r,url,login_data,s):
    soup = BeautifulSoup(r.content, 'html5lib')
    #hidden login info
    login_data['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    login_data['AccountMode'] = soup.find('input',attrs={'name':'AccountMode'})
    return login_data
