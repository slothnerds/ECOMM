package com.example.ecommerce.core.error;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Comparator;
import java.util.List;

/**
 * The one error body of the API, identical in the Python app.
 *
 * @param code stable machine-readable code
 * @param message human-readable summary
 * @param status HTTP status, repeated for clients that only see the body
 * @param path the request path
 * @param timestamp when it happened (UTC, milliseconds)
 * @param fieldErrors which input fields were wrong; empty unless code is VALIDATION_FAILED
 */
public record ApiError(
    String code,
    String message,
    int status,
    String path,
    Instant timestamp,
    List<FieldError> fieldErrors) {

  public record FieldError(String field, String message) {}

  public static ApiError of(ErrorCode code, String message, String path) {
    return of(code, message, path, List.of());
  }

  public static ApiError of(
      ErrorCode code, String message, String path, List<FieldError> fieldErrors) {
    return new ApiError(
        code.name(),
        message,
        code.status().value(),
        path,
        Instant.now().truncatedTo(ChronoUnit.MILLIS),
        // Stable order, so responses (and tests) don't depend on validation order
        fieldErrors.stream()
            .sorted(Comparator.comparing(FieldError::field).thenComparing(FieldError::message))
            .toList());
  }
}
