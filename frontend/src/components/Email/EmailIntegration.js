import React, { useState } from 'react';
import axios from 'axios';

const EmailIntegration = () => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const [emailData, setEmailData] = useState({
    email: '',
    appPassword: '',
    days: 60,
  });
  
  const [passwordInfo, setPasswordInfo] = useState({
    dateOfBirth: '',
    mobileNumber: '',
    accountNumber: '',
    panCard: '',
    customPassword: '',
  });

  const handleEmailChange = (e) => {
    setEmailData({
      ...emailData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordInfoChange = (e) => {
    setPasswordInfo({
      ...passwordInfo,
      [e.target.name]: e.target.value,
    });
  };

  const fetchStatements = async () => {
    setLoading(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        '/api/v1/email/fetch-statements',
        {
          email_credentials: {
            email: emailData.email,
            app_password: emailData.appPassword,
            days: parseInt(emailData.days),
          },
          pdf_password_info: {
            date_of_birth: passwordInfo.dateOfBirth || null,
            mobile_number: passwordInfo.mobileNumber || null,
            account_number: passwordInfo.accountNumber || null,
            pan_card: passwordInfo.panCard || null,
            custom_password: passwordInfo.customPassword || null,
          },
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setResult(response.data);
      setStep(3);
    } catch (error) {
      setResult({
        error: true,
        message: error.response?.data?.detail || 'Failed to fetch statements',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>📧 Automated Email Statement Import</h1>
      <p style={styles.subtitle}>
        Automatically fetch and process bank statements from your email
      </p>

      {/* Step 1: Email Credentials */}
      {step === 1 && (
        <div style={styles.stepContainer}>
          <h2>Step 1: Email Setup</h2>
          
          <div style={styles.infoBox}>
            <h3>🔐 Gmail App Password Setup:</h3>
            <ol style={styles.instructions}>
              <li>Go to <a href="https://myaccount.google.com/security" target="_blank" rel="noopener noreferrer">Google Account Security</a></li>
              <li>Enable <strong>2-Step Verification</strong></li>
              <li>Search for <strong>"App Passwords"</strong></li>
              <li>Generate password for <strong>"Mail"</strong></li>
              <li>Copy the 16-character password</li>
            </ol>
          </div>

          <div style={styles.form}>
            <div style={styles.formGroup}>
              <label>Email Address</label>
              <input
                type="email"
                name="email"
                value={emailData.email}
                onChange={handleEmailChange}
                placeholder="your.email@gmail.com"
                style={styles.input}
                required
              />
            </div>

            <div style={styles.formGroup}>
              <label>App Password (16 characters)</label>
              <input
                type="password"
                name="appPassword"
                value={emailData.appPassword}
                onChange={handleEmailChange}
                placeholder="xxxx xxxx xxxx xxxx"
                style={styles.input}
                required
              />
              <small style={styles.hint}>NOT your regular Gmail password!</small>
            </div>

            <div style={styles.formGroup}>
              <label>Fetch Last (Days)</label>
              <select
                name="days"
                value={emailData.days}
                onChange={handleEmailChange}
                style={styles.input}
              >
                <option value="30">30 days</option>
                <option value="60">60 days (Recommended)</option>
                <option value="90">90 days</option>
                <option value="180">6 months</option>
              </select>
            </div>

            <button onClick={() => setStep(2)} style={styles.primaryButton}>
              Next: PDF Password Info →
            </button>
          </div>
        </div>
      )}

      {/* Step 2: PDF Password Info */}
      {step === 2 && (
        <div style={styles.stepContainer}>
          <h2>Step 2: PDF Password Information</h2>
          
          <div style={styles.infoBox}>
            <h3>🔑 Common Bank PDF Passwords:</h3>
            <ul style={styles.instructions}>
              <li><strong>ICICI/HDFC/Axis/SBI:</strong> Date of Birth (DDMMYYYY)</li>
              <li><strong>Kotak:</strong> DOB (DDMMYY) or Mobile Last 4</li>
              <li><strong>Yes Bank:</strong> Account Last 4 digits</li>
              <li><strong>Others:</strong> PAN Card or Custom Password</li>
            </ul>
            <p style={{marginTop: '10px', color: '#666'}}>
              ℹ️ We'll try common patterns automatically. Provide what you know!
            </p>
          </div>

          <div style={styles.form}>
            <div style={styles.formGroup}>
              <label>Date of Birth (DDMMYYYY) - Most Common</label>
              <input
                type="text"
                name="dateOfBirth"
                value={passwordInfo.dateOfBirth}
                onChange={handlePasswordInfoChange}
                placeholder="15041990"
                maxLength="8"
                style={styles.input}
              />
              <small style={styles.hint}>Example: 15041990 for 15 Apr 1990</small>
            </div>

            <div style={styles.formGroup}>
              <label>Mobile Number (Last 4 digits)</label>
              <input
                type="text"
                name="mobileNumber"
                value={passwordInfo.mobileNumber}
                onChange={handlePasswordInfoChange}
                placeholder="1234"
                maxLength="10"
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label>Account Number (Last 4 digits)</label>
              <input
                type="text"
                name="accountNumber"
                value={passwordInfo.accountNumber}
                onChange={handlePasswordInfoChange}
                placeholder="5678"
                maxLength="20"
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label>PAN Card Number</label>
              <input
                type="text"
                name="panCard"
                value={passwordInfo.panCard}
                onChange={handlePasswordInfoChange}
                placeholder="ABCDE1234F"
                maxLength="10"
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label>Custom Password (if you know)</label>
              <input
                type="password"
                name="customPassword"
                value={passwordInfo.customPassword}
                onChange={handlePasswordInfoChange}
                placeholder="Your custom PDF password"
                style={styles.input}
              />
            </div>

            <div style={styles.buttonGroup}>
              <button onClick={() => setStep(1)} style={styles.secondaryButton}>
                ← Back
              </button>
              <button onClick={fetchStatements} style={styles.primaryButton} disabled={loading}>
                {loading ? '🔄 Fetching Statements...' : '🚀 Fetch & Process Statements'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Results */}
      {step === 3 && result && (
        <div style={styles.stepContainer}>
          <h2>Results</h2>
          
          {result.error ? (
            <div style={styles.errorBox}>
              <h3>❌ Error</h3>
              <p>{result.message}</p>
              <button onClick={() => setStep(1)} style={styles.secondaryButton}>
                Try Again
              </button>
            </div>
          ) : (
            <div style={styles.successBox}>
              <h3>✅ {result.message}</h3>
              
              <div style={styles.statsGrid}>
                <div style={styles.statCard}>
                  <div style={styles.statNumber}>{result.total_emails_fetched}</div>
                  <div style={styles.statLabel}>Emails Scanned</div>
                </div>
                
                <div style={styles.statCard}>
                  <div style={styles.statNumber}>{result.statements_found}</div>
                  <div style={styles.statLabel}>Statements Found</div>
                </div>
                
                <div style={styles.statCard}>
                  <div style={styles.statNumber}>{result.statements_processed}</div>
                  <div style={styles.statLabel}>Successfully Processed</div>
                </div>
                
                <div style={styles.statCard}>
                  <div style={styles.statNumber}>{result.transactions_extracted}</div>
                  <div style={styles.statLabel}>Transactions Extracted</div>
                </div>
              </div>

              {result.failed_pdfs && result.failed_pdfs.length > 0 && (
                <div style={styles.warningBox}>
                  <h4>⚠️ Failed PDFs ({result.failed_pdfs.length})</h4>
                  <ul>
                    {result.failed_pdfs.map((pdf, index) => (
                      <li key={index}>{pdf}</li>
                    ))}
                  </ul>
                  <p style={{marginTop: '10px'}}>
                    Tip: Try uploading these manually or check password info
                  </p>
                </div>
              )}

              <div style={styles.buttonGroup}>
                <button onClick={() => setStep(1)} style={styles.secondaryButton}>
                  Fetch More
                </button>
                <button onClick={() => window.location.href = '/transactions'} style={styles.primaryButton}>
                  View Transactions →
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
  },
  subtitle: {
    color: '#666',
    fontSize: '1.1rem',
    marginBottom: '30px',
  },
  stepContainer: {
    background: 'white',
    padding: '40px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  },
  infoBox: {
    background: 'linear-gradient(135deg, #667eea15 0%, #764ba215 100%)',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '30px',
    border: '1px solid #667eea40',
  },
  instructions: {
    paddingLeft: '20px',
    lineHeight: '1.8',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  input: {
    padding: '12px 15px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '15px',
    transition: 'all 0.3s ease',
  },
  hint: {
    color: '#999',
    fontSize: '13px',
  },
  primaryButton: {
    padding: '14px 24px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  secondaryButton: {
    padding: '14px 24px',
    background: 'white',
    color: '#667eea',
    border: '2px solid #667eea',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  buttonGroup: {
    display: 'flex',
    gap: '15px',
    marginTop: '10px',
  },
  successBox: {
    padding: '20px',
  },
  errorBox: {
    background: '#fff3f3',
    padding: '30px',
    borderRadius: '8px',
    border: '2px solid #ff6b6b',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '20px',
    margin: '30px 0',
  },
  statCard: {
    background: 'linear-gradient(135deg, #667eea15 0%, #764ba215 100%)',
    padding: '20px',
    borderRadius: '12px',
    textAlign: 'center',
  },
  statNumber: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    color: '#667eea',
  },
  statLabel: {
    fontSize: '0.9rem',
    color: '#666',
    marginTop: '8px',
  },
  warningBox: {
    background: '#fff9e6',
    padding: '20px',
    borderRadius: '8px',
    border: '2px solid #ffd93d',
    marginTop: '20px',
  },
};

export default EmailIntegration;
