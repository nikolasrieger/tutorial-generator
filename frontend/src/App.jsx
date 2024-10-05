import React, { useState } from 'react';
import { Container, Button, Typography, CircularProgress, Box, AppBar, Toolbar, TextField } from '@mui/material';
import axios from 'axios';
import UrlInput from './components/UrlInput';
import PdfUploadButton from './components/PdfUploadButton';

const App = () => {
  const [urls, setUrls] = useState([]);
  const [pdfFiles, setPdfFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [error, setError] = useState('');
  const [topic, setTopic] = useState(''); 

  const handlePdfChange = (e) => {
    setPdfFiles(e.target.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAudioFile(null);

    const formData = new FormData();
    formData.append('urls', urls);
    formData.append('topic', topic); 

    for (let i = 0; i < pdfFiles.length; i++) {
      formData.append('pdf_files', pdfFiles[i]);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAudioFile(response.data.audio_file); 
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
    setLoading(false);
  };

  const handleDownload = () => {
    if (audioFile) {
      const byteString = atob(audioFile);
      const buffer = new ArrayBuffer(byteString.length);
      const uintArray = new Uint8Array(buffer);

      for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
      }

      const blob = new Blob([uintArray], { type: 'audio/mp3' }); 
      const url = URL.createObjectURL(blob); 

      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'generated_audio.mp3'); 
      document.body.appendChild(link);
      link.click();  
      document.body.removeChild(link); 
    }
  };

  return (
    <>
      <AppBar position="sticky" style={{ width: '100%' }}>
        <Toolbar>
          <Typography variant="h4" style={{ flexGrow: 1 }}>
            Teachify
          </Typography>
        </Toolbar>
      </AppBar>

      <Box sx={{ mx: 2,  marginTop: 5 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Topic"
            variant="outlined"
            fullWidth
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            style={{ marginBottom: '16px' }} 
          />

          <UrlInput urls={urls} setUrls={setUrls} />

          <PdfUploadButton pdfFiles={pdfFiles} handlePdfChange={handlePdfChange} />

          {loading ? (
            <Box textAlign="center" mt={2}>
              <CircularProgress />
            </Box>
          ) : (
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              style={{ margin: '16px 0' }}
            >
              Process Content
            </Button>
          )}
        </form>

        {error && (
          <Typography color="error" align="center" mt={2}>
            {error}
          </Typography>
        )}

        {audioFile && (
          <Box mt={4} display="flex" alignItems="center" justifyContent="center">
            <audio controls src={`data:audio/mp3;base64,${audioFile}`} style={{ marginLeft: '16px' }} />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleDownload}
              style={{ marginLeft: '16px' }}
            >
              Download MP3
            </Button>
          </Box>
        )}
      </Box>
    </>
  );
};

export default App;
