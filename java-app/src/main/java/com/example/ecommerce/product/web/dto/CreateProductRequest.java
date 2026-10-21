package com.example.ecommerce.product.web.dto;

import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import java.math.BigDecimal;

/**
 * Body of POST /api/v1/products: only what a client may set. Anything else in the JSON (id,
 * version, timestamps) is simply not a field here, so it can't reach the entity.
 *
 * @param description optional, defaults to ""
 * @param status optional, defaults to ACTIVE (DRAFT creates a product that isn't for sale yet)
 * @param categoryId optional
 */
public record CreateProductRequest(
    String sku,
    String name,
    String description,
    BigDecimal price,
    ProductStatus status,
    Long categoryId) {

  /** Builds a new, unsaved entity; the database assigns id, version and timestamps. */
  public Product toProduct() {
    return Product.builder()
        .sku(sku)
        .name(name)
        .description(description != null ? description : "")
        .price(price)
        .status(status != null ? status : ProductStatus.ACTIVE)
        .categoryId(categoryId)
        .build();
  }
}
