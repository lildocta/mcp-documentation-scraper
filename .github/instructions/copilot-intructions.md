# GitHub Copilot Instructions

## Coding Guidelines
- Follow the project's coding standards and style guides
- Use meaningful variable and function names
- Write clear and concise comments where necessary
- Avoid complex logic in a single function; break it down into smaller, reusable functions
- Ensure code is modular and adheres to the DRY (Don't Repeat Yourself) principle

### Python Specifics
- Use `PEP 8` for Python code style
- Use type hints for function signatures
- Prefer `f-strings` for string formatting
- Use `async` and `await` for asynchronous code
- Handle exceptions gracefully and log errors appropriately

## Single Story Development Protocol

### Story Management
- Work on **ONE story at a time** only
- Complete the current story fully before starting any new work
- Ensure all story requirements are met before moving forward

### Testing Requirements
Upon story completion:

1. **Create comprehensive tests** for the new functionality
    - Unit tests for individual components
    - Integration tests for feature workflows
    - Edge case and error handling tests

2. **Run full regression suite**
    - Execute all existing tests
    - Verify no breaking changes
    - Fix any failing tests before story closure

3. **Test Coverage Validation**
    - Ensure new code meets minimum coverage requirements
    - Document any testing gaps or limitations

### Story Completion Checklist
- [ ] All acceptance criteria met
- [ ] New tests written and passing
- [ ] Full test suite runs successfully
- [ ] Code reviewed and approved
- [ ] Documentation updated if needed
- [ ] Run Git commands 
    - commit changes to the branch 
    - push those changes to the remote repository
    - create a pull request for review
    - merge the pull request once approved
    - create and checkout a new branch for the next story

Do not move on to the next story, a new chat should be started for each story.