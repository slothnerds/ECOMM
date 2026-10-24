package com.example.ecommerce.product.web.dto;

import static com.example.ecommerce.core.error.ValidationMessages.GREATER_THAN_0;
import static com.example.ecommerce.core.error.ValidationMessages.MAX_200;
import static com.example.ecommerce.core.error.ValidationMessages.MAX_2000;
import static com.example.ecommerce.core.error.ValidationMessages.MONEY_DIGITS;
import static com.example.ecommerce.core.error.ValidationMessages.NOT_BLANK;
import static com.example.ecommerce.core.error.ValidationMessages.NOT_BLANK_PATTERN;
import static com.example.ecommerce.core.error.ValidationMessages.REQUIRED;
import static com.example.ecommerce.core.error.ValidationMessages.SKU_FORMAT;
import static com.example.ecommerce.core.error.ValidationMessages.SKU_PATTERN;

import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;

/**
 * Body of POST /api/v1/products: only what a client may set. Anything else in the JSON (id,
 * version, timestamps) is simply not a field here, so it can't reach the entity.
 *
 * <p>Validated with Bean Validation when the controller marks it {@code @Valid}; the messages are
 * shared with the Python app (see {@code ValidationMessages}).
 *
 * @param description optional, defaults to ""
 * @param status optional, defaults to ACTIVE (DRAFT creates a product that isn't for sale yet)
 * @param categoryId optional
 */
public record CreateProductRequest(
    @NotNull(message = REQUIRED) @Pattern(regexp = SKU_PATTERN, message = SKU_FORMAT) String sku,
    @NotNull(message = REQUIRED)
        @Pattern(regexp = NOT_BLANK_PATTERN, message = NOT_BLANK)
        @Size(max = 200, message = MAX_200)
        String name,
    @Size(max = 2000, message = MAX_2000) String description,
    @NotNull(message = REQUIRED)
        @DecimalMin(value = "0", inclusive = false, message = GREATER_THAN_0)
        @Digits(integer = 10, fraction = 2, message = MONEY_DIGITS)
        BigDecimal price,
    ProductStatus status,
    @Positive(message = GREATER_THAN_0) Long categoryId) {

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
