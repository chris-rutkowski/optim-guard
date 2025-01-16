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

### 1. Add the GitHub Action
Create a GitHub Actions workflow in `.github/workflows/optim_guard.yml`:

```yaml
name: Optim Guard
on:
  pull_request:
    branches:
      - main

jobs:
  optim_guard:
    runs-on: ubuntu-latest
    steps:
      - name: Optim Guard
        uses: chris-rutkowski/optim-guard@v2.0.0
```

---

### 2. Create an ignore file (optional)
Add a `optim_guard.ignore` file to the root of your repository to define patterns for files or directories to exclude from optimization. The syntax follows `.gitignore` conventions.

**Note**: This action processes only **JP(E)G, SVG, PDF, WebP, and PNG** files. You don't need to exclude source code directories or other irrelevant files. Only specify the directories containing these file types that you don't want to optimise.

**Example `optim_guard.ignore`:**
```gitignore
test/snapshots/*
```

---

## 🔍 How it works?

1. The action scans for added or modified image files in a pull request.
2. It processes the images, optimizing them using:
   - **SVG**: [SVGO](https://github.com/svg/svgo)
   - **PNG**: [pngquant](https://pngquant.org/)
   - **JPG/JPEG**: [jpegoptim](https://github.com/tjko/jpegoptim)
   - **WebP**: [cwebp](https://developers.google.com/speed/webp)
   - **GIF**: [gifsicle](https://www.lcdf.org/gifsicle/)
3. PDF files are converted to SVG using [pdf2svg](https://github.com/dawbarton/pdf2svg) and optimized with [SVGO](https://github.com/svg/svgo).
4. If unoptimized images are found, the action fails, and a downloadable artefact (`optim_guard_result`) is uploaded with the optimised assets for developers to replace.

**Note:**  
The optimization process only performs **lossless optimization**. This ensures no degradation in image quality while reducing file sizes. However, already optimized images may still be reprocessed if their size can be further reduced. Developers are encouraged to use their judgment to optimize images to an acceptable quality level before committing them, especially when balancing quality and file size.

---

## ♻️ Optimise existing files

Run the action manually using the `workflow_dispatch` event to scan and optimise existing files in your repository. Trigger it against your main branch to identify and generate optimised versions of assets that you can replace in your next pull request.

```yaml
name: Optim Guard
on:
  workflow_dispatch:
  pull_request:

...
```

---

## ⚙️ Configuration

### Enable optimising PDF files

PDF files can be converted to SVG format and optimised. This functionality is disabled by default, but you can enable it. 

**Note:** Based on testing, the Xcode archiving pipeline produces smaller final results with PDFs than SVGs.

```yaml
steps:
  - name: Optim Guard
    uses: chris-rutkowski/optim-guard@v2.0.0
      with:
        process_pdfs: "true"
```

### Specify a custom ignore file path

```yaml
steps:
  - name: Optim Guard
    uses: chris-rutkowski/optim-guard@v2.0.0
      with:
        ignore_file: ./my/path/my_optim_guard.ignore
```

## 📄 License
This project is licensed under the [MIT License](LICENSE).
