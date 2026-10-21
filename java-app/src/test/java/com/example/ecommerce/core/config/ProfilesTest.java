package com.example.ecommerce.core.config;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.ConfigDataApplicationContextInitializer;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.core.env.Environment;

/**
 * Checks which database each profile selects, by loading only the application*.yml files into a
 * tiny context: no beans and no database connection, so it never touches a real database.
 */
class ProfilesTest {

  private final ApplicationContextRunner runner =
      new ApplicationContextRunner().withInitializer(new ConfigDataApplicationContextInitializer());

  @Test
  void defaultProfileIsLocalOnPort5433() {
    runner.run(
        context -> {
          Environment env = context.getEnvironment();
          // With no profile set explicitly, Spring reports the fallback via getDefaultProfiles();
          // getActiveProfiles() stays empty
          assertThat(env.getActiveProfiles()).isEmpty();
          assertThat(env.getDefaultProfiles()).contains("local");
          assertThat(env.getProperty("spring.datasource.url"))
              .isEqualTo("jdbc:postgresql://localhost:5433/ecomm_db");
          assertThat(env.getProperty("spring.datasource.username")).isEqualTo("postgres");
          // The local -> dev group also applies to the default profile
          assertThat(env.getProperty("app.environment")).isEqualTo("dev");
          assertThat(env.getProperty("app.jwt-secret")).startsWith("dev-only");
        });
  }

  @Test
  void dockerProfileUsesPort5432AndIncludesDevSettings() {
    runner
        .withPropertyValues("spring.profiles.active=docker")
        .run(
            context -> {
              Environment env = context.getEnvironment();
              assertThat(env.getActiveProfiles()).containsExactlyInAnyOrder("docker", "dev");
              assertThat(env.getProperty("spring.datasource.url"))
                  .isEqualTo("jdbc:postgresql://localhost:5432/ecomm_db");
              assertThat(env.getProperty("app.environment")).isEqualTo("dev");
            });
  }
}
