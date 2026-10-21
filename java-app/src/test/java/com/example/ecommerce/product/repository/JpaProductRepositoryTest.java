package com.example.ecommerce.product.repository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.example.ecommerce.TestcontainersConfiguration;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase;
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager;
import org.springframework.context.annotation.Import;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.test.context.ActiveProfiles;

/**
 * Slice test: only the JPA layer, against a real PostgreSQL (Testcontainers) with the real schema.
 * Each test runs in a transaction that is rolled back afterwards, so tests don't see each other's
 * rows.
 */
@DataJpaTest
// Use the Testcontainers database, don't replace it with an in-memory one
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import({TestcontainersConfiguration.class, JpaProductRepository.class})
@ActiveProfiles("test")
class JpaProductRepositoryTest {

  @Autowired private ProductRepository repository;
  @Autowired private TestEntityManager entityManager;

  private static Product product(String sku) {
    return Product.builder().sku(sku).name("Product " + sku).price(new BigDecimal("9.99")).build();
  }

  /** Sends pending SQL to the database and forgets loaded objects, so reads hit the table. */
  private void flushAndClear() {
    entityManager.flush();
    entityManager.clear();
  }

  @Test
  void saveInsertsAndTheDatabaseFillsGeneratedColumns() {
    Product saved = repository.save(product("TST-1"));
    flushAndClear();

    Product loaded = repository.findById(saved.getId()).orElseThrow();
    assertThat(loaded.getId()).isPositive();
    assertThat(loaded.getVersion()).isZero();
    assertThat(loaded.getStatus()).isEqualTo(ProductStatus.ACTIVE);
    assertThat(loaded.getCreatedAt()).isNotNull();
    assertThat(loaded.getPrice()).isEqualByComparingTo("9.99");
  }

  @Test
  void findBySkuAndFindAllOrderedById() {
    Product first = repository.save(product("TST-1"));
    Product second = repository.save(product("TST-2"));
    flushAndClear();

    assertThat(repository.findBySku("TST-2")).contains(second);
    assertThat(repository.findBySku("NOPE-1")).isEmpty();
    assertThat(repository.findAll()).containsExactly(first, second);
  }

  @Test
  void updateIncrementsTheVersion() {
    Product saved = repository.save(product("TST-1"));
    flushAndClear();

    Product loaded = repository.findById(saved.getId()).orElseThrow();
    loaded.setPrice(new BigDecimal("12.00"));
    repository.save(loaded);
    flushAndClear();

    assertThat(repository.findById(saved.getId()).orElseThrow().getVersion()).isEqualTo(1L);
  }

  @Test
  void databaseRejectsADuplicateSku() {
    repository.save(product("TST-1"));

    // The service checks first, but the unique constraint is the real guarantee (e.g. under races).
    // With IDENTITY ids Hibernate INSERTs immediately on save (it needs the generated id), so the
    // database rejects the row right here, not at a later flush.
    assertThatThrownBy(() -> repository.save(product("TST-1")))
        .isInstanceOf(DataIntegrityViolationException.class)
        .hasMessageContaining("products_sku_uq");
  }

  @Test
  void databaseRejectsANonPositivePrice() {
    assertThatThrownBy(
            () -> repository.save(product("TST-1").toBuilder().price(BigDecimal.ZERO).build()))
        .isInstanceOf(DataIntegrityViolationException.class)
        .hasMessageContaining("products_price_positive_chk");
  }

  @Test
  void staleUpdateFailsWithOptimisticLocking() {
    Long id = repository.save(product("TST-1")).getId();
    flushAndClear();

    // Two users load version 0 of the same product
    Product alice = repository.findById(id).orElseThrow();
    entityManager.detach(alice);
    Product bob = repository.findById(id).orElseThrow();

    bob.setName("Bob's change");
    repository.save(bob);
    entityManager.flush(); // version is now 1

    alice.setName("Alice's change, based on version 0");
    assertThatThrownBy(() -> repository.save(alice))
        .isInstanceOfAny(
            ObjectOptimisticLockingFailureException.class, DataIntegrityViolationException.class);
  }
}
