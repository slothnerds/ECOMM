package com.example.ecommerce.core.config;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

/**
 * Typed application settings, bound from the {@code app.*} keys in application.yml.
 *
 * <p>{@code @Validated} makes startup fail fast when a value is missing or invalid.
 */
@Validated
@ConfigurationProperties(prefix = "app")
public record AppProperties(
    @NotBlank @Pattern(regexp = "dev|test|prod") String environment,
    @NotBlank @Size(min = 32, message = "must be at least 32 characters") String jwtSecret,
    @NotNull Duration holdDuration) {

  /** Never print the secret: records include every field in toString() by default. */
  @Override
  public String toString() {
    return "AppProperties[environment=%s, jwtSecret=**********, holdDuration=%s]"
        .formatted(environment, holdDuration);
  }
}
