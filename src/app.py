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

@app.route('/otpForm',methods=['POST','GET'])
def otpForm():
    global otp_created
    otp=request.form['otp']
    print(otp,otp_created)
    if int(otp)==otp_created:
        return redirect('/vehicleRegister')
    return redirect('/')

@app.route('/vehicleRegister')
def vehicleRegister():
    return render_template('vehicleregister.html')

@app.route('/vehicleRegisterForm',methods=['POST','GET'])
def vehicleRegisterForm():
    walletaddr=request.form['walletaddr']
    vehicletype=request.form['vehicletype']
    vehicleno=request.form['vehicleno']
    owneremail=request.form['owneremail']
    owneraddr=request.form['owneraddr']
    chassisno=request.form['chassisno']
    ownername=request.form['ownername']
    print(walletaddr,vehicletype,vehicleno,owneremail,owneraddr,chassisno,ownername)
    contract,web3=connect_with_blockchain(0)
    tx_hash=contract.functions.addVehicle(walletaddr,vehicletype,vehicleno,owneremail,owneraddr,chassisno,ownername).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    verifyIdentity(owneremail)
    while True:
        try:
            a=sendmessage('Vehicle Registration',walletaddr,vehicletype,vehicleno,owneremail,owneraddr,chassisno,ownername,owneremail)
            if(a):
                break
            else:
                continue
        except:
            time.sleep(10)
    
    return redirect('/listVehicles')

@app.route('/listVehicles')
def listVehicles():
    data=[]
    contract,web3=connect_with_blockchain(0)
    vOwners,vTypes,vNumbers,vEmails,vAddresses,vChassisnos,vOwnernames=contract.functions.viewVehicles().call()
    for i in range(len(vOwners)):
        dummy=[]
        dummy.append(vOwners[i])
        dummy.append(vTypes[i])
        dummy.append(vNumbers[i])
        dummy.append(vEmails[i])
        dummy.append(vAddresses[i])
        dummy.append(vChassisnos[i])
        dummy.append(vOwnernames[i])
        data.append(dummy)
    l=len(data)
    return render_template('listvehicles.html',dashboard_data=data,len=l)

@app.route('/logout')
def logout():
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)