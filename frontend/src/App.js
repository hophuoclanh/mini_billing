import React, { useState } from 'react';
import Login from './component/login';
import Dashboard from './component/dashboard';

const App = () => {
  const [userRole, setUserRole] = useState('');

  const handleLogin = (role) => {
    setUserRole(role);
  };

  return (
    <div>
      {userRole ? (
        <Dashboard userRole={userRole} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
