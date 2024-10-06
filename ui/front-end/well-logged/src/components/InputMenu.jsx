import React, { useState } from 'react';

const InputMenu = ({ onProcessInput }) => {
    const [input1, setInput1] = useState('');   // Store input 1
    const [input2, setInput2] = useState('');   // Store input 2
    const [input3, setInput3] = useState('');   // Store input 3

    // Handle input field changes
    const handleInput1Change = (event) => {
        setInput1(event.target.value);  // Update input 1 state
    };

    const handleInput2Change = (event) => {
        setInput2(event.target.value);  // Update input 2 state
    };

    const handleInput3Change = (event) => {
        setInput3(event.target.value);  // Update input 3 state
    };

    // Handle submit action
    const handleSubmit = async () => {
        if (input1.trim() === "" || input2.trim() === "" || input3.trim() === "") {
            alert("Please enter valid inputs.");
            return;
        }

        // Send the inputs to the backend
        try {
            const response = await fetch('http://127.0.0.1:8000/process-inputs/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contractAddress: input1,
                    ipfsHash: input2,
                    address: input3,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                alert("Processing successful");
            } else {
                alert("Error: " + data.detail);
            }
        } catch (error) {
            console.error("Error while submitting inputs:", error);
            alert("Error submitting inputs.");
        }
    };

    return (
        <div className="input-menu">
            <h3>Enter Your Strings</h3>
            <input 
                type="text" 
                placeholder="Contract Address" 
                value={input1} 
                onChange={handleInput1Change}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <input 
                type="text" 
                placeholder="IPFS Hash" 
                value={input2} 
                onChange={handleInput2Change}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <input 
                type="text" 
                placeholder="Ethereum Address" 
                value={input3} 
                onChange={handleInput3Change}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <button onClick={handleSubmit} style={{ padding: '10px', cursor: 'pointer' }}>
                Submit
            </button>
        </div>
    );
};

export default InputMenu;
