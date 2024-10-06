from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3
import requests
import json  # Import the json module
import matplotlib.pyplot as plt
import io
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import ipfshttpclient  # Import the IPFS HTTP client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for input data
class InputData(BaseModel):
    contractAddress: str
    ipfsHash: str
    address: str

# Connect to IPFS
try:
    ipfs_client = ipfshttpclient.connect()  # Connect to your local IPFS node
except Exception as e:
    print(f"Error connecting to IPFS: {e}")
    ipfs_client = None

# Example POST route to process input data
@app.post("/process-inputs/")
async def process_inputs(data: InputData):
    if not ipfs_client:
        raise HTTPException(status_code=500, detail="IPFS client is not connected.")

    try:
        # Connect to Ethereum network via Infura
        infura_url = "https://sepolia.infura.io/v3/3ec4e3eb7199461bb399f4504ec9ed4e"
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Convert contract address to checksum address
        contract_address = Web3.to_checksum_address(data.contractAddress)

        # Contract ABI (provided earlier)
        abi = '[{"inputs": [{"internalType": "string", "name": "_ipfsHash", "type": "string"}], "name": "getFileName", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}]'
        contract = w3.eth.contract(address=contract_address, abi=json.loads(abi))

        # Verify that the hash exists in the contract and check authorization
        try:
            file_name = contract.functions.getFileName(data.ipfsHash).call({'from': Web3.to_checksum_address(data.address)})
            if file_name:
                print(f"Verified IPFS Hash: {data.ipfsHash}")
                print(f"File Name: {file_name}")
            else:
                raise HTTPException(status_code=404, detail="Hash not found or unauthorized.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error verifying IPFS hash: {str(e)}")

        # Download the file from IPFS and show the image
        try:
            file_data = ipfs_client.cat(data.ipfsHash)
            image = Image.open(io.BytesIO(file_data))
            plt.imshow(image)
            plt.axis('off')  # Hide axis
            plt.show()
            print(f"Image displayed successfully.")
            return JSONResponse(content={"message": "Image displayed successfully."}, status_code=200)

        except Exception as e:
            print(f"Error downloading or displaying the image: {e}")
            raise HTTPException(status_code=500, detail=f"Error downloading or displaying the image from IPFS: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

