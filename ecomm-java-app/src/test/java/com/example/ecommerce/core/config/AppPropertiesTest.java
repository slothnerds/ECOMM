package com.example.ecommerce.core.config;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import org.junit.jupiter.api.Test;
import org.springframework.boot.autoconfigure.AutoConfigurations;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.boot.validation.autoconfigure.ValidationAutoConfiguration;
import org.springframework.context.annotation.Configuration;

/** Binds AppProperties in a tiny Spring context, without starting the whole app. */
class AppPropertiesTest {

  @Configuration
  @EnableConfigurationProperties(AppProperties.class)
  static class Config {}

  private final ApplicationContextRunner runner =
      new ApplicationContextRunner()
          .withConfiguration(AutoConfigurations.of(ValidationAutoConfiguration.class))
          .withUserConfiguration(Config.class)
          .withPropertyValues("app.environment=test", "app.hold-duration=PT15M");

  @Test
  void validSettingsAreBound() {
    runner
        .withPropertyValues("app.jwt-secret=a-valid-secret-that-is-32-chars-long!")
        .run(
            context -> {
              AppProperties props = context.getBean(AppProperties.class);
              assertThat(props.holdDuration()).isEqualTo(Duration.ofMinutes(15));
              assertThat(props.toString()).contains("jwtSecret=**********");
              assertThat(props.toString()).doesNotContain("a-valid-secret");
            });
  }

  @Test
  void shortJwtSecretFailsStartup() {
    runner
        .withPropertyValues("app.jwt-secret=too-short")
        .run(
            context ->
                assertThat(context)
                    .hasFailed()
                    .getFailure()
                    .rootCause()
                    .hasMessageContaining("must be at least 32 characters"));
  }

  @Test
  void unknownEnvironmentFailsStartup() {
    runner
        .withPropertyValues(
            "app.jwt-secret=a-valid-secret-that-is-32-chars-long!", "app.environment=staging")
        .run(context -> assertThat(context).hasFailed());
  }
}
