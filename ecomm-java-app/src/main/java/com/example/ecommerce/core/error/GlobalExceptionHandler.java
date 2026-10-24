package com.example.ecommerce.core.error;

import jakarta.servlet.http.HttpServletRequest;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.HandlerMethodValidationException;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.resource.NoResourceFoundException;
import tools.jackson.core.JacksonException;
import tools.jackson.databind.exc.MismatchedInputException;

/**
 * Turns every exception into the one {@link ApiError} format (Steps 4.3 + 4.4). Controllers never
 * build error responses themselves; they just throw.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

  /** Expected business errors: the exception carries its own code and HTTP status. */
  @ExceptionHandler(BusinessException.class)
  ResponseEntity<ApiError> business(BusinessException e, HttpServletRequest request) {
    return respond(ApiError.of(e.getCode(), e.getMessage(), request.getRequestURI()));
  }

  /** Bean Validation failed on a @Valid request body: one entry per wrong field. */
  @ExceptionHandler(MethodArgumentNotValidException.class)
  ResponseEntity<ApiError> invalidBody(
      MethodArgumentNotValidException e, HttpServletRequest request) {
    List<ApiError.FieldError> fields =
        e.getBindingResult().getFieldErrors().stream()
            .map(f -> new ApiError.FieldError(f.getField(), f.getDefaultMessage()))
            .toList();
    return validationFailed(fields, request);
  }

  /**
   * Constraints on method parameters failed, e.g. ?size=500 (Spring's built-in method validation).
   */
  @ExceptionHandler(HandlerMethodValidationException.class)
  ResponseEntity<ApiError> invalidParameters(
      HandlerMethodValidationException e, HttpServletRequest request) {
    List<ApiError.FieldError> fields =
        e.getParameterValidationResults().stream()
            .flatMap(
                result ->
                    result.getResolvableErrors().stream()
                        .map(
                            error ->
                                new ApiError.FieldError(
                                    result.getMethodParameter().getParameterName(),
                                    error.getDefaultMessage())))
            .toList();
    return validationFailed(fields, request);
  }

  /**
   * The body couldn't be turned into the request object. A wrong type for a known field (e.g.
   * "price": "abc", or an unknown status) is a field error; anything else (broken JSON, no body) is
   * MALFORMED_REQUEST.
   */
  @ExceptionHandler(HttpMessageNotReadableException.class)
  ResponseEntity<ApiError> unreadableBody(
      HttpMessageNotReadableException e, HttpServletRequest request) {
    if (e.getCause() instanceof MismatchedInputException mismatch) {
      String field = fieldName(mismatch);
      if (field != null) {
        Class<?> target = mismatch.getTargetType();
        String message =
            target != null && target.isEnum()
                ? "must be one of "
                    + Arrays.stream(target.getEnumConstants())
                        .map(Object::toString)
                        .collect(Collectors.joining(", "))
                : ValidationMessages.INVALID_VALUE;
        return validationFailed(List.of(new ApiError.FieldError(field, message)), request);
      }
    }
    return respond(
        ApiError.of(
            ErrorCode.MALFORMED_REQUEST,
            "Request body is missing or is not valid JSON",
            request.getRequestURI()));
  }

  /** A path variable of the wrong type, e.g. /api/v1/products/abc. */
  @ExceptionHandler(MethodArgumentTypeMismatchException.class)
  ResponseEntity<ApiError> wrongPathType(
      MethodArgumentTypeMismatchException e, HttpServletRequest request) {
    return validationFailed(
        List.of(new ApiError.FieldError(e.getName(), ValidationMessages.INVALID_VALUE)), request);
  }

  /** No controller for this URL. */
  @ExceptionHandler(NoResourceFoundException.class)
  ResponseEntity<ApiError> noEndpoint(NoResourceFoundException e, HttpServletRequest request) {
    return respond(
        ApiError.of(
            ErrorCode.NOT_FOUND,
            "No endpoint " + request.getMethod() + " " + request.getRequestURI(),
            request.getRequestURI()));
  }

  @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
  ResponseEntity<ApiError> wrongMethod(
      HttpRequestMethodNotSupportedException e, HttpServletRequest request) {
    return respond(
        ApiError.of(
            ErrorCode.METHOD_NOT_ALLOWED,
            "Method " + request.getMethod() + " is not allowed for " + request.getRequestURI(),
            request.getRequestURI()));
  }

  /** Optimistic locking: someone else changed the row since it was read. */
  @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
  ResponseEntity<ApiError> concurrentUpdate(
      ObjectOptimisticLockingFailureException e, HttpServletRequest request) {
    return respond(
        ApiError.of(
            ErrorCode.CONCURRENT_UPDATE,
            "The data was changed by another request; reload it and try again",
            request.getRequestURI()));
  }

  /** A database constraint stopped the write (e.g. a duplicate SKU created at the same moment). */
  @ExceptionHandler(DataIntegrityViolationException.class)
  ResponseEntity<ApiError> constraintViolated(
      DataIntegrityViolationException e, HttpServletRequest request) {
    log.warn("Constraint violation on {}: {}", request.getRequestURI(), e.getMostSpecificCause());
    return respond(
        ApiError.of(
            ErrorCode.CONFLICT,
            "The request conflicts with existing data",
            request.getRequestURI()));
  }

  /** Anything unexpected: full details go to the log only, never to the client. */
  @ExceptionHandler(Exception.class)
  ResponseEntity<ApiError> unexpected(Exception e, HttpServletRequest request) {
    log.error("Unexpected error on {} {}", request.getMethod(), request.getRequestURI(), e);
    return respond(
        ApiError.of(
            ErrorCode.INTERNAL_ERROR, "An unexpected error occurred", request.getRequestURI()));
  }

  private static ResponseEntity<ApiError> validationFailed(
      List<ApiError.FieldError> fields, HttpServletRequest request) {
    return respond(
        ApiError.of(
            ErrorCode.VALIDATION_FAILED,
            "Request validation failed",
            request.getRequestURI(),
            fields));
  }

  private static ResponseEntity<ApiError> respond(ApiError body) {
    return ResponseEntity.status(body.status()).body(body);
  }

  /** The JSON property the error happened on, or null when it isn't about a property. */
  private static String fieldName(JacksonException e) {
    return e.getPath().stream()
        .map(JacksonException.Reference::getPropertyName)
        .filter(name -> name != null)
        .reduce((first, second) -> first + "." + second)
        .orElse(null);
  }
}
