from web3 import Web3
import json, time
import os
from dotenv import load_dotenv

global contract, PRIVATE_KEY, PUBLIC_KEY, abi, nonce

# Initialize variables
node_url = os.getenv('NETWORK_URL', 'http://127.0.0.1:8545')
PRIVATE_KEY = os.getenv('PRIVATE_KEY', "private key")
PUBLIC_KEY = os.getenv('PUBLIC_KEY', "public key")
contract_address = os.getenv('CONTRACT_ADDRESS', "contract address")

# Create the node connection
web3 = Web3(Web3.HTTPProvider(node_url))

# read abi
with open('abi.json') as f:
    abi = json.load(f)

contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

# get dpp by dpp_identifier

def get_dpp_history(dpp_identifier):
    dpp = contract.functions.getDPPHistory(dpp_identifier).call()
    return dpp

def get_dpp_first(dpp_identifier):
    dpp = contract.functions.getFirstDPP(dpp_identifier).call()
    return dpp

def get_dpp_last(dpp_identifier):
    dpp = contract.functions.getLastDPP(dpp_identifier).call()
    return dpp

def add_dpp(companyName, productType, productDetail, manufactureDate):
    # get nonce
    nonce = web3.eth.get_transaction_count(PUBLIC_KEY)
    # create transaction
    tx = contract.functions.addDPP(companyName, productType, productDetail, int(manufactureDate)).buildTransaction({'nonce': nonce,'from': PUBLIC_KEY, 'gas': 250000,'gasPrice': 1000000, 'chainId': 1337})
    # sign transaction
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    # send transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(tx_hash)
    # get receipt
    # tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt)
    # get logs
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    print(receipt)
    logs = web3.eth.get_logs({'fromBlock': receipt['blockNumber'], 'toBlock': receipt['blockNumber'], 'address': receipt['to']})
    print(logs)

    return receipt

#update dpp with same add_dpp values plus dpp_identifier
def update_dpp(dpp_identifier, companyName, productType, productDetail, manufactureDate):
    # get nonce
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    # create transaction
    tx = contract.functions.updateDPP(dpp_identifier, companyName, productType, productDetail, int(manufactureDate)).buildTransaction({'nonce': nonce,'from': PUBLIC_KEY, 'gas': 250000,'gasPrice': 1000000})
    # sign transaction
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    # send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash)
    # get receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)
    return tx_receipt


