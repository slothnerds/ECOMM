package com.example.ecommerce.core.error;

/**
 * Field error texts, identical to the Python app's, so both return the same message for the same
 * mistake. Constants, because annotation attributes must be compile-time constants.
 */
public final class ValidationMessages {

  public static final String REQUIRED = "is required";
  public static final String NOT_BLANK = "must not be blank";
  public static final String MAX_200 = "must be at most 200 characters";
  public static final String MAX_2000 = "must be at most 2000 characters";
  public static final String GREATER_THAN_0 = "must be greater than 0";
  public static final String MONEY_DIGITS =
      "must have at most 10 digits before and 2 after the decimal point";
  public static final String SKU_FORMAT =
      "must look like ABC-123 (3 capital letters, a dash, digits)";
  public static final String INVALID_VALUE = "has an invalid value";
  public static final String AT_LEAST_0 = "must be greater than or equal to 0";
  public static final String AT_LEAST_1 = "must be greater than or equal to 1";
  public static final String AT_MOST_100 = "must be less than or equal to 100";

  /** Regex: at least one non-whitespace character. */
  public static final String NOT_BLANK_PATTERN = "(?s).*\\S.*";

  /** Regex for a SKU: 3 capital letters, a dash, 1 to 28 digits (32 characters at most). */
  public static final String SKU_PATTERN = "[A-Z]{3}-\\d{1,28}";

  private ValidationMessages() {}
}
