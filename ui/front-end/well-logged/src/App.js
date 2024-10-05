import './App.css';
import 'semantic-ui-css/semantic.min.css';

import { useState } from 'react';
import {PaperCanvas} from './components/PaperCanvas.jsx';
import {View} from './components/View.jsx'; 
import { CreateGridBG } from './interactions/CreateGridBG.jsx';
import FileUpload from './interactions/UploadFile.jsx';

const START_SCREEN = "paper";

function App() {
  const [appScreen, setScreen] = useState(START_SCREEN);
  const [paperReady, setPaperReady] = useState(false);

  return (
    <div className="App">
      {appScreen === "paper" && (
        <View icon="" goToScreen="" screen={appScreen} setScreen={setScreen}>
          <FileUpload/>
          <PaperCanvas setPaperReady={setPaperReady} />

          {paperReady && (
            <CreateGridBG 
              paper={paperReady} 
              paperReady={paperReady}
            />
          )}
        </View>
      )}
    </div>
  );
}

export default App;