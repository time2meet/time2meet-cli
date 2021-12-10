import os
from getpass import getpass
from .request_handler import request
from .yaml_validator import yaml_user
import json


def __dir__():
    return ["token_info", "new_token", "delete_token"]


def token_req(protocol, param = None, data = None):
    return request(protocol, "token", param = param, data = data)


#Get current token info
#
def token_info():
    tok = getpass("Enter the user's token: ")
    token_req("get", {"userId": yaml_user()["userId"], "token": tok})


#Create a new token
#
def new_token(email = None, pswrd = None):
    if email is None:
        email = input("Enter your email: ")

    print("Creating a new token: ")

    try:
        scopes = input("Please enter your desired scopes: ").split()
    except:
        print("Setting scopes to default values: read write")
        scopes = ["read", "write"]
 
    try:
        duration = int(input("How long should this token stay valid in terms of days: "))

    except:
        print("Setting length to default value: 7")
        duration = 7

    if pswrd is None:
        pswrd = getpass("Enter your password: ")

    if token_req("post", {"password":  pswrd, "email": email}, {"maxAge": duration, "scopes": json.dumps(scopes)}):
        print("SAVE YOUR TOKEN SOMEWHERE, IT WILL NOT BE SAVED.")


#Delete a token
#
def delete_token():
    confirm = input("Are you sure you want to delete your token [Enter 'confirm' for confirmation]: ")

    if confirm == "confirm":
        tok = getpass("Please enter your token: ")
        user_req("delete", {"token": tok, "userId": yaml_user()["userId"]})

    else:
        print("Confirmaiton failed, stopping.")
        os._exit(1)


