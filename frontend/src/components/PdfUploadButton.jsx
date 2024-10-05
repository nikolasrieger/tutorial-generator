import React from 'react';
import { Button } from '@mui/material';

const PdfUploadButton = ({ pdfFiles, handlePdfChange }) => {
  return (
    <Button
      variant="contained"
      component="label"
      fullWidth
      style={{ margin: '16px 0' }}
      disabled={true}
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
  );
};

export default PdfUploadButton;
