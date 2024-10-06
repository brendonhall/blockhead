import io
from typing import Union

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, Response, UploadFile
from mpl_toolkits.axes_grid1 import make_axes_locatable
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

facies_colors = [
    "#F4D03F",
    "#F5B041",
    "#DC7633",
    "#6E2C00",
    "#1B4F72",
    "#2E86C1",
    "#AED6F1",
    "#A569BD",
    "#196F3D",
]

def make_facies_log_plot(logs, facies_colors):
    # make sure logs are sorted by depth
    logs = logs.sort_values(by="Depth")
    cmap_facies = colors.ListedColormap(
        facies_colors[0 : len(facies_colors)], "indexed"
    )

    ztop = logs.Depth.min()
    zbot = logs.Depth.max()

    cluster = np.repeat(np.expand_dims(logs["Facies"].values, 1), 100, 1)

    f, ax = plt.subplots(nrows=1, ncols=6, figsize=(8, 12))
    ax[0].plot(logs.GR, logs.Depth, "-g")
    ax[1].plot(logs.ILD_log10, logs.Depth, "-")
    ax[2].plot(logs.DeltaPHI, logs.Depth, "-", color="0.5")
    ax[3].plot(logs.PHIND, logs.Depth, "-", color="r")
    ax[4].plot(logs.PE, logs.Depth, "-", color="black")
    im = ax[5].imshow(
        cluster, interpolation="none", aspect="auto", cmap=cmap_facies, vmin=1, vmax=9
    )

    divider = make_axes_locatable(ax[5])
    cax = divider.append_axes("right", size="20%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label(
        (17 * " ").join(
            [" SS ", "CSiS", "FSiS", "SiSh", " MS ", " WS ", " D  ", " PS ", " BS "]
        )
    )
    cbar.set_ticks(range(0, 1))
    cbar.set_ticklabels("")

    for i in range(len(ax) - 1):
        ax[i].set_ylim(ztop, zbot)
        ax[i].invert_yaxis()
        ax[i].grid()
        ax[i].locator_params(axis="x", nbins=3)

    ax[0].set_xlabel("GR")
    ax[0].set_xlim(logs.GR.min(), logs.GR.max())
    ax[1].set_xlabel("ILD_log10")
    ax[1].set_xlim(logs.ILD_log10.min(), logs.ILD_log10.max())
    ax[2].set_xlabel("DeltaPHI")
    ax[2].set_xlim(logs.DeltaPHI.min(), logs.DeltaPHI.max())
    ax[3].set_xlabel("PHIND")
    ax[3].set_xlim(logs.PHIND.min(), logs.PHIND.max())
    ax[4].set_xlabel("PE")
    ax[4].set_xlim(logs.PE.min(), logs.PE.max())
    ax[5].set_xlabel("Facies")

    ax[1].set_yticklabels([])
    ax[2].set_yticklabels([])
    ax[3].set_yticklabels([])
    ax[4].set_yticklabels([])
    ax[5].set_yticklabels([])
    ax[5].set_xticklabels([])
    f.suptitle("Well: %s" % logs.iloc[0]["Well Name"], fontsize=14, y=0.94)
    return f


from fastapi import FastAPI, HTTPException, File, UploadFile, Response
from pydantic import BaseModel
from web3 import Web3
import ipfshttpclient
import matplotlib.pyplot as plt
import io
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

app = FastAPI()

# Add CORS middleware
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

# Route to process inputs and return an image
@app.post("/process-inputs/")
async def process_inputs(data: InputData):
    try:
        # Connect to IPFS
        ipfs_client = ipfshttpclient.connect()

        # Connect to Ethereum network via Infura
        infura_url = "https://sepolia.infura.io/v3/3ec4e3eb7199461bb399f4504ec9ed4e"
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Convert contract address to checksum address
        contract_address = Web3.to_checksum_address(data.contractAddress)

        # Contract ABI
        abi = json.loads('[{"inputs": [{"internalType": "string", "name": "_ipfsHash", "type": "string"}], "name": "getFileName", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}]')
        contract = w3.eth.contract(address=contract_address, abi=abi)

        # Verify that the hash exists in the contract and check authorization
        try:
            file_name = contract.functions.getFileName(data.ipfsHash).call({'from': Web3.to_checksum_address(data.address)})
            if not file_name:
                raise HTTPException(status_code=404, detail="Hash not found or unauthorized.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error verifying IPFS hash: {str(e)}")

        # Download the file from IPFS
        try:
            print(f"Attempting to download the file from IPFS: {data.ipfsHash}")
            file_data = ipfs_client.cat(data.ipfsHash)
            print(f"File successfully downloaded from IPFS, length: {len(file_data)} bytes")

            # Open the image using PIL
            image = Image.open(io.BytesIO(file_data))

            # Convert the image to bytes (PNG format)
            image_io = io.BytesIO()
            image.save(image_io, format="PNG")
            image_io.seek(0)

            # Return the image as a response
            return Response(content=image_io.getvalue(), media_type="image/png")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error downloading or displaying image: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
