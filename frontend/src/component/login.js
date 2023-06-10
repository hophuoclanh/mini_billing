import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleLogin = () => {
    // Xử lý logic đăng nhập và gọi hàm onLogin khi đăng nhập thành công
    if (username === 'admin' && password === 'password') {
      onLogin('admin');
    } else if (username === 'manager' && password === 'password') {
      onLogin('manager');
    } else if (username === 'staff' && password === 'password') {
      onLogin('staff');
    }
  };

  return (
    <div>
      <TextField label="Username" value={username} onChange={handleUsernameChange} />
      <TextField type="password" label="Password" value={password} onChange={handlePasswordChange} />
      <Button variant="contained" onClick={handleLogin}>Login</Button>
    </div>
  );
};

export default Login;
