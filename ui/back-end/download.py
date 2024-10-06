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

# Example POST route to process input data
@app.post("/process-inputs/")
async def process_inputs(data: InputData):
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

        # Download the file from an alternative IPFS gateway and show the image
        try:
            print(f"Attempting to download the file from IPFS: {data.ipfsHash}")
            # Use an alternative IPFS gateway (dweb.link)
            gateway_url = f"https://dweb.link/ipfs/{data.ipfsHash}"

            # Extend the timeout to 5 minutes (300 seconds)
            response = requests.get(gateway_url, timeout=300)
            print(f"Response status code: {response.status_code}")

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Error downloading from IPFS. Status code: {response.status_code}")
            
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            file_data = response.content
            print(f"File successfully downloaded from IPFS. Length: {len(file_data)} bytes")

            # Process the file as an image
            image = Image.open(io.BytesIO(file_data))
            plt.imshow(image)
            plt.axis('off')  # Hide axis
            plt.show()

            return JSONResponse(content={"message": "Image displayed successfully."}, status_code=200)

        except requests.exceptions.RequestException as e:
            print(f"Error during HTTP request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error downloading from IPFS gateway: {str(e)}")
        except Exception as e:
            print(f"Error processing the image: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



