import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button } from '@mui/material';

const Create_user = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newUser, setNewUser] = useState({
    user_id: '',
    user_name: '',
    email: '',
    phone: '',
    address: '',
    password: '',
  });

  useEffect(() => {
    axios.get('http://localhost:3000/users')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handleAddUser = () => {
    axios.post('http://localhost:3000/users', newUser)
      .then(response => {
        setUsers([...users, response.data]);
        setNewUser({
          user_id: '',
          user_name: '',
          email: '',
          phone: '',
          address: '',
          password: '',
        });
      })
      .catch(error => {
        console.error(error);
      });
  };

  const handleUpdateUser = () => {
    axios.put(`http://localhost:3000/users/${selectedUser.user_id}`, selectedUser)
      .then(response => {
        const updatedUsers = users.map(user => {
          if (user.user_id === response.data.user_id) {
            return response.data;
          }
          return user;
        });
        setUsers(updatedUsers);
        setSelectedUser(null);
      })
      .catch(error => {
        console.error(error);
      });
  };

  const handleDeleteUser = () => {
    axios.delete(`http://localhost:3000/users/${selectedUser.user_id}`)
      .then(() => {
        const updatedUsers = users.filter(user => user.user_id !== selectedUser.user_id);
        setUsers(updatedUsers);
        setSelectedUser(null);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
      <h2>Dữ liệu Users</h2>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>user_id</TableCell>
              <TableCell>user_name</TableCell>
              <TableCell>email</TableCell>
              <TableCell>phone</TableCell>
              <TableCell>address</TableCell>
              <TableCell>password</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map(user => (
              <TableRow key={user.user_id} onClick={() => setSelectedUser(user)}>
                <TableCell>{user.user_id}</TableCell>
                <TableCell>{user.user_name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.phone}</TableCell>
                <TableCell>{user.address}</TableCell>
                <TableCell>{user.password}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <div>
        <h3>Thông tin người dùng</h3>
        {selectedUser ? (
          <div>
            <p>user_id: {selectedUser.user_id}</p>
            <p>user_name: {selectedUser.user_name}</p>
            <p>email: {selectedUser.email}</p>
            <p>phone: {selectedUser.phone}</p>
            <p>address: {selectedUser.address}</p>
            <p>password: {selectedUser.password}</p>

            <Button variant="contained" onClick={handleUpdateUser}>Change</Button>
            <Button variant="contained" onClick={handleDeleteUser}>Delete</Button>
          </div>
        ) : (
          <div>
            <TextField
              type="text"
              placeholder="user_id"
              value={newUser.user_id}
              onChange={event => setNewUser({ ...newUser, user_id: event.target.value })}
            />
            <TextField
              type="text"
              placeholder="user_name"
              value={newUser.user_name}
              onChange={event => setNewUser({ ...newUser, user_name: event.target.value })}
            />
            <TextField
              type="text"
              placeholder="email"
              value={newUser.email}
              onChange={event => setNewUser({ ...newUser, email: event.target.value })}
            />
            <TextField
              type="text"
              placeholder="phone"
              value={newUser.phone}
              onChange={event => setNewUser({ ...newUser, phone: event.target.value })}
            />
            <TextField
              type="text"
              placeholder="address"
              value={newUser.address}
              onChange={event => setNewUser({ ...newUser, address: event.target.value })}
            />
            <TextField
              type="text"
              placeholder="password"
              value={newUser.password}
              onChange={event => setNewUser({ ...newUser, password: event.target.value })}
            />

            <Button variant="contained" onClick={handleAddUser}>Add</Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Create_user;
