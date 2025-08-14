# Test File in Subfolder

This is a test file to demonstrate that the subfolder mapping functionality works correctly.

## Features

- Files in `folder1/subfolder/` will now be mapped to the OneDrive folder specified in the configuration
- The mapping uses the most specific (longest) path match
- Both top-level folders and subfolders are supported

## Example

- `folder1/file.md` → Maps to `folder1` OneDrive folder!!
- `folder1/subfolder/file.md` → Maps to `folder1/subfolder` OneDrive folder (if configured)
- `folder2/file.md` → Maps to `folder2` OneDrive folder 