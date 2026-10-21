package com.example.ecommerce.product.web;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.ecommerce.product.exception.DuplicateSkuException;
import com.example.ecommerce.product.exception.ProductNotFoundException;
import com.example.ecommerce.product.model.Product;
import com.example.ecommerce.product.model.ProductStatus;
import com.example.ecommerce.product.model.ProductUpdate;
import com.example.ecommerce.product.service.ProductService;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Slice test: starts only the web layer (this controller, JSON, MockMvc) with a mocked service. It
 * checks HTTP concerns: paths, status codes, headers and JSON.
 */
@WebMvcTest(ProductController.class)
@ActiveProfiles("test")
class ProductControllerTest {

  @Autowired private MockMvc mockMvc;

  @MockitoBean private ProductService service; // replaces the real bean in the Spring context

  private static Product mug() {
    return Product.builder().id(1L).sku("MUG-1").name("Mug").price(new BigDecimal("9.99")).build();
  }

  @Test
  void listReturnsProducts() throws Exception {
    when(service.list()).thenReturn(List.of(mug()));

    mockMvc
        .perform(get("/api/v1/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].sku").value("MUG-1"))
        .andExpect(jsonPath("$[0].price").value(9.99));
  }

  @Test
  void getReturnsProduct() throws Exception {
    when(service.get(1L)).thenReturn(mug());

    mockMvc
        .perform(get("/api/v1/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.name").value("Mug"));
  }

  @Test
  void getReturns404WhenMissing() throws Exception {
    when(service.get(42L)).thenThrow(new ProductNotFoundException(42L));

    mockMvc.perform(get("/api/v1/products/42")).andExpect(status().isNotFound());
  }

  @Test
  void createReturns201WithLocation() throws Exception {
    when(service.create(any())).thenReturn(mug());

    mockMvc
        .perform(
            post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {"sku": "MUG-1", "name": "Mug", "price": 9.99}
                    """))
        .andExpect(status().isCreated())
        .andExpect(header().string("Location", "/api/v1/products/1"))
        .andExpect(jsonPath("$.id").value(1));

    // "status" was not in the JSON, so the product must default to ACTIVE
    ArgumentCaptor<Product> received = ArgumentCaptor.forClass(Product.class);
    verify(service).create(received.capture());
    assertThat(received.getValue().getStatus()).isEqualTo(ProductStatus.ACTIVE);
  }

  @Test
  void createReturns409OnDuplicateSku() throws Exception {
    when(service.create(any())).thenThrow(new DuplicateSkuException("MUG-1"));

    mockMvc
        .perform(
            post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"sku\": \"MUG-1\", \"name\": \"Mug\", \"price\": 9.99}"))
        .andExpect(status().isConflict());
  }

  @Test
  void updateReturnsUpdatedProduct() throws Exception {
    Product updated = mug();
    updated.setName("Big mug");
    when(service.update(eq(1L), any(ProductUpdate.class))).thenReturn(updated);

    mockMvc
        .perform(
            put("/api/v1/products/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    """
                    {"name": "Big mug", "description": "", "price": 9.99, "status": "ACTIVE"}
                    """))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.name").value("Big mug"));
  }

  @Test
  void deleteReturns204() throws Exception {
    mockMvc.perform(delete("/api/v1/products/1")).andExpect(status().isNoContent());
  }

  @Test
  void deleteReturns404WhenMissing() throws Exception {
    doThrow(new ProductNotFoundException(42L)).when(service).delete(42L);

    mockMvc.perform(delete("/api/v1/products/42")).andExpect(status().isNotFound());
  }
}
