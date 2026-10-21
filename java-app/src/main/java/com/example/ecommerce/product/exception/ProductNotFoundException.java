package com.example.ecommerce.product.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * No product exists with the requested id. Mapped to 404 for now via @ResponseStatus; Stage 4
 * replaces this with central handling.
 */
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ProductNotFoundException extends RuntimeException {

  // Exceptions are Serializable (inherited from Throwable); a fixed version id avoids an -Xlint
  // warning
  private static final long serialVersionUID = 1L;

  private final long productId;

  public ProductNotFoundException(long productId) {
    super("Product " + productId + " not found");
    this.productId = productId;
  }

  public long getProductId() {
    return productId;
  }
}
