# OneDrive Sync with PDF Conversion

This GitHub Action automatically uploads changed files to OneDrive and converts markdown files to PDF using pandoc.

## Features

### Step 1: File Upload
- Uploads all changed files from folders specified in `folder-mapping.yml`
- Supports any file type (not just markdown)
- Uses folder mappings to organize files in OneDrive

### Step 2: PDF Conversion
- Automatically converts `.md` and `.markdown` files to PDF
- Uses pandoc with custom LaTeX styling
- Applies professional formatting with headers, fonts, and layout

## Configuration

### folder-mapping.yml
```yaml
mappings:
  folder1: "your-onedrive-folder-id-1"
  folder2: "your-onedrive-folder-id-2"
  "folder1/subfolder": "your-onedrive-folder-id-3"  # Subfolder mapping example

# File patterns to include (supports glob patterns)
include_patterns:
  - "**/*"

# File patterns to exclude
exclude_patterns:
  - "**/node_modules/**"
  - "**/.git/**"
  - "**/package-lock.json"
  - "**/yarn.lock"
  - "**/.github/**"
  - "**/dist/**"
  - "**/build/**"
```

**Folder Mapping Rules:**
- Use forward slashes (`/`) as path separators
- The most specific (longest) matching path takes precedence
- Examples:
  - `folder1/file.md` → Maps to `folder1` OneDrive folder
  - `folder1/subfolder/file.md` → Maps to `folder1/subfolder` OneDrive folder (if configured)
  - `folder2/file.md` → Maps to `folder2` OneDrive folder

### meta.yaml
Contains pandoc metadata for PDF styling:
- Custom fonts (Gentium Book Plus)
- Professional headers with logo
- Consistent page layout
- Proper font fallbacks

## PDF Conversion Settings

The action uses the following pandoc parameters:
- `--variable=geometry:margin=0.8in`
- `--metadata-file=meta.yaml`
- `--pdf-engine=lualatex`
- `--variable=fontsize:11pt`

## Requirements

- OneDrive API credentials (Client ID, Client Secret, Refresh Token)
- pandoc and LaTeX (automatically installed in the GitHub Action)
- Node.js dependencies (see package.json)

## Usage

1. Set up your OneDrive API credentials as GitHub secrets:
   - `ONEDRIVE_CLIENT_ID`
   - `ONEDRIVE_CLIENT_SECRET`
   - `ONEDRIVE_REFRESH_TOKEN`

2. Configure your `folder-mapping.yml` with your OneDrive folder IDs

3. The action will automatically run on:
   - Push to main/master branch
   - Pull requests to main/master branch
   - Manual workflow dispatch

## Output

The action provides detailed logging for both steps:
- Step 1: File upload summary
- Step 2: PDF conversion and upload summary
- Success/failure counts for each operation 