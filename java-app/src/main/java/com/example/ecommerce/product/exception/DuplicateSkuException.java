package com.example.ecommerce.product.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * Another product already uses this SKU. Mapped to 409 for now via @ResponseStatus; Stage 4
 * replaces this with central handling.
 */
@ResponseStatus(HttpStatus.CONFLICT)
public class DuplicateSkuException extends RuntimeException {

  // Exceptions are Serializable (inherited from Throwable); a fixed version id avoids an -Xlint
  // warning
  private static final long serialVersionUID = 1L;

  private final String sku;

  public DuplicateSkuException(String sku) {
    super("A product with SKU " + sku + " already exists");
    this.sku = sku;
  }

  public String getSku() {
    return sku;
  }
}
