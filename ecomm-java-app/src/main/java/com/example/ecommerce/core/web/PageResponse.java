package com.example.ecommerce.core.web;

import java.util.List;
import java.util.function.Function;
import org.springframework.data.domain.Page;

/**
 * One page of results, the same JSON shape in the Python app. Our own record instead of Spring's
 * {@link Page}, whose JSON is verbose and not a stable contract.
 *
 * @param items the results on this page
 * @param page 0-based page number
 * @param size requested page size
 * @param totalItems number of results across all pages
 * @param totalPages number of pages (0 when there are no results)
 */
public record PageResponse<T>(List<T> items, int page, int size, long totalItems, int totalPages) {

  /** Converts a Spring Data page of entities, mapping each item to its DTO. */
  public static <E, T> PageResponse<T> from(Page<E> page, Function<E, T> mapper) {
    return new PageResponse<>(
        page.getContent().stream().map(mapper).toList(),
        page.getNumber(),
        page.getSize(),
        page.getTotalElements(),
        page.getTotalPages());
  }
}
