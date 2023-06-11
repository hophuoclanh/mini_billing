import React, { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {

    if (email === 'example@example.com' && password === 'password123') {

      console.log('Logged in successfully');
    } else {

      setError('Wrong password or email');
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
      }}
    >
      <Typography variant="h4" gutterBottom>
        Login
      </Typography>
      <TextField
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ marginBottom: '16px' }}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ marginBottom: '16px' }}
      />
      {error && (
        <Typography variant="body1" color="error" style={{ marginBottom: '16px' }}>
          {error}
        </Typography>
      )}
      <Button variant="contained" onClick={handleLogin}>
        Login
      </Button>
    </div>
  );
};

export default Login;
