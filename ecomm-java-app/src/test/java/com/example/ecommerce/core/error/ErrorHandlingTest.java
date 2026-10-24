package com.example.ecommerce.core.error;

import static org.hamcrest.Matchers.endsWith;
import static org.hamcrest.Matchers.hasSize;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.ecommerce.product.exception.DuplicateSkuException;
import com.example.ecommerce.product.exception.ProductNotFoundException;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.service.ProductService;
import com.example.ecommerce.product.web.ProductController;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.MediaType;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

/**
 * Validation (4.2) and the one error format (4.3) produced centrally (4.4). The Python app has the
 * same cases in tests/test_errors.py and must return the same bodies.
 */
@WebMvcTest(ProductController.class)
@ActiveProfiles("test")
class ErrorHandlingTest {

  @Autowired private MockMvc mockMvc;

  @MockitoBean private ProductService service;

  private ResultActions postJson(String json) throws Exception {
    return mockMvc.perform(
        post("/api/v1/products").contentType(MediaType.APPLICATION_JSON).content(json));
  }

  private ResultActions putJson(String json) throws Exception {
    return mockMvc.perform(
        put("/api/v1/products/1").contentType(MediaType.APPLICATION_JSON).content(json));
  }

  // ---------------------------------------------------------------- validation (400)

