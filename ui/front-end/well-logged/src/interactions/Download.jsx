import React, { useState } from 'react';

const Download = () => {
    const [userInput, setUserInput] = useState('');   // To store user-inputted string

    // Handles changes to user input
    const handleInputChange = (event) => {
        setUserInput(event.target.value);  // Update state when user types
    };

    // Placeholder for the download functionality
    const handleDownload = async () => {
        console.log('User input:', userInput); // You can use this value in your logic
        // TODO: Implement actual download or further actions based on user input
    };

    return (
        <div>
            {/* Text input for user to enter a string */}
            <input 
                type="text" 
                placeholder="Enter a string" 
                value={userInput} 
                onChange={handleInputChange}  // Capture user input
            />
            <br />

            {/* Button to trigger download action */}
            <button onClick={handleDownload}>Download</button>

            {/* Optionally display the user input or other content */}
            {userInput && (
                <div 
                    style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px' }}
                >
                    <p>User Input: {userInput}</p>
                </div>
            )}
        </div>
    );
};

export default Download;
