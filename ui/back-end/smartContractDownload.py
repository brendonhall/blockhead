import ipfshttpclient
import json
from web3 import Web3
import matplotlib.pyplot as plt
import PIL.Image as Image
import io

# Connect to IPFS
ipfs_client = ipfshttpclient.connect()

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

# Verify that the hash exists in the contract and check authorization
try:
    file_name = contract.functions.getFileName(ipfs_hash).call({'from': Web3.to_checksum_address(address)})
    if file_name:
        print(f"Verified IPFS Hash: {ipfs_hash}")
        print(f"File Name: {file_name}")
    else:
        print("Hash not found in the contract or unauthorized access.")
        exit()
except Exception as e:
    print(f"An error occurred while verifying the IPFS hash: {e}")
    exit()

# Download the file from IPFS and show the image
try:
    file_data = ipfs_client.cat(ipfs_hash)
    image = Image.open(io.BytesIO(file_data))
    plt.imshow(image)
    plt.axis('off')  # Hide axis
    plt.show()
    print(f"Image displayed successfully.")
except Exception as e:
    print(f"An error occurred while downloading or displaying the image from IPFS: {e}")