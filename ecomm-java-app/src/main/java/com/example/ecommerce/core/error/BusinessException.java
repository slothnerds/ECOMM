package com.example.ecommerce.core.error;

/**
 * Parent of every expected business error. Carries its {@link ErrorCode}, so the central handler
 * turns any subclass into the right HTTP status and body without knowing the subclass.
 */
public abstract class BusinessException extends RuntimeException {

  // Exceptions are Serializable (inherited from Throwable); a fixed version id avoids an -Xlint
  // warning
  private static final long serialVersionUID = 1L;

  private final ErrorCode code;

  protected BusinessException(ErrorCode code, String message) {
    super(message);
    this.code = code;
  }

  public ErrorCode getCode() {
    return code;
  }
}
