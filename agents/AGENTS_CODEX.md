# Instructions for Codex

This document defines instructions for Codex when working with this Django project.

## Task Processing Instructions
- Wait for all terminal commands to be completed before finishing
- Validate all changes before completing tasks
- Run all programmatic checks after making changes
- Handle errors and provide clear feedback

## Git Workflow
- Do not create new branches
- Use git to commit changes
- Run prek checks before committing
- Fix any prek issues and retry
- Check git status to confirm commits
- Leave worktree in a clean state
- Only committed code will be evaluated
- Do not modify or amend existing commits

## Project Standards
- Follow Django best practices
- Use PEP 8 style guide
- Maintain project structure
- Keep code organized by apps
- Use proper documentation
- Follow security guidelines

## File Locations
- New apps go in `/apps` directory
- Common code in `/apps/comun`
- Tests in `/tests` directory
- Templates in app-specific folders
- Static files organized by app

## Required Validations
Before completing any task:
1. Run all tests: `python manage.py test`
2. Check migrations: `python manage.py makemigrations --check`
3. Verify code style: `black .`
4. Run linting: `flake8`
5. Check security: `bandit -r .`

## Security Rules
- Never expose sensitive data
- Never modify .env files
- Use proper authentication
- Validate all inputs
- Follow security best practices
- Use secure defaults

## Documentation Requirements
- Update relevant documentation
- Add docstrings to new code
- Document API endpoints
- Update README.md when needed
- Include usage examples

## Citations Format
When referencing files or terminal output:
1. File citations:
   - Format: `【F:<file_path>†L<line_start>(-L<line_end>)?】`
   - Use relative paths from repo root
   - Include exact line numbers

2. Terminal output citations:
   - Format: `【<chunk_id>†L<line_start>(-L<line_end>)?】`
   - Reference specific output lines
   - Only cite relevant content

Citation Rules:
- Always cite code changes
- Use correct line numbers
- Don't cite empty lines
- Prefer file citations over terminal citations
- Only use terminal citations for relevant output
- Don't cite PR diffs or git hashes
- Cite documentation changes
- Include test results with terminal citations

## Scope Rules
- These instructions apply to entire directory tree
- More nested AGENTS.md files take precedence
- Direct user instructions override these rules
- Style rules apply only within scope
- Follow all instructions for touched files
