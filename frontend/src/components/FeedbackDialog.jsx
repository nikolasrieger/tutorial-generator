import React, { useState } from 'react';
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  Typography,
  TextField,
} from '@mui/material';

const FeedbackDialog = ({ open, onClose, onSubmit }) => {
  const [comment, setComment] = useState(''); // State for comment input

  const handleSend = () => {
    onSubmit(comment); // Pass the comment to the parent component
    setComment(''); // Clear the comment after submission
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Feedback</DialogTitle>
      <DialogContent>
        <Typography variant="body1">
          Do you want to send your feedback?
        </Typography>
        <TextField
          label="Comment (optional)"
          variant="outlined"
          fullWidth
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          sx={{ marginTop: 2 }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Skip
        </Button>
        <Button onClick={handleSend} color="primary">
          Send
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default FeedbackDialog;
