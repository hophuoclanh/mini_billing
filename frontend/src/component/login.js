import React, { useState } from 'react';
import { Button, TextField, Typography } from '@mui/material';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (email === 'example@gmail.com' && password === 'password') {
      setError('');
      console.log('Logged in successfully');
    } else {
      setError('Wrong password or email');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={handleEmailChange}
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={handlePasswordChange}
        required
      />
      {error && <Typography color="error">{error}</Typography>}
      <Button variant="contained" type="submit">
        Login
      </Button>
    </form>
  );
};

export default Login;
