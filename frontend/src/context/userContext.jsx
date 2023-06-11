import React, { createContext, useEffect, useState } from "react";

import config from "./config.js"

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("accessToken"));

  useEffect(() => {
    const fetchUser = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };

      const response = await fetch(config.API_URL_ROOT + "/me", requestOptions);

      if (!response.ok) {
        setToken(null);
      }
      localStorage.setItem("accessToken", token);
    };
    fetchUser();
  }, [token]);

  return (
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
  );
};
