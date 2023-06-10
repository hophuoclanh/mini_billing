import React from 'react';
import { makeStyles } from '@mui/styles';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

const useStyles = makeStyles({
  verticalNavbar: {
    height: '100%',
    width: '80px',
    position: 'fixed',
    zIndex: 1,
    top: 0,
    left: 0,
    backgroundColor: '#cf8be0',
    overflowX: 'hidden',
    paddingTop: '100px',
  },
});

const buttonStyle = {
    color: 'white', 
    backgroundColor: '#ccc0cf',
  };

function Manager() {
  const classes = useStyles();

  const handleButtonClick = (link) => {
    window.location.href = link;
  };

  return (
    <div className={classes.verticalNavbar}>
      <Box gap={1} display="flex" flexDirection="column">
        <Button style={buttonStyle} onClick={() => handleButtonClick('users')}>
          Users
        </Button>
        <Button style={buttonStyle} onClick={() => handleButtonClick('product')}>
          Product
        </Button>
        <Button style={buttonStyle} onClick={() => handleButtonClick('order')}>
          Orders
        </Button>
        <Button style={buttonStyle} onClick={() => handleButtonClick('Login')}>
          Logout
        </Button>
      </Box>
    </div>
  );
}

export default Manager;
