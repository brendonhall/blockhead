import json
from web3 import Web3

# Connect to Ethereum network via Infura
infura_url = "https://sepolia.infura.io/v3/3ec4e3eb7199461bb399f4504ec9ed4e"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Input: Contract Address, IPFS Hash, and Address
contract_address_input = input("Enter the contract address: ")
ipfs_hash = input("Enter the IPFS hash: ")
address = input("Enter your address: ")

# Convert contract address to checksum address
contract_address = Web3.to_checksum_address(contract_address_input)

# Contract Details
abi = json.loads('[{"inputs": [{"internalType": "string", "name": "_ipfsHash", "type": "string"}], "name": "getFileName", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}]')
contract = w3.eth.contract(address=contract_address, abi=abi)

# Use the getter function to retrieve the file name
try:
    file_name = contract.functions.getFileName(ipfs_hash).call({'from': Web3.to_checksum_address(address)})
    print(f"IPFS Hash: {ipfs_hash}")
    print(f"File Name: {file_name}")
except Exception as e:
    print(f"An error occurred while retrieving the file name: {e}")