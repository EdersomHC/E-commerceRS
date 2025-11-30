import React from "react";
import Login from "./components/Login";
import Products from "./components/Products";
import Cart from "./components/Cart";

function App() {
  return (
    <div>
      <h1>E-commerce Frontend</h1>
      <Login />
      <Products />
      <Cart />
    </div>
  );
}

export default App;