  @Test
  void missingRequiredFieldsAreListedInFieldOrder() throws Exception {
    postJson("{}")
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"))
        .andExpect(jsonPath("$.message").value("Request validation failed"))
        .andExpect(jsonPath("$.status").value(400))
        .andExpect(jsonPath("$.path").value("/api/v1/products"))
        .andExpect(jsonPath("$.timestamp").value(endsWith("Z")))
        .andExpect(jsonPath("$.fieldErrors", hasSize(3)))
        .andExpect(jsonPath("$.fieldErrors[0].field").value("name"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("is required"))
        .andExpect(jsonPath("$.fieldErrors[1].field").value("price"))
        .andExpect(jsonPath("$.fieldErrors[2].field").value("sku"));
    verifyNoInteractions(service); // invalid input never reaches the service
  }

  @Test
  void eachRuleHasItsOwnMessage() throws Exception {
    postJson(
            """
            {"sku": "bad", "name": "   ", "price": "-1", "categoryId": 0}
            """)
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.fieldErrors", hasSize(4)))
        .andExpect(jsonPath("$.fieldErrors[0].field").value("categoryId"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("must be greater than 0"))
        .andExpect(jsonPath("$.fieldErrors[1].field").value("name"))
        .andExpect(jsonPath("$.fieldErrors[1].message").value("must not be blank"))
        .andExpect(jsonPath("$.fieldErrors[2].field").value("price"))
        .andExpect(jsonPath("$.fieldErrors[2].message").value("must be greater than 0"))
        .andExpect(jsonPath("$.fieldErrors[3].field").value("sku"))
        .andExpect(
            jsonPath("$.fieldErrors[3].message")
                .value("must look like ABC-123 (3 capital letters, a dash, digits)"));
  }

  @Test
  void lengthAndMoneyPrecisionAreChecked() throws Exception {
    postJson(
            """
            {"sku": "ABC-1", "name": "%s", "price": "12.345"}
            """
                .formatted("x".repeat(201)))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.fieldErrors[0].message").value("must be at most 200 characters"))
        .andExpect(
            jsonPath("$.fieldErrors[1].message")
                .value("must have at most 10 digits before and 2 after the decimal point"));
  }

  @Test
  void wrongTypeIsAFieldError() throws Exception {
    postJson(
            """
            {"sku": "ABC-1", "name": "Mug", "price": "abc"}
            """)
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"))
        .andExpect(jsonPath("$.fieldErrors[0].field").value("price"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("has an invalid value"));
  }

  @Test
  void unknownEnumValueListsTheAllowedValues() throws Exception {
    putJson(
            """
            {"name": "Mug", "price": "9.99", "status": "SOLD_OUT"}
            """)
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.fieldErrors[0].field").value("status"))
        .andExpect(
            jsonPath("$.fieldErrors[0].message")
                .value("must be one of DRAFT, ACTIVE, DISCONTINUED"));
  }

  @Test
  void updateRequiresStatus() throws Exception {
    putJson(
            """
            {"name": "Mug", "price": "9.99"}
            """)
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.fieldErrors[0].field").value("status"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("is required"));
  }

  @Test
  void pathVariableOfWrongType() throws Exception {
    mockMvc
        .perform(get("/api/v1/products/abc"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.fieldErrors[0].field").value("id"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("has an invalid value"));
  }

  @Test
  void pageAndSizeAreValidated() throws Exception {
    mockMvc
        .perform(get("/api/v1/products").param("page", "-1").param("size", "101"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"))
        .andExpect(jsonPath("$.fieldErrors[0].field").value("page"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("must be greater than or equal to 0"))
        .andExpect(jsonPath("$.fieldErrors[1].field").value("size"))
        .andExpect(jsonPath("$.fieldErrors[1].message").value("must be less than or equal to 100"));
    mockMvc
        .perform(get("/api/v1/products").param("size", "0"))
        .andExpect(
            jsonPath("$.fieldErrors[0].message").value("must be greater than or equal to 1"));
    mockMvc
        .perform(get("/api/v1/products").param("page", "abc"))
        .andExpect(jsonPath("$.fieldErrors[0].field").value("page"))
        .andExpect(jsonPath("$.fieldErrors[0].message").value("has an invalid value"));
    verifyNoInteractions(service);
  }

  @Test
  void brokenJsonIsMalformed() throws Exception {
    postJson("{\"sku\": ")
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("MALFORMED_REQUEST"))
        .andExpect(jsonPath("$.message").value("Request body is missing or is not valid JSON"))
        .andExpect(jsonPath("$.fieldErrors", hasSize(0)));
  }

  @Test
  void missingBodyIsMalformed() throws Exception {
    mockMvc
        .perform(post("/api/v1/products").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.code").value("MALFORMED_REQUEST"));
  }

  // ---------------------------------------------------------------- routing (404 / 405)

  @Test
  void unknownUrlIsNotFound() throws Exception {
    mockMvc
        .perform(get("/api/v1/nope"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.code").value("NOT_FOUND"))
        .andExpect(jsonPath("$.message").value("No endpoint GET /api/v1/nope"));
  }

  @Test
  void wrongMethodIsNotAllowed() throws Exception {
    mockMvc
        .perform(patch("/api/v1/products"))
        .andExpect(status().isMethodNotAllowed())
        .andExpect(jsonPath("$.code").value("METHOD_NOT_ALLOWED"))
        .andExpect(jsonPath("$.message").value("Method PATCH is not allowed for /api/v1/products"));
  }

  // ---------------------------------------------------------------- business and data errors

  @Test
  void businessExceptionsCarryTheirCode() throws Exception {
    when(service.get(42L)).thenThrow(new ProductNotFoundException(42L));
    when(service.create(any())).thenThrow(new DuplicateSkuException("ABC-1"));

    mockMvc
        .perform(get("/api/v1/products/42"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.code").value("PRODUCT_NOT_FOUND"))
        .andExpect(jsonPath("$.message").value("Product 42 not found"))
        .andExpect(jsonPath("$.path").value("/api/v1/products/42"));
    postJson(
            """
            {"sku": "ABC-1", "name": "Mug", "price": "9.99"}
            """)
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.code").value("DUPLICATE_SKU"))
        .andExpect(jsonPath("$.message").value("A product with SKU ABC-1 already exists"));
  }

  @Test
  void optimisticLockConflictIs409() throws Exception {
    when(service.update(eq(1L), any()))
        .thenThrow(new ObjectOptimisticLockingFailureException(Product.class, 1L));

    putJson(
            """
            {"name": "Mug", "price": "9.99", "status": "ACTIVE"}
            """)
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.code").value("CONCURRENT_UPDATE"));
  }

  @Test
  void databaseConstraintIs409() throws Exception {
    when(service.create(any())).thenThrow(new DataIntegrityViolationException("duplicate key"));

    postJson(
            """
            {"sku": "ABC-1", "name": "Mug", "price": "9.99"}
            """)
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.code").value("CONFLICT"));
  }

  @Test
  void unexpectedErrorsHideTheirDetails() throws Exception {
    when(service.get(anyLong())).thenThrow(new IllegalStateException("secret internal detail"));

    mockMvc
        .perform(get("/api/v1/products/1"))
        .andExpect(status().isInternalServerError())
        .andExpect(jsonPath("$.code").value("INTERNAL_ERROR"))
        .andExpect(jsonPath("$.message").value("An unexpected error occurred"));
  }
}
