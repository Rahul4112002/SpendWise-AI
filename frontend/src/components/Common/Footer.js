import React from 'react';

const Footer = () => {
  return (
    <footer style={styles.footer}>
      <div style={styles.container}>
        <p style={styles.text}>
          © 2024 PennyWise AI - Autonomous Financial Coaching for Everyone
        </p>
        <p style={styles.subtext}>
          Powered by AI | Built for Gig Workers & Informal Sector
        </p>
      </div>
    </footer>
  );
};

const styles = {
  footer: {
    background: '#2d3748',
    color: 'white',
    padding: '2rem',
    marginTop: 'auto',
    textAlign: 'center',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  text: {
    margin: '0 0 0.5rem 0',
    fontSize: '1rem',
  },
  subtext: {
    margin: 0,
    fontSize: '0.875rem',
    opacity: 0.7,
  },
};

export default Footer;
