import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ExpenseTracker = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/transactions', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTransactions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch transactions', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.container}>Loading transactions...</div>;
  }

  return (
    <div style={styles.container}>
      <h1>Transaction History</h1>
      <div style={styles.transactionsList}>
        {transactions.length === 0 ? (
          <p style={styles.emptyState}>No transactions yet. Start tracking your expenses!</p>
        ) : (
          transactions.map((transaction) => (
            <div key={transaction.id} style={styles.transactionItem}>
              <div>
                <h4>{transaction.merchant_name || 'Unknown Merchant'}</h4>
                <p style={styles.category}>{transaction.category}</p>
                <p style={styles.date}>
                  {new Date(transaction.transaction_date).toLocaleDateString()}
                </p>
              </div>
              <div style={styles.amount}>
                <span style={transaction.transaction_type === 'debit' ? styles.debit : styles.credit}>
                  {transaction.transaction_type === 'debit' ? '-' : '+'}₹
                  {transaction.amount.toLocaleString()}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    maxWidth: '1000px',
    margin: '0 auto',
  },
  transactionsList: {
    background: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  transactionItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    borderBottom: '1px solid #eee',
  },
  category: {
    color: '#666',
    fontSize: '14px',
    textTransform: 'capitalize',
  },
  date: {
    color: '#999',
    fontSize: '12px',
  },
  amount: {
    fontSize: '18px',
    fontWeight: 'bold',
  },
  debit: {
    color: '#e74c3c',
  },
  credit: {
    color: '#27ae60',
  },
  emptyState: {
    textAlign: 'center',
    padding: '40px',
    color: '#999',
  },
};

export default ExpenseTracker;
