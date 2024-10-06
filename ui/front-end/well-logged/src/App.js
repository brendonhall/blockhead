import './App.css';
import 'semantic-ui-css/semantic.min.css';
import { useState } from 'react';
import { PaperCanvas } from './components/PaperCanvas.jsx';
import { View } from './components/View.jsx';
import { CreateGridBG } from './interactions/CreateGridBG.jsx';
import Draggable from 'react-draggable';
import InputMenu from './components/InputMenu';
import { Menus } from './components/Menus';
import InfoWindow from './components/InfoWindow'; // Import the InfoWindow component

const START_SCREEN = "paper";

function App() {
  const [appScreen, setScreen] = useState(START_SCREEN);
  const [paperReady, setPaperReady] = useState(false);
  const [file, setFile] = useState(null);
  const [svgContent, setSvgContent] = useState(null); // State for SVG content
  const [processedInput, setProcessedInput] = useState(null); // Store processed input from InputMenu

  // Handle file change
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file submission for CSV
  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:8000/plot-logs/', { 
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const svg = await response.text();
      setSvgContent(svg);
    } else {
      console.error('File upload failed');
    }
  };

  // Handle submission for other plot
  const handleOtherPlot = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:8000/plot-other-log/', { 
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const svg = await response.text();
      setSvgContent(svg);
    } else {
      console.error('File upload failed');
    }
  };

  // Handle input processing from InputMenu
  const handleProcessInput = (input) => {
    setProcessedInput(input);
  };

  return (
    <div className="App">
      {/* Informational Window */}
      <InfoWindow />

      {appScreen === "paper" && (
        <View icon="" goToScreen="" screen={appScreen} setScreen={setScreen}>
          <PaperCanvas setPaperReady={setPaperReady} />
          {paperReady && (
            <CreateGridBG 
              paper={paperReady} 
              paperReady={paperReady}
            />
          )}

          {/* Draggable Menu for FileUpload */}
          <Draggable>
            <div 
              className="draggable-menu" 
              style={{
                position: 'absolute', 
                zIndex: 10, 
                backgroundColor: '#fff', 
                padding: '20px', 
                borderRadius: '8px', 
                boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
                top: '100px',
                left: '50px'
              }}
            >
              <h3>File Upload Menu</h3>
              <Menus 
                handleFileChange={handleFileChange} 
                handleSubmit={handleSubmit} 
                handleOtherPlot={handleOtherPlot} 
                file={file} 
                svgContent={svgContent} 
              />
            </div>
          </Draggable>

          {/* Draggable Menu for InputMenu */}
          <Draggable>
            <div 
              className="draggable-menu" 
              style={{
                position: 'absolute', 
                zIndex: 10, 
                backgroundColor: '#fff', 
                padding: '20px', 
                borderRadius: '8px', 
                boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
                top: '300px',
                left: '50px'
              }}
            >
              <h3>User Input Menu</h3>
              <InputMenu onProcessInput={handleProcessInput} />
            </div>
          </Draggable>

          {/* Optionally display the processed input */}
          {processedInput && (
            <div style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px' }}>
              <h4>Processed Input:</h4>
              <p>{processedInput}</p>
            </div>
          )}
        </View>
      )}
    </div>
  );
}

export default App;
