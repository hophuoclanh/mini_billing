import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";

import Home from "./component/home";
import Manager from "./pages/manager";
import Login from "./component/login";
import Product from "./component/product";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" exact element={<Login />} />
          <Route path="/manager" element={<Manager />} />
          <Route path="/product" element={<Product />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
