import React, { useState } from 'react';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [svgContent, setSvgContent] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file.");
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/plot-logs/', { 
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const svg = await response.text();
        setSvgContent(svg);
      }
    } catch (error) {
      console.error('Error uploading the file', error);
    }
  };

  const handleOtherPlot = async () => {
    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/plot-other-log/', { 
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const svg = await response.text();
        setSvgContent(svg);
      }
    } catch (error) {
      console.error('Error uploading the file', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={handleOtherPlot}>Other Plot</button>

      {svgContent && (
        <div 
          dangerouslySetInnerHTML={{ __html: svgContent }} 
          style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px' }}
        />
      )}
    </div>
  );
};

export default FileUpload;





