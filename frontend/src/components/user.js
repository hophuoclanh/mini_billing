import React, { useState, useEffect } from "react";

import config from "./config.js";

const User = () => {
  const [user_id, setUserId] = useState("");
  const [user_name, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");

  const token = `Bearer ${localStorage.getItem("access_token")}`;
  console.log("This is token: " + token);
  const getUserInfo = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    };

    const response = await fetch(
      config.API_URL_ROOT + "/authentication/me",
      requestOptions
    );

    const data = await response.json();

    if (!response.ok) {
      console.log("something messed up");
      console.log(response);
      console.log("***");
    } else {
      setUserId(data.user_id);
      setUserName(data.user_name);
      setEmail(data.email);
      setPhone(data.phone);
      setAddress(data.address);
    }
  };

  useEffect(() => {
    getUserInfo();
  }, []);

  return (
    <div>
      <h2>User personal information</h2>
      <h4>{user_id}</h4>
      <h4>{user_name}</h4>
      <h4>{email}</h4>
      <h4>{phone}</h4>
      <h4>{address}</h4>
    </div>
  );
};

export default User;
