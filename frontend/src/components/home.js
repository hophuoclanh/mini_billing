import React, { useEffect, useState } from "react";

import config from "./config.js";

const Home = () => {
  const [message, setMessage] = useState("");

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(config.API_URL_ROOT + "/", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("something messed up");
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  return (
    <div>
      <h1> Hello World </h1>
      <h2>{message ? message : "Fail to connect to backend"}</h2>
    </div>
  );
};
export default Home;
