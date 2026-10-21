package com.example.ecommerce.product.web;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.ecommerce.TestcontainersConfiguration;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

/** The whole app, HTTP down to PostgreSQL (Testcontainers): controller → service → JPA → table. */
@SpringBootTest
@AutoConfigureMockMvc
@Import(TestcontainersConfiguration.class)
@ActiveProfiles("test")
class ProductApiIntegrationTest {

  @Autowired private MockMvc mockMvc;

  @Test
  void createListSoftDeleteRoundTripThroughTheDatabase() throws Exception {
    String body =
        """
        {"sku": "INT-1", "name": "Integration mug", "price": "11.25"}
        """;
    String location =
        mockMvc
            .perform(post("/api/v1/products").contentType(MediaType.APPLICATION_JSON).content(body))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.status").value("ACTIVE"))
            .andExpect(jsonPath("$.version").value(0))
            .andReturn()
            .getResponse()
            .getHeader("Location");

    mockMvc
        .perform(get("/api/v1/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[?(@.sku == 'INT-1')].price").value(11.25));

    // Same SKU again: the service finds it in the database
    mockMvc
        .perform(post("/api/v1/products").contentType(MediaType.APPLICATION_JSON).content(body))
        .andExpect(status().isConflict());

    // Soft delete: 204, then the product is still there, DISCONTINUED (SN-4)
    mockMvc.perform(delete(location)).andExpect(status().isNoContent());
    mockMvc
        .perform(get(location))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("DISCONTINUED"))
        .andExpect(jsonPath("$.version").value(1));
  }
}
