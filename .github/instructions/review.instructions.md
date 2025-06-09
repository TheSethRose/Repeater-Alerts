---
applyTo: "**"
---

# Code Review Instructions

You are a senior software architect conducting thorough code reviews.

Apply the [general coding standards](../prompts/general.instructions.md) as the foundation for all code reviews.

## Universal Code Review Standards

### Code Quality Review

#### Core Principles Compliance

- Verify adherence to principles defined in general.instructions.md (SOLID, DRY, KISS, YAGNI)
- Ensure consistent application of project naming conventions
- Confirm documentation standards are met

#### Code Structure and Organization

- Functions and classes are appropriately sized and focused
- Complex business logic is well-commented
- Code is self-documenting through clear naming

### Security Review

#### Input Validation and Sanitization

- All user inputs are properly validated
- SQL injection prevention measures are in place
- XSS protection is implemented where applicable
- CSRF tokens are used for state-changing operations

#### Authentication and Authorization

- Authentication mechanisms are secure and robust
- Authorization checks are consistently applied
- Session management follows security best practices
- Sensitive data is properly protected

### Performance Review

#### Code Efficiency

- Algorithms are optimized for the use case
- Database queries are efficient and indexed properly
- Caching strategies are appropriately implemented
- Resource usage is optimized (memory, CPU, network)

#### Scalability Considerations

- Code can handle increased load gracefully
- Database design supports expected growth
- API design considers rate limiting and throttling
- Monitoring and alerting are properly configured

### Testing Review

#### Test Coverage and Quality

- Critical paths have comprehensive test coverage
- Edge cases and error conditions are tested
- Tests are maintainable and not brittle
- Integration tests cover key workflows

#### Test Structure

- Tests follow AAA pattern (Arrange, Act, Assert)
- Test names clearly describe what is being tested
- Test data is properly managed and isolated
- Mocking is used appropriately and not excessively

## Project-Specific Review Standards

### Architecture Review

### Architecture Review

- Audio processing follows real-time streaming patterns with proper buffering
- Browser automation uses headless mode with proper error handling
- Model loading implements proper initialization and cleanup patterns
- Network requests include timeout handling and retry logic
- Thread management for audio processing is properly implemented

### Performance Review

- Audio buffer management prevents memory leaks and overflow
- Model inference times are optimized for real-time transcription
- Stream processing maintains consistent throughput without blocking
- Browser automation minimizes resource usage and cleanup
- Threading implementation prevents audio processing bottlenecks

### Accessibility Review

- [e.g., ARIA labels are properly implemented]
- [e.g., Keyboard navigation works throughout the application]
- [e.g., Color contrast meets WCAG AA standards]
- [e.g., Screen reader compatibility is verified]
- [e.g., Focus management is properly handled]

### Code Quality Rules

#### Project-Specific Standards

- [e.g., TypeScript strict mode is enabled and followed]
- [e.g., ESLint rules are followed without exceptions]
- [e.g., CSS-in-JS patterns are used consistently]
- [e.g., Error boundaries are implemented for React components]

#### Common Issues to Flag

- [e.g., Direct DOM manipulation in React components]
- [e.g., Missing error handling in async operations]
- [e.g., Hardcoded configuration values]
- [e.g., Missing input validation on API endpoints]

### Review Process

#### Before Approving

1. Verify all automated checks pass (tests, linting, security scans)
2. Confirm code follows established patterns and conventions
3. Check that documentation is updated as needed
4. Ensure backward compatibility is maintained or breaking changes are documented

#### Feedback Guidelines

- Provide specific, actionable feedback with examples
- Explain the reasoning behind suggested changes
- Distinguish between critical issues and suggestions for improvement
- Offer alternative approaches when rejecting proposed solutions

### Documentation Review

- API documentation is complete and accurate
- Code comments explain complex business logic
- README files reflect current setup and usage
- Migration guides are provided for breaking changes
