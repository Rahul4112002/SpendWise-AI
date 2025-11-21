import React, { useState } from 'react';
import axios from 'axios';

const UploadStatement = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/v1/bank-statements/upload', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setMessage(`✅ Upload successful! ${response.data.total_transactions} transactions extracted.`);
      setFile(null);
    } catch (error) {
      setMessage('❌ Upload failed: ' + (error.response?.data?.detail || 'Unknown error'));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Upload Bank Statement</h1>
      <div style={styles.uploadBox}>
        <h3>📄 Upload PDF Bank Statement</h3>
        <p style={styles.description}>
          Upload your bank statement PDF to automatically extract and categorize transactions
        </p>
        
        <form onSubmit={handleUpload} style={styles.form}>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            style={styles.fileInput}
          />
          
          {file && (
            <p style={styles.fileName}>Selected: {file.name}</p>
          )}
          
          <button 
            type="submit" 
            disabled={!file || uploading}
            style={{...styles.button, opacity: (!file || uploading) ? 0.5 : 1}}
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>
        </form>
        
        {message && (
          <div style={message.includes('✅') ? styles.successMessage : styles.errorMessage}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    maxWidth: '600px',
    margin: '0 auto',
  },
  uploadBox: {
    background: 'white',
    padding: '40px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textAlign: 'center',
  },
  description: {
    color: '#666',
    marginBottom: '30px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  fileInput: {
    padding: '10px',
    border: '2px dashed #667eea',
    borderRadius: '8px',
    cursor: 'pointer',
  },
  fileName: {
    color: '#667eea',
    fontWeight: 'bold',
  },
  button: {
    padding: '14px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '600',
  },
  successMessage: {
    marginTop: '20px',
    padding: '15px',
    background: '#d4edda',
    color: '#155724',
    borderRadius: '8px',
  },
  errorMessage: {
    marginTop: '20px',
    padding: '15px',
    background: '#f8d7da',
    color: '#721c24',
    borderRadius: '8px',
  },
};

export default UploadStatement;
