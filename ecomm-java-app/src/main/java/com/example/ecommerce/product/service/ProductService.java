package com.example.ecommerce.product.service;

import com.example.ecommerce.product.exception.DuplicateSkuException;
import com.example.ecommerce.product.exception.ProductNotFoundException;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import com.example.ecommerce.product.model.ProductUpdate;
import com.example.ecommerce.product.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Business rules for the catalog. Controllers call this; only this calls the repository.
 *
 * <p>Each public method runs in one database transaction: a check and the write that depends on it
 * either both happen or neither does.
 */
@Service
@RequiredArgsConstructor // generates a constructor for the final field; Spring injects the bean
public class ProductService {

  private final ProductRepository repository;

  /**
   * Creates a product; the SKU must be unique. Fields the database manages (id, version,
   * timestamps) are ignored if the caller sent them.
   */
  @Transactional
  public Product create(Product product) {
    if (repository.findBySku(product.getSku()).isPresent()) {
      throw new DuplicateSkuException(product.getSku());
    }
    return repository.save(
        product.toBuilder().id(null).version(null).createdAt(null).updatedAt(null).build());
  }

  @Transactional(readOnly = true)
  public Product get(long id) {
    return repository.findById(id).orElseThrow(() -> new ProductNotFoundException(id));
  }

  /**
   * One page of the catalog, ordered by id so pages are stable. Page numbers start at 0; a page
   * past the end is empty. The controller validates page and size.
   */
  @Transactional(readOnly = true)
  public Page<Product> list(int page, int size) {
    return repository.findAll(PageRequest.of(page, size, Sort.by("id")));
  }

  /** Changes name, description, price and status. The SKU never changes. */
  @Transactional
  public Product update(long id, ProductUpdate update) {
    Product product = get(id);
    product.setName(update.name());
    product.setDescription(update.description());
    product.setPrice(update.price());
    product.setStatus(update.status());
    return repository.save(product);
  }

  /**
   * Soft delete (spec rule SN-4): the product becomes DISCONTINUED instead of being removed,
   * because carts and orders reference it. It stays readable by id.
   */
  @Transactional
  public void delete(long id) {
    Product product = get(id);
    product.setStatus(ProductStatus.DISCONTINUED);
    repository.save(product);
  }
}
