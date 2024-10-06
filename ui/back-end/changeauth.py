import json
from web3 import Web3

# Connect to Ethereum network via Infura
infura_url = "https://sepolia.infura.io/v3/3ec4e3eb7199461bb399f4504ec9ed4e"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Wallet and Contract Details
private_key = "YOUR_PRIVATE_KEY"
account = w3.eth.account.from_key(private_key)
contract_address = Web3.to_checksum_address("0xe39c1af35f361af2e7edcc2fa10bbd27883ccfad")
abi = json.loads('[{"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "authorizeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "revokeAuthorization", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]')
contract = w3.eth.contract(address=contract_address, abi=abi)

# Function to authorize an address
def authorize_address(address_to_authorize):
    nonce = w3.eth.get_transaction_count(account.address, 'pending')
    transaction = contract.functions.authorizeAddress(address_to_authorize).build_transaction({
        'chainId': 11155111,  # Sepolia testnet
        'gas': 3000000,  # Gas limit
        'gasPrice': w3.to_wei('100', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash for authorizing address: {txn_hash.hex()}")
    except Exception as e:
        print(f"An error occurred while authorizing the address: {e}")

# Function to revoke authorization for an address
def revoke_authorization(address_to_revoke):
    nonce = w3.eth.get_transaction_count(account.address, 'pending')
    transaction = contract.functions.revokeAuthorization(address_to_revoke).build_transaction({
        'chainId': 11155111,  # Sepolia testnet
        'gas': 3000000,  # Gas limit
        'gasPrice': w3.to_wei('100', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash for revoking authorization: {txn_hash.hex()}")
    except Exception as e:
        print(f"An error occurred while revoking the authorization: {e}")

# Function to transfer ownership of the contract
def transfer_ownership(new_owner):
    nonce = w3.eth.get_transaction_count(account.address, 'pending')
    transaction = contract.functions.transferOwnership(new_owner).build_transaction({
        'chainId': 11155111,  # Sepolia testnet
        'gas': 3000000,  # Gas limit
        'gasPrice': w3.to_wei('100', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash for transferring ownership: {txn_hash.hex()}")
    except Exception as e:
        print(f"An error occurred while transferring ownership: {e}")

# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage authorizations and ownership for the smart contract.")
    parser.add_argument("action", choices=["authorize", "revoke", "transfer"], help="The action to perform: authorize, revoke, or transfer.")
    parser.add_argument("address", help="The address to authorize, revoke, or transfer ownership to.")

    args = parser.parse_args()

    if args.action == "authorize":
        authorize_address(Web3.to_checksum_address(args.address))
    elif args.action == "revoke":
        revoke_authorization(Web3.to_checksum_address(args.address))
    elif args.action == "transfer":
        transfer_ownership(Web3.to_checksum_address(args.address))