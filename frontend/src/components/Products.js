import React, { useEffect, useState } from "react";
import axios from "axios";

function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/products")
      .then(res => setProducts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Produtos</h2>
      <ul>
        {products.map(p => (
          <li key={p.id}>{p.name} - R${p.price}</li>
        ))}
      </ul>
    </div>
  );
}

export default Products;