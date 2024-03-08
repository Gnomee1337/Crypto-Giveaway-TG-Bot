import os
import json
from web3 import Web3, EthereumTesterProvider
from dotenv import load_dotenv


async def token_connection():
    load_dotenv()
    w3 = Web3(Web3.WebsocketProvider(os.getenv('COIN_API')))
    if w3.is_connected():
        return True
    else:
        return False


async def token_transaction(receiver_wallet, token_amount):
    # Load env
    load_dotenv()
    owner_wallet = os.getenv('OWNER_WALLET')
    contract_address = os.getenv('CONTRACT_ADDRESS')
    # Make API connection
    w3 = Web3(Web3.WebsocketProvider(os.getenv('COIN_API')))
    if w3.is_connected():
        print("###DEBUG-COIN### Coin API connected")

        # Read ABI
        with open("./contracts/puppy_abi.json", "r") as file:
            abi_filedata = json.load(file)
        # Connect Contract
        erc_contract = w3.eth.contract(contract_address, abi=abi_filedata)
        # Get contract decimals
        decimals = erc_contract.functions.decimals().call()
        DECIMALS = 10 ** decimals

        send_to_wallet = receiver_wallet

        # unicorns = w3.eth.contract(address=contract_address, abi=abi_filedata)

        # Set amount of transactions from owner
        nonce = w3.eth.get_transaction_count(owner_wallet)

        # Create transaction template
        unicorn_txn = erc_contract.functions.transfer(
            receiver_wallet,
            w3.to_wei(token_amount, 'ether'),
        ).build_transaction(
            {
                'chainId': 11155111,
                'gas': 70000,
                'maxFeePerGas': w3.to_wei('2', 'gwei'),
                'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
                'nonce': nonce,
            }
        )

        # Sign transaction
        private_key = os.getenv('PRIVATE_KEY_COIN')
        signed = w3.eth.account.sign_transaction(unicorn_txn, private_key=private_key)

        # Send signed transaction
        w3.eth.send_raw_transaction(signed.rawTransaction)

        # print(erc_contract.functions.balanceOf(owner_wallet).call()/DECIMALS)
        print("###DEBUG-COIN### Transaction completed!")
    else:
        print("###DEBUG-COIN### Coin API not connected")
