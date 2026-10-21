package com.example.ecommerce.product.model;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.HashSet;
import java.util.Set;
import org.junit.jupiter.api.Test;

class ProductTest {

  @Test
  void builderSetsFieldsAndDefaultsToActiveStatus() {
    Product product =
        Product.builder().sku("ABC-1").name("Mug").price(new BigDecimal("12.50")).build();

    assertThat(product.getName()).isEqualTo("Mug");
    assertThat(product.getId()).isNull();
    assertThat(product.getStatus()).isEqualTo(ProductStatus.ACTIVE); // from @Builder.Default
    assertThat(product.getDescription()).isEmpty();
  }

  @Test
  void noArgsConstructorAlsoDefaultsToActiveStatus() {
    // Jackson uses this constructor (then setters) when JSON is deserialized
    assertThat(new Product().getStatus()).isEqualTo(ProductStatus.ACTIVE);
  }

  @Test
  void doubleIsInexactButBigDecimalIsExact() {
    assertThat(0.1 + 0.2).isNotEqualTo(0.3); // 0.30000000000000004
    assertThat(new BigDecimal("0.1").add(new BigDecimal("0.2"))).isEqualTo(new BigDecimal("0.3"));
  }

  @Test
  void bigDecimalFromDoubleCarriesTheError() {
    // Always build money from a String, never from a double
    assertThat(new BigDecimal(0.1)).isNotEqualTo(new BigDecimal("0.1"));
  }

  @Test
  void productsWithSameIdAreEqualEvenIfFieldsDiffer() {
    Product a = Product.builder().id(1L).name("Mug").price(new BigDecimal("10.00")).build();
    Product b = Product.builder().id(1L).name("Mug v2").price(new BigDecimal("12.00")).build();

    assertThat(a).isEqualTo(b).hasSameHashCodeAs(b);
  }

  @Test
  void unsavedProductsAreOnlyEqualToThemselves() {
    Product a = Product.builder().name("A").build();
    Product b = Product.builder().name("A").build();

    assertThat(a).isEqualTo(a).isNotEqualTo(b);
  }

  @Test
  void productIsNeverEqualToAnotherType() {
    Product product = Product.builder().id(1L).build();

    assertThat(product).isNotEqualTo("1").isNotEqualTo(null);
  }

  @Test
  void productStaysFindableInSetAfterIdIsAssigned() {
    Product product = Product.builder().name("Mug").build();
    Set<Product> set = new HashSet<>();
    set.add(product);

    product.setId(42L); // what saving to the database will do

    assertThat(set).contains(product);
  }
}
