package com.example.ecommerce;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.MountableFile;

/**
 * A throwaway PostgreSQL 18 in Docker for tests that start the whole app, so tests never touch the
 * local or Docker database. Use with {@code @Import(TestcontainersConfiguration.class)}.
 *
 * <p>{@code @ServiceConnection} makes Spring Boot use this container's URL, user and password
 * instead of {@code spring.datasource.*}. The container is started once and reused by every test
 * class that shares the same Spring context.
 */
@TestConfiguration(proxyBeanMethods = false)
public class TestcontainersConfiguration {

  @Bean
  @ServiceConnection
  PostgreSQLContainer postgres() {
    return new PostgreSQLContainer("postgres:18")
        .withDatabaseName("ecomm_db")
        .withUsername("postgres")
        .withPassword("password")
        // Same schema as the real databases: the image runs this on first start, like compose
        .withCopyFileToContainer(
            MountableFile.forHostPath("../db/scripts/ecomm-setup.sql"),
            "/docker-entrypoint-initdb.d/01-ecomm-setup.sql");
  }
}
