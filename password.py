import requests
from bs4 import BeautifulSoup
import streamlit as st

def changepwd(r,s, old):
    confirmation = 1
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Account/ChangePIN")
    soup = BeautifulSoup(r.content,'html5lib')
    pwd_info = {}
    pwd_info['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    pwd_info['OldPIN'] = old
    new_pwd = st.text_input("Enter New Password (Must follow rules)")
    result = st.button("Enter", key=2)
    if result:
        pwd_info['NewPIN'] = new_pwd
        pwd_info['RepeatNewPIN'] = pwd_info['NewPIN']
        r = s.post("https://watcard.uwaterloo.ca/OneWeb/Account/ChangePIN",data=pwd_info)
        soup = BeautifulSoup(r.content, 'html5lib')
        confirmation = soup.find(class_='alert alert-success')
        if confirmation is not None:
            return "Password has been changed"
        else:
            return "Password could not be changed"

    