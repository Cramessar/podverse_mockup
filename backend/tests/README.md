# Testing Guide

## Directory Structure
```
/tests
├── unit/                  # Logic-level tests, fully mocked
│   └── blueprints/       # Mirrors application structure
├── integration/          # Real DB, app context tests
├── e2e/                 # Endpoint tests, HTTP requests (haven't done yet fi needed)
├── fixtures/            # Shared fixtures and test data
├── conftest.py         # Shared fixtures
└── pytest.ini          # Test configuration
```

## Test Categories

### Unit Tests
- Located in `/unit/`
- Mock all external dependencies (DB, APIs)
- Test individual components in isolation
- Follow naming convention: `test_<module>.py`
- Run with: `pytest tests/unit`

### Integration Tests
- Located in `/integration/`
- Use test database
- Test complete workflows
- Follow naming convention: `test_<workflow>.py`
- Run with: `pytest tests/integration`

### End-to-End Tests
- Located in `/e2e/`
- Test complete HTTP endpoints
- Follow naming convention: `test_<endpoint>.py`
- Run with: `pytest tests/e2e`

## Fixtures

### Global Fixtures
- Located in `/fixtures/` and main `conftest.py`
- Shared across all tests
- Include:
  - Database connections
  - API clients
  - Authentication helpers

### Local Fixtures
- Located in directory-specific `conftest.py` files
- Specific to test module or directory
- Include test-specific data and setup

## Running Tests

### All Tests
```bash
pytest
```

### Specific Categories
```bash
pytest tests/unit  # Run unit tests
pytest tests/integration  # Run integration tests
pytest tests/e2e  # Run e2e tests
```

### With Markers
```bash
pytest -m unit  # Run tests marked as unit
pytest -m integration  # Run tests marked as integration
pytest -m e2e  # Run tests marked as e2e
```

## Best Practices

1. **Unit Tests**
   - Mock all external dependencies (no DB),
   - One test file per module
   - Clear, descriptive test names
   - Test one thing per test function

2. **Integration Tests**
   - Test complete workflows
   - Use test database
   - Clean up after tests
   - Test realistic scenarios

3. **Fixtures**
   - Keep fixtures focused and simple
   - Use appropriate scope (function, class, module, session)
   - Clean up resources in fixture teardown
   - Document fixture purpose and usage

4. **General Guidelines**
   - Write descriptive test names
   - Follow AAA pattern (Arrange, Act, Assert)
   - Clean up test data
   - Keep tests independent
   - Use appropriate markers 

NOTE: Best way to write test is edge cases, extreme case (maximum/unusual conditions), minimum case (smallest/simplest input), middle case (typical/normal usage)