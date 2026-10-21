package com.example.ecommerce.product.model;

/** Lifecycle of a catalog product; stored as text, matching the products_status_chk constraint. */
public enum ProductStatus {
  /** Being prepared; not visible to customers yet. */
  DRAFT,
  /** For sale. */
  ACTIVE,
  /** No longer sold, but kept because carts and orders reference it (soft delete, SN-4). */
  DISCONTINUED
}
