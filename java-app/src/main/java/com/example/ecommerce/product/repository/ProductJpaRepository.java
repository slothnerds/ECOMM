package com.example.ecommerce.product.repository;

import com.example.ecommerce.product.model.Product;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Spring Data generates the implementation at startup: save, findById, findAll(Sort), ... come from
 * JpaRepository, and findBySku is derived from the method name (WHERE sku = ?).
 */
interface ProductJpaRepository extends JpaRepository<Product, Long> {

  Optional<Product> findBySku(String sku);
}
