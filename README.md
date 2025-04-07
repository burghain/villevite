# Villevite City Generator

## Development Setup

### Blender

- Blender Preferences>File Paths>Asset Catalogs
  - Add the absolute Path for ./villevite/Assets as Asset Catalog (Name arbitrary)
  - Change import policy to link

## Architecture

### Assets

- Assets sorted in different blend files
- Each not larger than 100mb (github limitation, don't wanna use lfs)
- Every Collection that needs to be used individually (e.g. Building Walls) as separate Asset

### City Generator

### General Add-on Structure

- See BlenderAddonTemplate
