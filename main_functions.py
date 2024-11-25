from web3 import Web3
import json, time
import os
from dotenv import load_dotenv

global contract, private_key, public_key, abi, nonce

# Initialize variables
load_dotenv()
node_url = os.getenv('NETWORK_URL', 'http://127.0.0.1:8545')
contract_address = os.getenv('CONTRACT_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')
public_key = os.getenv('PUBLIC_KEY')

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
    try:
        # get nonce
        nonce = web3.eth.get_transaction_count(public_key)

        # get current gas price
        gas_price = web3.eth.gas_price

        # create transaction
        tx = contract.functions.addDPP(companyName, productType, productDetail, manufactureDate).build_transaction({'nonce': nonce,'from': public_key, 'gas': 250000,'gasPrice': gas_price})

        # sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # get recepit
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # get dpp identifier from event
        logs = contract.events.DPPAdded().process_receipt(receipt)
        dpp_identifier = logs[0]['args']['uniqueIdentifier']

        return dpp_identifier

    except Exception as e:
        print("Error ocurred: ", e)
        raise e

#update dpp with same add_dpp values plus dpp_identifier
def update_dpp(dpp_identifier, companyName, productType, productDetail, manufactureDate):
    try:
        # get nonce
        nonce = web3.eth.get_transaction_count(public_key)

        # get current gas price
        gas_price = web3.eth.gas_price

        # create transaction
        tx = contract.functions.updateDPP(dpp_identifier, companyName, productType, productDetail, manufactureDate).build_transaction({'nonce': nonce,'from': public_key, 'gas': 250000,'gasPrice': gas_price})

    # sign transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # send transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # get receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt

    except Exception as e:
        print("Error ocurred: ", e)
        raise e

