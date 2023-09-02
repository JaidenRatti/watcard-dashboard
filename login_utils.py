import requests
from bs4 import BeautifulSoup

def login(user,pwd):
    url = "https://watcard.uwaterloo.ca/OneWeb/Account/LogOn"
    login_data = {
        'Account': user,
        'Password': pwd
    }
    with requests.Session() as s:
        r = s.get(url)
        login_data = get_login_data(r,login_data)
        r = s.post(url, data=login_data)
        personal_info = get_personal_info(r,s)
    
    return personal_info,r,s    

def get_login_data(r,login_data):
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
