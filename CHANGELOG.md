# Changelog

All notable changes to HuanMo are documented here. The project follows semantic versioning for published releases.

## [Unreleased]

- Professionalized project documentation and community files.
- Added automated scan-regression tests for pull requests.

## [1.1.1] - 2026-09-30

### Fixed

- Preserve original colors by default instead of forcing grayscale output.
- Preserve landscape orientation when EXIF is already correct.
- Avoid mistaking large tables or colored blocks for the page boundary.
- Preserve color after manual page rotation.

### Added

- Original color, enhanced color, and black-and-white scan styles.

## [1.1.0] - 2026-09-30

### Added

- Mobile document scanning with perspective correction.
- HEIC/HEIF and common image format support.
- Scan preview, page rotation, deletion, reordering, and A4 PDF export.

## [1.0.3] - 2026-08-02

### Fixed

- Windows PDF preview packaging.
- Native PNG preview encoding without a Pillow dependency.

## [1.0.0] - 2026-08-01

### Added

- Markdown, TXT, and DOCX conversion to PDF.
- Page-level PDF preview, deletion, ordering, and merging.
- Standalone macOS and Windows builds.

[Unreleased]: https://github.com/Forwindreach/HuanMo/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/Forwindreach/HuanMo/releases/tag/v1.1.1
[1.1.0]: https://github.com/Forwindreach/HuanMo/releases/tag/v1.1.0
[1.0.3]: https://github.com/Forwindreach/HuanMo/releases/tag/v1.0.3
[1.0.0]: https://github.com/Forwindreach/HuanMo/releases/tag/v1.0.0
