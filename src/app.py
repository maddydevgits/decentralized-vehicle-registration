from flask import Flask, render_template, redirect, request
from web3 import Web3, HTTPProvider
import json
from ca import *

app=Flask(__name__)
app.secret_key='makeskilled'

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


if __name__=="__main__":
    app.run(debug=True)