import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";
import config from "./config.js";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify(
        `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
      ),
    };

    const response = await fetch(
      config.API_URL_ROOT + "/authentication/login",
      requestOptions
    );

    const data = await response.json();

    if (!response.ok) {
      setError(data.detail);
    } else {
      console.log("Login sucessfully");
      console.log(data);
      // save access token into local storage
      localStorage.setItem("access_token", data.access_token);
      // const navigate = useNavigate();
      // navigate(config.API_URL_ROOT + "/authenticate/me");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
      }}
    >
      <Typography variant="h4" gutterBottom>
        Login
      </Typography>
      <TextField
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ marginBottom: "16px" }}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ marginBottom: "16px" }}
      />
      {error && (
        <Typography
          variant="body1"
          color="error"
          style={{ marginBottom: "16px" }}
        >
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
