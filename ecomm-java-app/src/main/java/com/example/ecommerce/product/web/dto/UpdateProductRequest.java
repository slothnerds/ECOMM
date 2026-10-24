package com.example.ecommerce.product.web.dto;

import static com.example.ecommerce.core.error.ValidationMessages.GREATER_THAN_0;
import static com.example.ecommerce.core.error.ValidationMessages.MAX_200;
import static com.example.ecommerce.core.error.ValidationMessages.MAX_2000;
import static com.example.ecommerce.core.error.ValidationMessages.MONEY_DIGITS;
import static com.example.ecommerce.core.error.ValidationMessages.NOT_BLANK;
import static com.example.ecommerce.core.error.ValidationMessages.NOT_BLANK_PATTERN;
import static com.example.ecommerce.core.error.ValidationMessages.REQUIRED;

import com.example.ecommerce.product.model.ProductStatus;
import com.example.ecommerce.product.model.ProductUpdate;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;

/** Body of PUT /api/v1/products/{id}. The SKU is not here: it can't change after creation. */
public record UpdateProductRequest(
    @NotNull(message = REQUIRED)
        @Pattern(regexp = NOT_BLANK_PATTERN, message = NOT_BLANK)
        @Size(max = 200, message = MAX_200)
        String name,
    @Size(max = 2000, message = MAX_2000) String description,
    @NotNull(message = REQUIRED)
        @DecimalMin(value = "0", inclusive = false, message = GREATER_THAN_0)
        @Digits(integer = 10, fraction = 2, message = MONEY_DIGITS)
        BigDecimal price,
    @NotNull(message = REQUIRED) ProductStatus status) {

  /** The service's input; keeps HTTP types out of the service layer. */
  public ProductUpdate toUpdate() {
    return new ProductUpdate(name, description != null ? description : "", price, status);
  }
}
