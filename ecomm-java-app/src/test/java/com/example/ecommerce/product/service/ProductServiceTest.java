package com.example.ecommerce.product.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.ecommerce.product.exception.DuplicateSkuException;
import com.example.ecommerce.product.exception.ProductNotFoundException;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import com.example.ecommerce.product.model.ProductUpdate;
import com.example.ecommerce.product.repository.ProductRepository;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

/**
 * Unit tests with a Mockito mock instead of a real repository: we script its answers (when) and
 * check how the service used it (verify).
 */
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

  @Mock private ProductRepository repository;

  @InjectMocks private ProductService service; // created with the mock passed to its constructor

  private static Product mug(Long id) {
    return Product.builder().id(id).sku("MUG-1").name("Mug").price(new BigDecimal("9.99")).build();
  }

  @Test
  void createSavesWhenSkuIsNew() {
    when(repository.findBySku("MUG-1")).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(mug(1L));

    Product created = service.create(mug(null));

    assertThat(created.getId()).isEqualTo(1L);
  }

  @Test
  void createIgnoresAnIdOnTheInput() {
    when(repository.findBySku("MUG-1")).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(mug(1L));
    ArgumentCaptor<Product> saved = ArgumentCaptor.forClass(Product.class);

    service.create(mug(99L));

    verify(repository).save(saved.capture());
    assertThat(saved.getValue().getId()).isNull();
  }

  @Test
  void createRejectsDuplicateSkuAndNeverSaves() {
    when(repository.findBySku("MUG-1")).thenReturn(Optional.of(mug(1L)));

    assertThatThrownBy(() -> service.create(mug(null)))
        .isInstanceOf(DuplicateSkuException.class)
        .hasMessageContaining("MUG-1");
    verify(repository, never()).save(any());
  }

  @Test
  void listAsksForTheRequestedPageOrderedById() {
    Page<Product> page = new PageImpl<>(List.of(mug(1L)), PageRequest.of(2, 5), 11);
    ArgumentCaptor<Pageable> requested = ArgumentCaptor.forClass(Pageable.class);
    when(repository.findAll(requested.capture())).thenReturn(page);

    assertThat(service.list(2, 5).getContent()).containsExactly(mug(1L));
    assertThat(requested.getValue().getPageNumber()).isEqualTo(2);
    assertThat(requested.getValue().getPageSize()).isEqualTo(5);
    assertThat(requested.getValue().getSort()).isEqualTo(Sort.by("id"));
  }

  @Test
  void getThrowsWhenMissing() {
    when(repository.findById(42L)).thenReturn(Optional.empty());

    assertThatThrownBy(() -> service.get(42L))
        .isInstanceOf(ProductNotFoundException.class)
        .hasMessage("Product 42 not found");
  }

  @Test
  void updateChangesFieldsButKeepsSku() {
    when(repository.findById(1L)).thenReturn(Optional.of(mug(1L)));
    when(repository.save(any())).thenAnswer(call -> call.getArgument(0));

    Product updated =
        service.update(
            1L,
            new ProductUpdate(
                "Big mug", "500 ml", new BigDecimal("14.50"), ProductStatus.DISCONTINUED));

    assertThat(updated.getName()).isEqualTo("Big mug");
    assertThat(updated.getPrice()).isEqualByComparingTo("14.50");
    assertThat(updated.getStatus()).isEqualTo(ProductStatus.DISCONTINUED);
    assertThat(updated.getSku()).isEqualTo("MUG-1");
  }

  @Test
  void updateThrowsWhenMissingAndNeverSaves() {
    when(repository.findById(42L)).thenReturn(Optional.empty());

    assertThatThrownBy(
            () ->
                service.update(
                    42L, new ProductUpdate("x", "", BigDecimal.ONE, ProductStatus.ACTIVE)))
        .isInstanceOf(ProductNotFoundException.class);
    verify(repository, never()).save(any());
  }

  @Test
  void deleteThrowsWhenMissingAndNeverSaves() {
    when(repository.findById(42L)).thenReturn(Optional.empty());

    assertThatThrownBy(() -> service.delete(42L)).isInstanceOf(ProductNotFoundException.class);
    verify(repository, never()).save(any());
  }

  @Test
  void deleteIsASoftDeleteThatDiscontinuesTheProduct() {
    when(repository.findById(1L)).thenReturn(Optional.of(mug(1L)));
    ArgumentCaptor<Product> saved = ArgumentCaptor.forClass(Product.class);

    service.delete(1L);

    verify(repository).save(saved.capture());
    assertThat(saved.getValue().getStatus()).isEqualTo(ProductStatus.DISCONTINUED);
    assertThat(saved.getValue().getId()).isEqualTo(1L);
  }

  @Test
  void createResetsDatabaseManagedFields() {
    when(repository.findBySku("MUG-1")).thenReturn(Optional.empty());
    when(repository.save(any())).thenAnswer(call -> call.getArgument(0));
    Product fromClient = mug(99L).toBuilder().version(7L).build();

    Product created = service.create(fromClient);

    assertThat(created.getId()).isNull();
    assertThat(created.getVersion()).isNull();
  }
}
