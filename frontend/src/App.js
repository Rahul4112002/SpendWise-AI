import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import ExpenseTracker from './components/Dashboard/ExpenseTracker';
import UploadStatement from './components/BankStatement/UploadStatement';
import Reports from './components/Dashboard/Reports';
import AIChat from './components/AI/AIChat';
import Header from './components/Common/Header';
import Footer from './components/Common/Footer';
import PrivateRoute from './components/Common/PrivateRoute';
import './styles.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route 
                path="/dashboard" 
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/transactions" 
                element={
                  <PrivateRoute>
                    <ExpenseTracker />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/upload" 
                element={
                  <PrivateRoute>
                    <UploadStatement />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/reports" 
                element={
                  <PrivateRoute>
                    <Reports />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/ai-chat" 
                element={
                  <PrivateRoute>
                    <AIChat />
                  </PrivateRoute>
                } 
              />
              <Route path="/" element={<Navigate to="/login" />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
