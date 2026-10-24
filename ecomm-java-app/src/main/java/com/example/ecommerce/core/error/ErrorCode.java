package com.example.ecommerce.core.error;

import org.springframework.http.HttpStatus;

/**
 * Stable, machine-readable error codes. Clients and tests check the code, not the message text. The
 * same codes exist in the Python app (ecommerce/core/errors.py).
 */
public enum ErrorCode {
  VALIDATION_FAILED(HttpStatus.BAD_REQUEST),
  MALFORMED_REQUEST(HttpStatus.BAD_REQUEST),
  NOT_FOUND(HttpStatus.NOT_FOUND),
  METHOD_NOT_ALLOWED(HttpStatus.METHOD_NOT_ALLOWED),
  PRODUCT_NOT_FOUND(HttpStatus.NOT_FOUND),
  DUPLICATE_SKU(HttpStatus.CONFLICT),
  CONCURRENT_UPDATE(HttpStatus.CONFLICT),
  CONFLICT(HttpStatus.CONFLICT),
  INTERNAL_ERROR(HttpStatus.INTERNAL_SERVER_ERROR);

  private final HttpStatus status;

  ErrorCode(HttpStatus status) {
    this.status = status;
  }

  public HttpStatus status() {
    return status;
  }
}
