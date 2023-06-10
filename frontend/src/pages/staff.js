import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

const Staff = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/users')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);

  const handleDelete = (id) => {
    axios.delete(`http://localhost:5000/users/${id}`)
      .then(response => {
        setUsers(users.filter(user => user.IDuser !== id));
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Email</TableCell>
            <TableCell>Password</TableCell>
            <TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map(user => (
            <TableRow key={user.IDuser}>
              <TableCell>{user.IDuser}</TableCell>
              <TableCell>{user.name}</TableCell>
              <TableCell>{user.gmail}</TableCell>
              <TableCell>{user.password}</TableCell>
              <TableCell>
                <Button onClick={() => handleDelete(user.IDuser)}>Delete</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Staff;
