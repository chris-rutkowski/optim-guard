# Optim Guard

**Optim Guard** is a GitHub Action designed to ensure your repository stays lean by preventing unoptimized images from being merged into your codebase. It detects unoptimized assets in pull requests, provides a downloadable artifact with optimized replacements, and blocks the PR until the issues are resolved.

---

## 🚀 Features
- **Prevents merging of unoptimized images**: Automatically flags unoptimized assets in pull requests.
- **Supports multiple image types**: Optimizes and validates images, including:
  - SVG
  - PNG
  - JPG/JPEG
  - WebP
  - GIF
  - PDF (converted to optimised SVG)
- **Customizable with ignore files**: Use a `.gitignore`-like file to exclude specific files or directories.
- **Download optimized assets**: Automatically uploads optimized images as a downloadable artifact for easy replacement.

---

## 🛠️ Usage

### 1. **Create an Ignore File**
Add a `optim_guard.ignore` file to the root of your repository to define patterns for files or directories to exclude from optimization. The syntax follows `.gitignore` conventions.

**Example `optim_guard.ignore`:**
```gitignore
test/*
logs/*
```

---

### 2. **Add the GitHub Action**
Create a GitHub Actions workflow in `.github/workflows/optim_guard.yml`:

```yaml
name: Optim Guard
on:
  pull_request:
    branches:
      - master

jobs:
  optim_guard:
    runs-on: ubuntu-latest
    steps:
      - name: Optim Guard
        uses: chris-rutkowski/optim-guard@v1.0.0
```

---

## ⚙️ Configuration

### **Specify a Custom Ignore File Path**
If your `optim_guard.ignore` file is not in the root directory, specify its location using the `ignore_file` input:

```yaml
steps:
  - name: Optim Guard
    uses: chris-rutkowski/optim-guard@v1.0.0
      with:
        ignore_file: ./my/path/my_optim_guard.ignore
```

---

## 🔍 How It Works

1. The action scans for added or modified image files in a pull request.
2. It processes the images, optimizing them using:
   - **SVG**: [SVGO](https://github.com/svg/svgo)
   - **PNG**: [pngquant](https://pngquant.org/)
   - **JPG/JPEG**: [jpegoptim](https://github.com/tjko/jpegoptim)
   - **WebP**: [cwebp](https://developers.google.com/speed/webp)
   - **GIF**: [gifsicle](https://www.lcdf.org/gifsicle/)
3. PDF files are converted to SVG using [pdf2svg](https://github.com/dawbarton/pdf2svg) and optimized with [SVGO](https://github.com/svg/svgo).
4. If unoptimized images are found, the PR is blocked, and a downloadable artefact (`optim_guard_result`) is uploaded with the optimized images for developers to review and replace as necessary.

**Note:**  
The optimization process only performs **lossless optimization**. This ensures no degradation in image quality while reducing file sizes. However, already optimized images may still be reprocessed if their size can be further reduced. Developers are encouraged to use their judgment to optimize images to an acceptable quality level before committing them, especially when balancing quality and file size.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
