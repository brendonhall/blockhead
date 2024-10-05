let paper = require('paper');

function setupPaper(canvasRef) {
  // explicitly set the attr width/height
    canvasRef.current.height = canvasRef.current.parentElement.height;
    canvasRef.current.width = canvasRef.current.parentElement.width;
    paper.setup(canvasRef.current);
    paper.view.zoom = 1;
    return paper;
}

export { setupPaper };