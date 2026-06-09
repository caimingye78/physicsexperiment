```markdown
# physicsexperiment Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `physicsexperiment` Python codebase. You'll learn how to structure files, write imports and exports, and follow the project's testing and workflow practices. This guide is ideal for contributors looking to maintain consistency and quality in their code contributions.

## Coding Conventions

### File Naming
- Use **camelCase** for all file names.
  - Example: `dataProcessor.py`, `experimentRunner.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .dataProcessor import processData
    ```

### Export Style
- Use **named exports** by defining functions, classes, or variables explicitly.
  - Example:
    ```python
    def runExperiment():
        pass

    class Experiment:
        pass
    ```

### Commit Messages
- Freeform style, no strict prefixes.
- Average commit message length: ~81 characters.
  - Example:  
    ```
    Add initial data processing logic for temperature measurements
    ```

## Workflows

### Adding a New Experiment Module
**Trigger:** When you need to add a new physics experiment to the codebase  
**Command:** `/add-experiment`

1. Create a new Python file using camelCase (e.g., `newExperiment.py`).
2. Implement your experiment logic using functions and/or classes.
3. Use relative imports to access shared utilities or data processors.
4. Export your main functions/classes with named exports.
5. Add corresponding test files following the `*.test.*` pattern.
6. Commit your changes with a descriptive message.

### Running Tests
**Trigger:** When you want to verify code correctness  
**Command:** `/run-tests`

1. Locate test files matching the `*.test.*` pattern.
2. Use the project's preferred (unknown) test runner to execute tests.
3. Review test output and address any failures.

### Refactoring Code
**Trigger:** When improving or restructuring existing code  
**Command:** `/refactor`

1. Identify code to refactor.
2. Rename files using camelCase if needed.
3. Update relative imports accordingly.
4. Ensure all exports remain named and explicit.
5. Run tests to confirm nothing is broken.
6. Commit with a clear, descriptive message.

## Testing Patterns

- Test files follow the pattern: `*.test.*` (e.g., `dataProcessor.test.py`).
- The specific testing framework is unknown, but standard Python test practices likely apply.
- Place test files alongside or near the code they test.

**Example test file:**
```python
# dataProcessor.test.py
from .dataProcessor import processData

def test_processData():
    assert processData([1, 2, 3]) == expected_result
```

## Commands
| Command         | Purpose                                      |
|-----------------|----------------------------------------------|
| /add-experiment | Scaffold a new experiment module             |
| /run-tests      | Run all test files in the codebase           |
| /refactor       | Refactor code and update imports/exports     |
```
