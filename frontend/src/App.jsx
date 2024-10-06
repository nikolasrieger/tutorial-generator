import React, { useState } from 'react';
import { Button, Typography, CircularProgress, Box, AppBar, Toolbar, TextField, Switch, FormControlLabel, Container, Paper } from '@mui/material';
import axios from 'axios';
import UrlInput from './components/UrlInput';
import PdfUploadButton from './components/PdfUploadButton';
import './App.scss'; 
import './App.css'; 

const App = () => {
  const [urls, setUrls] = useState([]);
  const [pdfFiles, setPdfFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [error, setError] = useState('');
  const [topic, setTopic] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [tone, setTone] = useState('');
  const [length, setLength] = useState('');
  const [showExtraFields, setShowExtraFields] = useState(false);

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

    if (showExtraFields) {
      formData.append('target_audience', targetAudience);
      formData.append('tone', tone);
      formData.append('length', length);
    }

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
    <div className="app-container">
      <div className="stars">
        {Array.from({ length: 50 }).map((_, index) => (
          <div className="star" key={index}></div>
        ))}
      </div>

      <AppBar position="sticky" sx={{ backgroundColor: '#3f51b5', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)' }}>
        <Toolbar>
          <Typography variant="h4" sx={{ flexGrow: 1, color: '#fff', textAlign: 'left', letterSpacing: '2px' }}>
            Teachify
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ marginTop: 5 }}>
        <Paper elevation={12} sx={{
          padding: 4,
          borderRadius: 3,
          background: 'rgba(255, 255, 255, 0.8)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-10px)',
          },
        }}>
          <div className="form-container">
            <form onSubmit={handleSubmit}>

              <TextField
                label="Topic"
                variant="outlined"
                fullWidth
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                sx={{ marginBottom: 3 }}
              />

              <UrlInput urls={urls} setUrls={setUrls} />
              <PdfUploadButton pdfFiles={pdfFiles} handlePdfChange={handlePdfChange} />

              <FormControlLabel
                control={<Switch checked={showExtraFields} onChange={() => setShowExtraFields(!showExtraFields)} />}
                label="Advanced Options"
                sx={{ marginTop: 3, color: '#3f51b5' }}
              />

              {showExtraFields && (
                <>
                  <TextField
                    label="Target Audience"
                    variant="outlined"
                    fullWidth
                    value={targetAudience}
                    onChange={(e) => setTargetAudience(e.target.value)}
                    sx={{ marginBottom: 3 }}
                  />

                  <TextField
                    label="Tone"
                    variant="outlined"
                    fullWidth
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                    sx={{ marginBottom: 3 }}
                  />

                  <TextField
                    label="Approximate Length (in min)"
                    variant="outlined"
                    fullWidth
                    value={length}
                    onChange={(e) => setLength(e.target.value)}
                    sx={{ marginBottom: 3 }}
                  />
                </>
              )}

              {loading ? (
                <Box textAlign="center" mt={2}>
                  <CircularProgress size={60} thickness={5} sx={{ color: '#3f51b5' }} />
                </Box>
              ) : (
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    margin: '16px 0',
                    padding: '14px',
                    fontWeight: 'bold',
                    background: 'linear-gradient(45deg, #3f51b5, #2196f3)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #303f9f, #1976d2)',
                      transform: 'scale(1.05)',
                    },
                  }}
                >
                  Process Content
                </Button>
              )}
            </form>
          </div>

          {error && (
            <Typography color="error" align="center" mt={2} sx={{ marginBottom: 3 }}>
              {error}
            </Typography>
          )}

          {audioFile && (
            <Box mt={4} display="flex" alignItems="center" justifyContent="center" sx={{ marginBottom: 3 }}>
              <audio controls src={`data:audio/mp3;base64,${audioFile}`} style={{ marginLeft: '16px' }} />
              <Button
                variant="contained"
                color="secondary"
                onClick={handleDownload}
                sx={{ marginLeft: '16px' }}
              >
                Download MP3
              </Button>
            </Box>
          )}
        </Paper>
      </Container>
    </div>
  );
};

export default App;
