# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django package that provides `NativeShortUUIDField` - a custom Django model field that stores UUIDs in the database but presents them as base-57 encoded short UUIDs (20-22 characters) in Python/forms. It bridges the gap between full UUIDs and their shorter representations using the `shortuuid` library.

The package supports two main field types:
- `NativeShortUUIDField`: Standard short UUID field (up to 22 chars)
- `NativeShortUUID20Field`: Fixed 20-character short UUID field with special handling for legacy 22-char values

## Development Commands

This project uses **hatch** for all Python, library, and PyPI publishing management.

### Testing
```bash
# Run all tests
hatch run test

# Or directly (legacy)
python runtests.py
```

### Linting and Formatting
```bash
# Check code style with flake8
hatch run lint

# Check import sorting
hatch run format-check

# Fix import sorting
hatch run format
```

### Build and Package
```bash
# Build package
hatch run package

# Or directly
hatch build

# Publish to PyPI
hatch publish

# Clean build artifacts
hatch clean
```

### Environment Management
```bash
# Show available environments and scripts
hatch env show

# Create/update development environment
hatch env create

# Remove environment
hatch env remove default
```

## Code Architecture

### Core Components

1. **Fields Module** (`native_shortuuid/fields.py`):
   - `NativeShortUUIDField`: Main Django model field that inherits from UUIDField
   - `NativeShortUUID20Field`: 20-character variant with legacy 22-char support
   - Form fields: `NativeShortUUIDFormField`, `NativeShortUUID20FormField`
   - DRF serializer fields: `NativeShortUUIDSerializerField`, `NativeShortUUID20SerializerField`
   - Utility functions: `decode()`, `short_uuid4()`, `convert_uuid_to_uuid_v2()`

2. **Admin Integration** (`native_shortuuid/admin.py`):
   - `NativeUUIDSearchMixin`: Enables searching by short UUID in Django admin
   - `NativeUUID20SearchMixin`: Variant for 20-character fields
   - Automatically extracts UUID search fields from `search_fields`

3. **Validation** (`native_shortuuid/validation.py`):
   - `validate_shortuuid()`: Validates short UUID format
   - Django URL converters: `ShortUUIDConverter`, `ShortUUID20Converter`
   - Supports both 20 and 22 character short UUIDs

### Key Architecture Decisions

- **Database Storage**: UUIDs are stored as native UUID type in database for efficiency
- **Python Representation**: Converted to/from short UUIDs in Python layer using `shortuuid.encode()`/`shortuuid.decode()`
- **Length Handling**: The 20-char variant handles legacy 22-char values by trimming first 2 characters
- **Form Integration**: Custom form fields provide validation and proper display
- **Admin Search**: Special mixins enable searching by short UUID values in Django admin

### Testing Structure

Tests are in `tests/` directory with:
- `test_shortuuid_field.py`: Comprehensive field behavior tests
- `models.py`: Test models for various field configurations
- `test_settings.py`: Django settings for test environment

### Dependencies

Core dependencies:
- `django>=1.11`
- `djangorestframework>=3.13.1` 
- `django-shortuuidfield`
- `shortuuid` (for encoding/decoding)

Development dependencies managed by hatch in `pyproject.toml`:
- `isort` (import sorting)
- `flake8` (code style)
- `django`, `djangorestframework`, `shortuuid`

## Project Management

### Tool Preferences
- Use hatch for all python, library, and pypi publishing management

## Commit Guidelines

- When writing git commit messages, omit all mention of claude