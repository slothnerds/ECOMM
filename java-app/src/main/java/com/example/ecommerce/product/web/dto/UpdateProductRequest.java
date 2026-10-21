package com.example.ecommerce.product.web.dto;

import com.example.ecommerce.product.model.ProductStatus;
import com.example.ecommerce.product.model.ProductUpdate;
import java.math.BigDecimal;

/** Body of PUT /api/v1/products/{id}. The SKU is not here: it can't change after creation. */
public record UpdateProductRequest(
    String name, String description, BigDecimal price, ProductStatus status) {

  /** The service's input; keeps HTTP types out of the service layer. */
  public ProductUpdate toUpdate() {
    return new ProductUpdate(name, description != null ? description : "", price, status);
  }
}
