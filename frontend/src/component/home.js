import React, { useEffect, useState } from "react";

// import { config } from "dotenv";
// config();
// console.log(process.env.API_URL);

const Home = () => {
  console.log("Hello World");
  const [message, setMessage] = useState("");

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("http://localhost:9000/", requestOptions);
    // const response = await fetch("/", requestOptions);
    console.log(response);
    const data = await response.json();

    console.log(data);

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
      <h2> Successfully connected to backend api </h2>
      <h2> {message} </h2>
    </div>
  );
};
export default Home;
