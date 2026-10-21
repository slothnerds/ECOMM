package com.example.ecommerce.product.model;

import java.math.BigDecimal;

/**
 * The fields an update may change. Id and SKU are deliberately absent: the SKU is fixed after
 * creation because orders reference it.
 */
public record ProductUpdate(
    String name, String description, BigDecimal price, ProductStatus status) {}
