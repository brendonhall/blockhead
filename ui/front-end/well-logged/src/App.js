import './App.css';
import 'semantic-ui-css/semantic.min.css';
import { useState } from 'react';
import { PaperCanvas } from './components/PaperCanvas.jsx';
import { View } from './components/View.jsx';
import { CreateGridBG } from './interactions/CreateGridBG.jsx';
import { Menus } from './components/Menus.jsx';
import Draggable from 'react-draggable';

const START_SCREEN = "paper";

function App() {
  const [appScreen, setScreen] = useState(START_SCREEN);
  const [paperReady, setPaperReady] = useState(false);
  const [file, setFile] = useState(null);
  const [svgContent, setSvgContent] = useState(null); // State for SVG content

  // File upload handling logic from FileUpload component
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:8000/plot-logs/', { 
        method: 'POST',
        body: formData,
    });        

    if (response.ok) {
        console.log('File uploaded successfully');
        const svg = await response.text();
        setSvgContent(svg);  // Set the SVG content to display in UI
    } else {
        console.error('File upload failed');
        const errorText = await response.text();
        console.error('Response Text:', errorText);
    }
  };

  const handleOtherPlot = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:8000/plot-other-log/', { 
        method: 'POST',
        body: formData,
    });        

    if (response.ok) {
        console.log('File uploaded successfully');
        const svg = await response.text();
        setSvgContent(svg);  // Set the SVG content to display in UI
    } else {
        console.error('File upload failed');
        const errorText = await response.text();
        console.error('Response Text:', errorText);
    }
  };

  return (
    <div className="App">
      {appScreen === "paper" && (
        <View icon="" goToScreen="" screen={appScreen} setScreen={setScreen}>
          <PaperCanvas setPaperReady={setPaperReady} />
          {paperReady && (
            <CreateGridBG 
              paper={paperReady} 
              paperReady={paperReady}
            />
          )}
          {/* Draggable Menu */}
          <Draggable>
            <div className="draggable-menu" style={{ position: 'absolute', zIndex: 10, backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0,0,0,0.2)' }}>
              <Menus 
                handleFileChange={handleFileChange} 
                handleSubmit={handleSubmit} 
                handleOtherPlot={handleOtherPlot}
                file={file} 
                svgContent={svgContent}  // Pass SVG content to Menus for display
              />
            </div>
          </Draggable>
        </View>
      )}
    </div>
  );
}

export default App;









