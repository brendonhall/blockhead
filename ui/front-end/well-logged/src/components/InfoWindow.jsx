import React from 'react';
import './InfoWindow.css'; 
import appLogo from '../images/logo.svg'; 

const InfoWindow = () => {
  return (
    <div className="info-window">
      <div className="info-content">
        <img src={appLogo} alt="App Logo" className="info-logo" />
        <h3>Welcome to Well-Logged!</h3>
        <p>
          Here's how you can use our app:
          <ul>
            <li>Upload your CSV using the file input menu on the left.</li>
            <li>Click on the buttons to generate different interpretations of the data.</li>
            <li>View the results displayed directly below each menu.</li>
            <li>Use our blockchain algorithm to securly translate your data.</li>
          </ul>
        </p>
        <p style={{ marginTop: '15px', fontStyle: 'italic' }}>
          This is open-source software. Feel free to contribute or review the code on our GitHub repository.
        </p>
      </div>
    </div>
  );
};

export default InfoWindow;
