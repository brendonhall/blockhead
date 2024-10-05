import { useState } from 'react';
// STYLE LIBRARIES
import { Button, ButtonGroup, Label, Input} from 'semantic-ui-react';
import { FaRegSquare, FaRegCircle } from "react-icons/fa"; 
import { FiHexagon } from "react-icons/fi";
import { LuPaintBucket } from "react-icons/lu";
import { IoBrushOutline } from "react-icons/io5";
import { PiCylinderFill } from "react-icons/pi";
import { IoMoveSharp } from "react-icons/io5";
// COMPONENTS
import { ToolBarSubMenu } from './ToolBarSubMenu.jsx';
import { ParameterSlider, LabeledParameter } from './ParameterSlider.jsx'; 
import { fillTool } from '../interactions/FillTool.js';
import { lineTool } from '../interactions/LineTool.js';
import { beadTool } from '../interactions/BeadTool.js';
import { panTool } from '../interactions/PanTool.js';
import { ZoomControls } from './ZoomControls.js';
import { PaperControls } from './PaperControls.jsx';

// PARAMETERS
import { BEAD_COLORS} from '../AppConfig.jsx';
import { useEffect } from 'react';


const ColorPicker = ({ selectedColor, setSelectedColor }) => {
    const colors = BEAD_COLORS;
  
    return (
      <div className='fwh cr'>
        {colors.map(color => (
          <button
            key={color}
            className={`bead ${selectedColor === color ? "active" : ""}`}
            style={{ backgroundColor: color}}
            onClick={() => setSelectedColor(color)}
          >
            <div className='hole'></div>
          </button>
        ))}
      </div>
    );
  };

const Menus = ({paper, beadParameters, setBeadParameters, selectedColor, setSelectedColor, gridVisible, setGridVisible}) => {
    const setGridSize = (value)=> setBeadParameters({...beadParameters, gridSize: value});
    const setBeadSpacing = (value)=>setBeadParameters({...beadParameters, beadSpacing: value});
    const setCreateGridType = (value)=>setBeadParameters({...beadParameters, createGridType: value});
    const setThickness = (value)=>setBeadParameters({...beadParameters, thickness: value, inner_radius: beadParameters.outer_radius - value});
    const [currentTool, setCurrentTool] = useState('beadTool');
    const [projectName, setProjectName] = useState('MyBeadProject');
    const [version, setVersion] = useState("1");

    useEffect(() => { 
      if(paper){
        const lineT = lineTool(selectedColor);
        const fillT = fillTool(selectedColor);
        const beadT = beadTool(selectedColor);
        const panT = panTool(selectedColor);
      }
    }, [paper]);

    useEffect(() => {
      if(paper && currentTool){
        paper.tools.forEach(tool =>{
          if(tool.name === currentTool){
            tool.activate();
          }
        });
      }
    }, [paper, currentTool]);

    return (
        <>
         
        {/* TOOLS */}
        <ToolBarSubMenu id="Tools" name='Tools'>
          <LabeledParameter label='Project Name'>
            <Input type="text" value={projectName} onChange={(e)=>setProjectName(e.target.value)}/>
          </LabeledParameter>
          <LabeledParameter label='Version'>
            <Input type="number" value={version} onChange={(e)=>setVersion(e.target.value)}/>
          </LabeledParameter>
          <LabeledParameter label='Controls'>
            <PaperControls projectName={projectName} version={version} selectedColor={selectedColor}/>
          </LabeledParameter>
          <LabeledParameter label='Zoom'>
            <ZoomControls />
          </LabeledParameter>
          <LabeledParameter label='MarqueePlace'>
            <Button color={currentTool === "fillTool" ? "green" : ""} icon onClick={() => setCurrentTool("fillTool")}><LuPaintBucket /></Button>
          </LabeledParameter>
          <LabeledParameter label='BrushPlace'>
            <Button color={currentTool === "brushTool" ? "green" : ""} icon onClick={() => setCurrentTool("brushTool")}><IoBrushOutline /></Button>
          </LabeledParameter>
          <LabeledParameter label='BeadPlace'>
            <Button color={currentTool === "beadTool" ? "green" : ""} icon onClick={() => setCurrentTool("beadTool")}><PiCylinderFill /></Button>
          </LabeledParameter>
          <LabeledParameter label='Pan'>
            <Button color={currentTool === "panTool" ? "green" : ""} icon onClick={() => setCurrentTool("panTool")}><IoMoveSharp /> </Button>
          </LabeledParameter>
        </ToolBarSubMenu>


         
         {/* PEGBOARD */}
         <ToolBarSubMenu id="PegboardControls" name='Pegboard' initVisible={true}>
 
            <LabeledParameter label='Size'>
                <ParameterSlider 
                    value={beadParameters.gridSize} 
                    setValue={setGridSize} 
                    minValue={5} 
                    maxValue={25}
                    stepValue={1}
                    parser={parseInt}
                />
                {beadParameters.gridSize.toFixed(0)} x {beadParameters.gridSize.toFixed(0)}
            </LabeledParameter>


            <LabeledParameter label='Spacing'>
                <ParameterSlider 
                    value={beadParameters.beadSpacing} 
                    setValue={setBeadSpacing} 
                    minValue={-1} 
                    maxValue={1.5}
                    stepValue={0.05}
                />
                {beadParameters.beadSpacing.toFixed(2)} mm
            </LabeledParameter>


            <LabeledParameter label='Visibility'>
                <ParameterSlider 
                    value={gridVisible} 
                    setValue={setGridVisible} 
                    minValue={0} 
                    maxValue={1}
                    stepValue={0.1}
                />
                <Button basic icon={`eye ${gridVisible ? "" : "slash"}`} onClick={()=>setGridVisible(!gridVisible)}/>
            </LabeledParameter>

            
            <LabeledParameter label='Shape'>
                <ButtonGroup>
                    <Button color='red' icon onClick={() => setCreateGridType('square')}><FaRegSquare /></Button>
                    <Button color='green' icon onClick={() => setCreateGridType('circular')}><FaRegCircle /></Button>
                    <Button color='blue' icon onClick={() => setCreateGridType('hexagonal')}><FiHexagon /></Button> 
                </ButtonGroup>
                <Label basic>{beadParameters.createGridType}</Label>
            </LabeledParameter>


        </ToolBarSubMenu>
        



        {/* BEADS */}
        <ToolBarSubMenu id="BeadControls" name='Beads'>
            <LabeledParameter label='Thickness'>

            <ParameterSlider 
                // value={beadParameters.thickness} 
                // setValue={setThickness} 
                // minValue={0.1} 
                // maxValue={beadParameters.outer_radius}
                // stepValue={0.05}
            />
            {beadParameters.thickness.toFixed(2)} mm
            </LabeledParameter>
            
          <ColorPicker selectedColor={selectedColor} setSelectedColor={setSelectedColor} />
        </ToolBarSubMenu>
        </>
    )
}

export {Menus};