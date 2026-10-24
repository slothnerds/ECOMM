package com.example.ecommerce.product.web;

import static com.example.ecommerce.core.error.ValidationMessages.AT_LEAST_0;
import static com.example.ecommerce.core.error.ValidationMessages.AT_LEAST_1;
import static com.example.ecommerce.core.error.ValidationMessages.AT_MOST_100;

import com.example.ecommerce.core.web.PageResponse;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.service.ProductService;
import com.example.ecommerce.product.web.dto.CreateProductRequest;
import com.example.ecommerce.product.web.dto.ProductResponse;
import com.example.ecommerce.product.web.dto.UpdateProductRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import java.net.URI;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Product CRUD endpoints: thin, they only translate HTTP to service calls.
 *
 * <p>Requests and responses are DTOs (package {@code dto}); the JPA entity never leaves the
 * service, so database details can change without changing the API, and vice versa.
 *
 * <p>{@code @Valid} runs the DTO's validation annotations before the method; errors and exceptions
 * become the standard error body in {@code core.error.GlobalExceptionHandler}.
 */
@RestController
@RequestMapping("/api/v1/products")
@RequiredArgsConstructor
public class ProductController {

  private final ProductService service;

  /**
   * One page of products, ordered by id: {@code ?page=0&size=20}. The constraints on the parameters
   * are checked by Spring's built-in method validation; a violation becomes a 400 VALIDATION_FAILED
   * (deliberately not Spring's Pageable, which silently clamps bad values).
   */
  @GetMapping
  public PageResponse<ProductResponse> list(
      @RequestParam(defaultValue = "0") @Min(value = 0, message = AT_LEAST_0) int page,
      @RequestParam(defaultValue = "20")
          @Min(value = 1, message = AT_LEAST_1)
          @Max(value = 100, message = AT_MOST_100)
          int size) {
    return PageResponse.from(service.list(page, size), ProductResponse::from);
  }

  @GetMapping("/{id}")
  public ProductResponse get(@PathVariable long id) {
    return ProductResponse.from(service.get(id));
  }

  /** 201 Created with a Location header pointing at the new product. */
  @PostMapping
  public ResponseEntity<ProductResponse> create(@Valid @RequestBody CreateProductRequest request) {
    Product created = service.create(request.toProduct());
    return ResponseEntity.created(URI.create("/api/v1/products/" + created.getId()))
        .body(ProductResponse.from(created));
  }

  @PutMapping("/{id}")
  public ProductResponse update(
      @PathVariable long id, @Valid @RequestBody UpdateProductRequest request) {
    return ProductResponse.from(service.update(id, request.toUpdate()));
  }

  /** Soft delete: the product becomes DISCONTINUED (204 No Content). */
  @DeleteMapping("/{id}")
  public ResponseEntity<Void> delete(@PathVariable long id) {
    service.delete(id);
    return ResponseEntity.noContent().build();
  }
}
