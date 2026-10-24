package com.example.ecommerce.product.exception;

import com.example.ecommerce.core.error.BusinessException;
import com.example.ecommerce.core.error.ErrorCode;

/** Another product already uses this SKU (409 DUPLICATE_SKU). */
public class DuplicateSkuException extends BusinessException {

  // Exceptions are Serializable (inherited from Throwable); a fixed version id avoids an -Xlint
  // warning
  private static final long serialVersionUID = 1L;

  private final String sku;

  public DuplicateSkuException(String sku) {
    super(ErrorCode.DUPLICATE_SKU, "A product with SKU " + sku + " already exists");
    this.sku = sku;
  }

  public String getSku() {
    return sku;
  }
}
