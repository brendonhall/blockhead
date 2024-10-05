import React from 'react';
import { Icon, Button, Modal, ButtonGroup } from 'semantic-ui-react';
import paper from 'paper';

const PaperControls = () => {
  const trashInteraction = () => {
    paper.project.clear();
  };

  // const handleExportSVG = (selectedColor) => {
  // };
  

  return (
    <div>
      <Modal
        trigger={<Button color='red' icon><Icon name='trash' />Restart</Button>}
        header='Are you sure you want to destroy your masterpiece?'
        content='This action cannot be undone.'
        actions={['Keep It', { key: 'done', content: 'Nuke It', positive: true, onClick: trashInteraction }]}
      />
      {/* <ButtonGroup>
        <Button icon onClick={()=>handleExportSVG(selectedColor)}>
          <Icon name='download' />
          SVG
        </Button>
      </ButtonGroup> */}
    </div>
  );
};

export { PaperControls };