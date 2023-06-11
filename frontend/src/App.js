import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";

import Home from "./components/home";
import Manager from "./pages/manager";
import Login from "./components/login";
import User from "./components/user";
import Product from "./components/product";

import Dashboard from "./components/dashboard";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/user" element={<User />} />
          <Route path="/manager" element={<Manager />} />
          <Route path="/product" element={<Product />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
