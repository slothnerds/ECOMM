package com.example.ecommerce.product.exception;

import com.example.ecommerce.core.error.BusinessException;
import com.example.ecommerce.core.error.ErrorCode;

/** No product exists with the requested id (404 PRODUCT_NOT_FOUND). */
public class ProductNotFoundException extends BusinessException {

  // Exceptions are Serializable (inherited from Throwable); a fixed version id avoids an -Xlint
  // warning
  private static final long serialVersionUID = 1L;

  private final long productId;

  public ProductNotFoundException(long productId) {
    super(ErrorCode.PRODUCT_NOT_FOUND, "Product " + productId + " not found");
    this.productId = productId;
  }

  public long getProductId() {
    return productId;
  }
}
