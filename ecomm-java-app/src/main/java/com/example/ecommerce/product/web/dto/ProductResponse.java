package com.example.ecommerce.product.web.dto;

import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import com.fasterxml.jackson.annotation.JsonFormat;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;

/**
 * What the API returns for a product: the public contract, independent of the JPA entity. Internal
 * fields such as the optimistic-locking version are deliberately left out.
 */
public record ProductResponse(
    Long id,
    String sku,
    String name,
    String description,
    @JsonFormat(shape = JsonFormat.Shape.STRING) BigDecimal price,
    ProductStatus status,
    Long categoryId,
    Instant createdAt,
    Instant updatedAt) {

  public static ProductResponse from(Product product) {
    return new ProductResponse(
        product.getId(),
        product.getSku(),
        product.getName(),
        product.getDescription(),
        // Always 2 decimals ("14.50"), also when a client sent "14.5"; the column is numeric(12,2)
        product.getPrice().setScale(2, RoundingMode.HALF_UP),
        product.getStatus(),
        product.getCategoryId(),
        product.getCreatedAt(),
        product.getUpdatedAt());
  }
}
