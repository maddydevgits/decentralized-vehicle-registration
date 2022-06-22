from flask import Flask, render_template, redirect, request
from web3 import Web3, HTTPProvider
import json
from ca import *
import random
from SendEmail import *
import time

app=Flask(__name__)
app.secret_key='makeskilled'
otp_created=0
emailId='parvathanenimadhu@gmail.com'

def connect_with_blockchain(acc):
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    if(acc==0):
        web3.eth.defaultAccount = web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=acc
    compiled_contract_path='../build/contracts/vehicle.json'
    deployed_contract_address=vehicleContractAddress

    with open(compiled_contract_path) as file:
        contract_json=json.load(file)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=deployed_contract_address,abi=contract_abi)
    return contract,web3

@app.route('/')
def otpPage():
    global otp_created, emailId
    otp_created=random.randint(1800,9999)
    verifyIdentity(emailId)
    while True:
        try:
            a=sendotp(otp_created,'OTP to login the portal',emailId)
            if(a):
                break
            else:
                continue
        except:
            time.sleep(10)
    return render_template('otp.html')



if __name__=="__main__":
    app.run(debug=True)