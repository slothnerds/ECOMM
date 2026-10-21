package com.example.ecommerce.product.repository;

import com.example.ecommerce.product.model.Product;
import java.util.List;
import java.util.Optional;

/**
 * Storage contract for products. Stage 2 had an in-memory implementation; since Stage 3 it is
 * {@link JpaProductRepository} (PostgreSQL). Products are never deleted, only discontinued.
 */
public interface ProductRepository {

  /** Inserts when the id is null (the database assigns it), otherwise updates. */
  Product save(Product product);

  Optional<Product> findById(long id);

  Optional<Product> findBySku(String sku);

  /** All products, ordered by id. */
  List<Product> findAll();
}
