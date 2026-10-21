package com.example.ecommerce.product.repository;

import com.example.ecommerce.product.model.Product;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Repository;

/**
 * Our ProductRepository contract, backed by PostgreSQL through Spring Data JPA. An adapter keeps
 * the service independent of Spring Data's much larger interface.
 */
@Repository
@RequiredArgsConstructor
public class JpaProductRepository implements ProductRepository {

  private final ProductJpaRepository jpa;

  @Override
  public Product save(Product product) {
    return jpa.save(product);
  }

  @Override
  public Optional<Product> findById(long id) {
    return jpa.findById(id);
  }

  @Override
  public Optional<Product> findBySku(String sku) {
    return jpa.findBySku(sku);
  }

  @Override
  public List<Product> findAll() {
    return jpa.findAll(Sort.by("id"));
  }
}
