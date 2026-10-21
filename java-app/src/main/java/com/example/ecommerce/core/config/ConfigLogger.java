package com.example.ecommerce.core.config;

import java.util.Arrays;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

/** Logs the loaded (non-secret) settings once at startup, including which database is used. */
@Slf4j
@Component
@RequiredArgsConstructor
class ConfigLogger implements ApplicationRunner {

  private final AppProperties appProperties;
  private final Environment environment;

  @Override
  public void run(ApplicationArguments args) {
    String[] active = environment.getActiveProfiles();
    // With no profile set explicitly, the active list is empty and the default profile applies
    log.info(
        "Profiles: {}",
        active.length > 0
            ? Arrays.toString(active)
            : Arrays.toString(environment.getDefaultProfiles()) + " (default)");
    log.info("Configuration loaded: {}", appProperties);
    // Never log the password
    log.info(
        "Database: {} as user {}",
        environment.getProperty("spring.datasource.url", "(not configured)"),
        environment.getProperty("spring.datasource.username", "(none)"));
  }
}
