<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial creation)
- Added sections: All principles and governance sections
- Templates requiring updates: ✅ N/A (initial creation)
- Follow-up TODOs: None
-->

# CLI Todo App Constitution

## Core Principles

### I. CLI-First Design
Every feature must be accessible through a command-line interface; The application must follow standard CLI conventions with clear help text, argument parsing, and exit codes; Text-based input/output is the primary interface ensuring scriptability and automation.

### II. SQLite Persistent Storage
Task data is stored in an SQLite database file for persistence across application restarts; Tasks remain available after application quit and restart; Focus on reliable data storage and retrieval; Data is only removed when explicitly deleted by the user.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; Every feature must have corresponding unit tests before implementation.

### IV. Python 3.13+ Standards
Use modern Python 3.13+ syntax and features; Follow PEP 8 style guidelines; Leverage type hints for all public interfaces; Use UV for dependency management and virtual environments.

### V. Clean Architecture
Separate business logic from presentation layer; Follow single responsibility principle; Maintain clear boundaries between components; Code should be modular and easily testable.

### VI. User Experience Focus
Commands must be intuitive and self-documenting; Error messages should be helpful and actionable; Provide clear feedback for all operations; Consistent formatting across all output.

## Additional Constraints

Technology Stack: Python 3.13+, UV, Claude Code, Spec-Kit Plus
Project Scope: Command-line interface only, no GUI components
Functionality: Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
File Structure: Organize code in /src directory with proper Python packaging

## Development Workflow

Code Review: All changes must pass review before merging
Testing: All features must include unit tests with reasonable coverage
Quality Gates: Code must pass linting and testing before acceptance
Documentation: Public APIs and user-facing features must be documented

## Governance

This constitution supersedes all other development practices for this project; All amendments must be documented with clear justification and approval; The project must align with the specified feature progression from Basic to Advanced levels; Compliance with these principles is verified during code reviews.

All pull requests and reviews must verify constitutional compliance; Complexity must be justified with clear benefits; Use CLAUDE.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
