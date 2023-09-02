import requests
from bs4 import BeautifulSoup
import streamlit as st

def changepwd(r,s, old):
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Account/ChangePIN")
    soup = BeautifulSoup(r.content,'html5lib')
    pwd_info = {}
    pwd_info['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    pwd_info['OldPIN'] = old
    key1 = 1


    while True:
        new_pwd = input("Enter New Password (Must follow rules)")
        #button = st.button("Enter", key=key1 + 1)
        if new_pwd is not None:
            pwd_info['NewPIN'] = new_pwd
            pwd_info['RepeatNewPIN'] = pwd_info['NewPIN']
            r = s.post("https://watcard.uwaterloo.ca/OneWeb/Account/ChangePIN",data=pwd_info)
            soup = BeautifulSoup(r.content, 'html5lib')
            confirmation = soup.find(class_='alert alert-success')
            if confirmation is not None:
                print("Password has been changed")
                break
            else:
                print("Password could not be changed")
                key1 += 2
