import numpy as np
import ipfshttpclient
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import json
from web3 import Web3
import pandas as pd

# Connect to IPFS
ipfs_client = ipfshttpclient.connect()

# Request input for file to upload
file_path = input("Enter the path to the file to upload: ")
file_name = input("Enter the file name: ")

ipfs_data = pd.read_excel(file_path)
well_log = ipfs_data
depth = well_log.iloc[1:, 0].values
well_log = well_log.iloc[1:, 2].values

# Define the orders of the Gaussian filters
orders = [2, 2, 2, 2]

# Define the sigma values for the Gaussian filters
sigmas = [0.5, 1, 2, 4]

second_derivative = np.zeros((len(sigmas), len(depth)))
for i, (order, sigma) in enumerate(zip(orders, sigmas)):
    smoothed_well_log = gaussian_filter(well_log, sigma, order=order)
    second_derivative[i, :] = np.gradient(np.gradient(smoothed_well_log))

plt.figure(figsize=(20, 6))
contour = plt.contour(depth, sigmas, second_derivative, colors='k')
plt.xlabel('Depth (m)')
plt.ylabel('Sigma')
plt.title('2nd Derivative of Gaussian Filtered Well Log')
plt.show()

# Upload the file to IPFS
try:
    res = ipfs_client.add(file_path)
    ipfs_hash = res['Hash']
    print(f"File uploaded to IPFS with hash: {ipfs_hash}")
except Exception as e:
    print(f"An error occurred while uploading the file: {e}")
    exit()

# Connect to Ethereum network via Infura
infura_url = "https://sepolia.infura.io/v3/3ec4e3eb7199461bb399f4504ec9ed4e"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Request Wallet and Contract Details
private_key = input("Enter your private key: ")
account = w3.eth.account.from_key(private_key)
contract_address_input = input("Enter the contract address: ")
contract_address = Web3.to_checksum_address(contract_address_input)
abi = json.loads('[{"inputs": [{"internalType": "string", "name": "_ipfsHash", "type": "string"}, {"internalType": "string", "name": "_fileName", "type": "string"}], "name": "addIPFSHash", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]')
contract = w3.eth.contract(address=contract_address, abi=abi)

# Get current nonce
nonce = w3.eth.get_transaction_count(account.address, 'pending')

# Build the transaction to add the IPFS hash and file name to the contract
transaction = contract.functions.addIPFSHash(ipfs_hash, file_name).build_transaction({
    'chainId': 11155111,  # Sepolia testnet
    'gas': 3000000,  # Gas limit
    'gasPrice': w3.to_wei('100', 'gwei'),
    'nonce': nonce,
})

# Sign and send the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
try:
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {txn_hash.hex()}")
    # Verify the transaction
    receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=300)
    print(f"Transaction receipt: {receipt}")
except Exception as e:
    print(f"An error occurred while sending the transaction: {e}")