import React, { useEffect, useState } from "react";
import axios from "axios";

function Cart() {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/cart")
      .then(res => setCart(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Carrinho</h2>
      <ul>
        {cart.map(item => (
          <li key={item.product_id}>
            {item.name} - {item.quantity}x - R${item.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Cart;