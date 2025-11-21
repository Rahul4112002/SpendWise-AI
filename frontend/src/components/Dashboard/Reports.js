import React from 'react';

const Reports = () => {
  return (
    <div style={styles.container}>
      <h1>Financial Reports</h1>
      <div style={styles.content}>
        <div style={styles.card}>
          <h3>📊 Monthly Report</h3>
          <p>View detailed monthly financial analysis</p>
          <button style={styles.button}>Generate Report</button>
        </div>
        
        <div style={styles.card}>
          <h3>📈 Spending Trends</h3>
          <p>Analyze your spending patterns over time</p>
          <button style={styles.button}>View Trends</button>
        </div>
        
        <div style={styles.card}>
          <h3>💰 Budget Analysis</h3>
          <p>Compare budgets vs actual spending</p>
          <button style={styles.button}>View Analysis</button>
        </div>
        
        <div style={styles.card}>
          <h3>📄 Export Data</h3>
          <p>Download your financial data as CSV/PDF</p>
          <button style={styles.button}>Export</button>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  content: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '20px',
    marginTop: '20px',
  },
  card: {
    background: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textAlign: 'center',
  },
  button: {
    marginTop: '15px',
    padding: '10px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};

export default Reports;
