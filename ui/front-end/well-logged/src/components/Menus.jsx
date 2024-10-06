import { Button, Input } from 'semantic-ui-react';

const Menus = ({ handleFileChange, handleSubmit, handleOtherPlot, file, svgContent }) => {
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <Input 
          type="file" 
          accept=".csv, .svg" 
          onChange={handleFileChange} 
        />
        {file && <p>Selected file: {file.name}</p>}
        <Button type="submit" primary>
          Upload CSV
        </Button>
        <Button type="button" onClick={handleOtherPlot} secondary>
          Upload for Other Plot
        </Button>
      </form>

      {/* Display the SVG content if available */}
      {svgContent && (
        <div 
          dangerouslySetInnerHTML={{ __html: svgContent }} 
          style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px' }}
        />
      )}
    </div>
  );
};

export { Menus };






