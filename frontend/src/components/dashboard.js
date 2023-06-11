import React from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const Dashboard = ({ userRole }) => {
  const data = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'manager' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'staff' },
  ];

  const handleEdit = (id) => {
    // Xử lý logic khi nhấn nút Edit
  };

  const handleDelete = (id) => {
    // Xử lý logic khi nhấn nút Delete
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Email</TableCell>
            <TableCell>Role</TableCell>
            {userRole === 'admin' || userRole === 'manager' ? <TableCell>Actions</TableCell> : null}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.email}</TableCell>
              <TableCell>{row.role}</TableCell>
              {userRole === 'admin' || userRole === 'manager' ? (
                <TableCell>
                  <Button variant="contained" size="small" onClick={() => handleEdit(row.id)}>
                    Edit
                  </Button>
                  <Button variant="contained" color="error" size="small" onClick={() => handleDelete(row.id)}>
                    Delete
                  </Button>
                </TableCell>
              ) : null}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Dashboard;
