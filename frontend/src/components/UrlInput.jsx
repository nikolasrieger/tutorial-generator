import React, { useState } from 'react';
import { TextField, Box, Chip, Typography } from '@mui/material';

const UrlInput = ({ urls, setUrls }) => {
  const [currentUrl, setCurrentUrl] = useState('');

  const handleAddUrl = (e) => {
    if ((e.key === 'Enter' || e.key === ' ') && currentUrl.trim()) {
      setUrls([...urls, currentUrl.trim()]); 
      setCurrentUrl('');  
      e.preventDefault();  
    }
  };

  const handleDeleteUrl = (urlToDelete) => {
    setUrls(urls.filter((url) => url !== urlToDelete));  
  };

  return (
    <Box>
      <TextField
        label="Enter URLs"
        variant="outlined"
        fullWidth
        value={currentUrl}
        onChange={(e) => setCurrentUrl(e.target.value)}
        onKeyPress={handleAddUrl}
        margin="normal"
      />

      {urls.length > 0 && (
        <Box mt={2}>
          <Typography variant="body1" gutterBottom>
            Added URLs:
          </Typography>
          {urls.map((url, index) => (
            <Chip
              key={index}
              label={url}
              onDelete={() => handleDeleteUrl(url)}
              style={{ margin: '4px' }}
            />
          ))}
        </Box>
      )}
    </Box>
  );
};

export default UrlInput;
