# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-07-04

### Added
- **Automated CI/CD**: Added a GitHub Actions workflow using OIDC (Trusted Publishing) for automated, secure PyPI deployments on new GitHub Releases.
- **Enterprise Edge Case Protections**: Built a background transpiler to auto-backtick column headers containing spaces to support dirty real-world enterprise datasets without syntax crashes.

### Changed
- **Memory Optimization (Pandas)**: The Pandas backend now automatically requires the `pyarrow` multi-threaded C++ engine when loading large CSV files, heavily reducing physical RAM usage and preventing `MemoryError` crashes.
- **Datatype Coercion**: `Join.join` now dynamically casts mismatching datatypes between left and right anchor columns, eliminating strict PySpark `AnalysisException` errors when migrating disparate schemas.

### Fixed
- **Critical Security Fix**: Eradicated an arbitrary code execution vulnerability (RCE) in `Preparation.formula` by removing the insecure `eval()` fallback. The engine is now entirely zero-trust and sandboxed via `pd.eval` or strict `lambda` callables.
- **Spark Architecture (Sorting Death Trap)**: Completely refactored `Preparation.record_id` to utilize parallelized `F.monotonically_increasing_id()` instead of `Window.orderBy`, eliminating massive single-node memory bottlenecks when scaling Spark pipelines.
- **Spark Architecture (Tuple Bombs)**: Injected native `.persist()` boundaries directly into the upstream nodes of `Join.join` to prevent PySpark from redundantly computing the entire historical DAG multiple times during joins.
- **Regex Edge Cases**: Fixed an engine logic gap where Regex capture groups incorrectly counted non-capturing groups `(?:)` in the Spark backend.
## [0.2.0] — 2026-07-04

### Added
- **Enterprise Scalability (Dual-Backend Architecture)**: Added native support for distributed execution on big-data clusters using the new `SparkEngine`.
- **Thread-Safe Context Manager**: Added `Flowshift.backend()` context manager to allow concurrent multi-threading with different execution engines.
- **Dynamic Dispatch**: `Flowshift.set_backend("spark")` now seamlessly reroutes all tool executions down to Spark SQL and Vectorized Pandas UDFs (PyArrow).

### Changed
- All 55 Core tools have been refactored into thin dispatchers to support multiple engine backends without altering user-facing APIs.
- Updated `README.md` and created `USER_GUIDE.md` with complete documentation, tool reference tables, and declarative YAML pipeline configurations.

## [0.1.0] — 2025-06-28

- **InOut** class — `input_data`, `output_data`, `text_input`, `browse`, `directory`, `date_time_now`
- **Preparation** class — `filter`, `formula`, `select`, `data_cleansing`, `sort`, `unique`, `sample`, `record_id`, `generate_rows`, `auto_field`, `multi_field_formula`, `multi_row_formula`, `tile`, `imputation`
- **Join** class — `join`, `join_multiple`, `union`, `find_replace`, `append_fields`, `fuzzy_match`
- **Transform** class — `summarize`, `transpose`, `cross_tab`, `running_total`, `count_records`
- **Parse** class — `date_time`, `regex_match`, `regex_parse`, `regex_replace`, `regex_tokenize`, `text_to_columns`, `xml_parse`
- **Developer** class — `base64_encode`, `base64_decode`, `download`, `column_info`, `dynamic_rename`
- Full test suite with pytest
- Type hints and Google-style docstrings on all public methods
