import requests
from bs4 import BeautifulSoup

def get_login_data(r,url,login_data,s):
    soup = BeautifulSoup(r.content, 'html5lib')
    #hidden login info
    login_data['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    login_data['AccountMode'] = soup.find('input',attrs={'name':'AccountMode'})
    return login_data

def get_personal_info(r,s):
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Account/Personal")
    soup = BeautifulSoup(r.content, 'html5lib')
    data = soup.find_all(class_="ow-value")
    lst = []
    for datum in data:
        info = datum.get_text()
        lst.append(info)
    if not lst:
        return 0
    else:
        dct = {
            "Name": lst[0],
            "Marital Status": lst[2],
            "Email": lst[3]
        }
        return dct
    