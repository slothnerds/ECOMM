package com.example.ecommerce.product.web;

import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductUpdate;
import com.example.ecommerce.product.service.ProductService;
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
 * <p>Stage 2 exposes the model classes directly; Stage 4 introduces request/response DTOs.
 */
@RestController
@RequestMapping("/api/v1/products")
@RequiredArgsConstructor
public class ProductController {

  private final ProductService service;

  @GetMapping
  public List<Product> list() {
    return service.list();
  }

  @GetMapping("/{id}")
  public Product get(@PathVariable long id) {
    return service.get(id);
  }

  /** 201 Created with a Location header pointing at the new product. */
  @PostMapping
  public ResponseEntity<Product> create(@RequestBody Product product) {
    Product created = service.create(product);
    return ResponseEntity.created(URI.create("/api/v1/products/" + created.getId())).body(created);
  }

  @PutMapping("/{id}")
  public Product update(@PathVariable long id, @RequestBody ProductUpdate update) {
    return service.update(id, update);
  }

  /** 204 No Content: success, nothing to return. */
  @DeleteMapping("/{id}")
  public ResponseEntity<Void> delete(@PathVariable long id) {
    service.delete(id);
    return ResponseEntity.noContent().build();
  }
}
