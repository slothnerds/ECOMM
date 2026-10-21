package com.example.ecommerce.product.web;

import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.service.ProductService;
import com.example.ecommerce.product.web.dto.CreateProductRequest;
import com.example.ecommerce.product.web.dto.ProductResponse;
import com.example.ecommerce.product.web.dto.UpdateProductRequest;
import java.net.URI;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Product CRUD endpoints: thin, they only translate HTTP to service calls.
 *
 * <p>Requests and responses are DTOs (package {@code dto}); the JPA entity never leaves the
 * service, so database details can change without changing the API, and vice versa.
 */
@RestController
@RequestMapping("/api/v1/products")
@RequiredArgsConstructor
public class ProductController {

  private final ProductService service;

  @GetMapping
  public List<ProductResponse> list() {
    return service.list().stream().map(ProductResponse::from).toList();
  }

  @GetMapping("/{id}")
  public ProductResponse get(@PathVariable long id) {
    return ProductResponse.from(service.get(id));
  }

  /** 201 Created with a Location header pointing at the new product. */
  @PostMapping
  public ResponseEntity<ProductResponse> create(@RequestBody CreateProductRequest request) {
    Product created = service.create(request.toProduct());
    return ResponseEntity.created(URI.create("/api/v1/products/" + created.getId()))
        .body(ProductResponse.from(created));
  }

  @PutMapping("/{id}")
  public ProductResponse update(@PathVariable long id, @RequestBody UpdateProductRequest request) {
    return ProductResponse.from(service.update(id, request.toUpdate()));
  }

  /** Soft delete: the product becomes DISCONTINUED (204 No Content). */
  @DeleteMapping("/{id}")
  public ResponseEntity<Void> delete(@PathVariable long id) {
    service.delete(id);
    return ResponseEntity.noContent().build();
  }
}
