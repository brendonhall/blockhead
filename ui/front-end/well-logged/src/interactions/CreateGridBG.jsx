import { useEffect } from 'react';

const createGrid = (paper) => {
    console.log('Creating grid...');
    const cellSize = 20;
    const gridSizeX = paper.view.bounds.width;
    const gridSizeY = paper.view.bounds.height;

    // Loop through grid (size of paper) and place a small dot at each intersection
    for (let y = 0; y <= gridSizeY; y += cellSize) {
        for (let x = 0; x <= gridSizeX; x += cellSize) {
            // Create a circle at each intersection
            new paper.Path.Circle({
            center: new paper.Point(x, y),
            radius: 1.5,
            fillColor: new paper.Color(0, 0, 0, 0.1),
            name: 'gridDot',
            });
        }
    }
};

const CreateGridBG = ({ paper, paperReady }) => {
    useEffect(() => {
        if (paperReady) {
            createGrid(paper);
        }
    }, [paperReady]);

    return null;
};

export { CreateGridBG };








