import React, { useState } from 'react';
import {
  Button,
  Typography,
  CircularProgress,
  Box,
  AppBar,
  Toolbar,
  TextField,
  Switch,
  FormControlLabel,
  Container,
  Paper,
  IconButton,
} from '@mui/material';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import RefreshIcon from '@mui/icons-material/Refresh';
import axios from 'axios';
import UrlInput from './components/UrlInput';
import PdfUploadButton from './components/PdfUploadButton';
import FeedbackDialog from './components/FeedbackDialog'; 
import './App.scss';
import './App.css';

const App = () => {
  const [urls, setUrls] = useState([]);
  const [pdfFiles, setPdfFiles] = useState([]);
  const [pdfBase64Files, setPdfBase64Files] = useState([]);  // New state for base64 encoded PDFs
  const [loading, setLoading] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [error, setError] = useState('');
  const [topic, setTopic] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [tone, setTone] = useState('');
  const [length, setLength] = useState('');
  const [showExtraFields, setShowExtraFields] = useState(false);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false); 
  const [feedbackType, setFeedbackType] = useState('');
  const [promptID, setPromptID] = useState('');

  // Function to handle PDF upload
  const handlePdfChange = (e) => {
    const files = e.target.files;
    setPdfFiles(files);
    convertFilesToBase64(files);  // Convert to base64
  };

  // Function to convert PDF files to Base64
  const convertFilesToBase64 = (files) => {
    const base64Files = [];
    const fileReaders = Array.from(files).map(file => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          resolve(reader.result.split(',')[1]); // Exclude the "data:application/pdf;base64," part
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    });

    Promise.all(fileReaders)
      .then(base64FilesArray => {
        setPdfBase64Files(base64FilesArray);
      })
      .catch(error => console.error("Error converting files to base64:", error));
  };

  // Function to remove a selected PDF
  const handleRemovePdf = (index) => {
    const newPdfFiles = Array.from(pdfFiles).filter((_, i) => i !== index);
    const newPdfBase64Files = pdfBase64Files.filter((_, i) => i !== index);
    setPdfFiles(newPdfFiles);
    setPdfBase64Files(newPdfBase64Files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAudioFile(null);
    setFeedbackSubmitted(false); 

    const formData = new FormData();
    formData.append('urls', urls);
    formData.append('topic', topic);

    if (showExtraFields) {
      formData.append('target_audience', targetAudience);
      formData.append('tone', tone);
      formData.append('length', length);
    }

    // Attach the base64 PDFs
    for (let i = 0; i < pdfBase64Files.length; i++) {
      formData.append('pdf_files', pdfBase64Files[i]);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAudioFile(response.data.audio_file);
      setPromptID(response.data.prompt_id);
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

  const openFeedbackDialog = (type) => {
    if (!feedbackSubmitted) {
      setFeedbackType(type);
      setFeedbackDialogOpen(true);
    }
  };

  const closeFeedbackDialog = () => {
    setFeedbackDialogOpen(false);
  };

  const handleFeedbackSubmit = async (comment) => {
    try {
      await axios.post('http://127.0.0.1:5000/submit_feedback', {
        prompt_id: promptID,
        feedback_type: feedbackType,
        comment: comment || '',
      });
      setFeedbackSubmitted(true); 
    } catch (error) {
      console.error('Failed to submit feedback:', error.response || error);
    }
    closeFeedbackDialog();
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
              <PdfUploadButton
                pdfFiles={pdfFiles}
                handlePdfChange={handlePdfChange}
                handleRemovePdf={handleRemovePdf}
              />

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

              <IconButton
                onClick={() => openFeedbackDialog('like')}
                disabled={feedbackSubmitted}
                sx={{ marginLeft: '16px' }}
              >
                <ThumbUpIcon color={feedbackSubmitted ? 'disabled' : 'primary'} fontSize="large" />
              </IconButton>
              <IconButton
                onClick={() => openFeedbackDialog('dislike')}
                disabled={feedbackSubmitted} 
                sx={{ marginLeft: '8px' }}
              >
                <ThumbDownIcon color={feedbackSubmitted ? 'disabled' : 'error'} fontSize="large" />
              </IconButton>
              
              <IconButton
                onClick={handleSubmit}
                sx={{ marginLeft: '8px' }}
              >
                <RefreshIcon color="primary" fontSize="large" />
              </IconButton>
            </Box>
          )}
        </Paper>
      </Container>

      <FeedbackDialog
        open={feedbackDialogOpen}
        onClose={closeFeedbackDialog}
        onSubmit={handleFeedbackSubmit}
      />
    </div>
  );
};

export default App;
