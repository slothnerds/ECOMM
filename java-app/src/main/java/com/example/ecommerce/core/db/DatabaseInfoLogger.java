package com.example.ecommerce.core.db;

import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

/**
 * Proves the connection at startup: logs which server, database and schema were reached, and how
 * many products it holds. (Spring already fails fast if the database can't be reached.)
 */
@Slf4j
@Component
@RequiredArgsConstructor
class DatabaseInfoLogger implements ApplicationRunner {

  private final JdbcTemplate jdbc;

  @Override
  public void run(ApplicationArguments args) {
    Map<String, Object> info =
        jdbc.queryForMap(
            """
            SELECT current_setting('server_version') AS version,
                   current_database()               AS database,
                   current_schema()                 AS schema,
                   inet_server_port()               AS port,
                   -- -1 instead of an error if the tables haven't been created yet
                   CASE WHEN to_regclass('ecomm.products') IS NULL THEN -1
                        ELSE (SELECT count(*) FROM ecomm.products) END AS products
            """);
    log.info(
        "Connected to PostgreSQL {} on port {}: database {}, schema {}, {} products",
        info.get("version"),
        info.get("port"),
        info.get("database"),
        info.get("schema"),
        ((Number) info.get("products")).longValue() < 0 ? "no" : info.get("products"));
  }
}
