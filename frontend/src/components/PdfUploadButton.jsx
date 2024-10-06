import React from 'react';
import { Button, List, ListItem, ListItemText, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const PdfUploadButton = ({ pdfFiles, handlePdfChange, handleRemovePdf }) => {
  return (
    <div>
      <Button
        variant="contained"
        component="label"
        fullWidth
        style={{ margin: '16px 0' }}
      >
        {pdfFiles.length > 0 ? `${pdfFiles.length} PDF(s) selected` : 'Upload PDF Files'}
        <input
          type="file"
          hidden
          multiple
          accept="application/pdf"
          onChange={handlePdfChange}
        />
      </Button>

      {pdfFiles.length > 0 && (
        <List>
          {Array.from(pdfFiles).map((file, index) => (
            <ListItem key={index} secondaryAction={
              <IconButton edge="end" aria-label="delete" onClick={() => handleRemovePdf(index)}>
                <DeleteIcon />
              </IconButton>
            }>
              <ListItemText primary={file.name} />
            </ListItem>
          ))}
        </List>
      )}
    </div>
  );
};

export default PdfUploadButton;
