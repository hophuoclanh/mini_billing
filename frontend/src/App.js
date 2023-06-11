import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";

import Home from "./components/home";
import Manager from "./pages/manager";
import Login from "./components/login";
import Product from "./components/product";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/manager" element={<Manager />} />
          <Route path="/product" element={<Product />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
