# Publishing Guide

## Setup

The package is ready to publish to GitHub Package Registry for both NPM (TypeScript) and PyPI (Python).

## Prerequisites

### For NPM (GitHub Packages)

1. Create a GitHub Personal Access Token (PAT) with these scopes:
   - `write:packages`
   - `read:packages`
   - `repo`

2. Configure NPM authentication:
```bash
echo "//npm.pkg.github.com/:_authToken=YOUR_GITHUB_PAT" >> ~/.npmrc
```

### For Python (GitHub Packages)

1. Same PAT as above
2. Install twine:
```bash
pip install twine
```

## Publishing NPM Package

```bash
# Build
npm run build

# Publish to GitHub Packages
npm publish
```

The package will be available at:
```
@biosphere-labs/claude-langgraph-headless
```

### Installing the NPM Package

Users need to configure their `.npmrc`:
```
@biosphere-labs:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_GITHUB_PAT
```

Then install:
```bash
npm install @biosphere-labs/claude-langgraph-headless
```

## Publishing Python Package

```bash
cd python

# Build distribution
python setup.py sdist bdist_wheel

# Upload to GitHub Packages (requires personal access token)
TWINE_USERNAME=__token__
TWINE_PASSWORD=YOUR_GITHUB_PAT
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

### Installing the Python Package

```bash
pip install claude-langgraph-headless
```

## Current Status

✅ Code pushed to: https://github.com/biosphere-labs/claude-langgraph-headless
✅ Package.json configured for GitHub Packages
✅ Both TypeScript and Python versions tested and working
⏳ Awaiting PAT with `write:packages` scope to publish

## Automatic Publishing with GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish Package

on:
  release:
    types: [created]

jobs:
  publish-npm:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          registry-url: 'https://npm.pkg.github.com'
      - run: npm ci
      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}

  publish-python:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: |
          cd python
          pip install build twine
          python -m build
          twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{secrets.GITHUB_TOKEN}}
```

Then publishing is as simple as:
```bash
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0
```

The packages will be automatically published!
