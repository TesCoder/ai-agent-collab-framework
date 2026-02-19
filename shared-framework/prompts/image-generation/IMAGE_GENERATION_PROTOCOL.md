# Image generation protocol (shared)

Use this protocol when generating images for any project.

## Goals

- Keep assets consistent with the project’s brand/voice.
- Track which images were selected and where they’re used.
- Avoid sensitive or proprietary content.

## Rules

1) **No sensitive data**
- Do not include secrets, PHI, private customer data, or NDA materials in prompts or generated assets.

2) **Prefer repeatable prompts**
- Save final “approved” prompts in the project under:
  - `projects/<project-slug>/shared-framework/prompts/image-generation/`

3) **Log selected assets**
- For each selected image, append a row to:
  - `projects/<project-slug>/reports/assets/image-generation/manifest.csv`
- Minimum columns: generation_date, original_filename, final_filename, page_or_section, alt_text, notes

4) **Folder convention (recommended)**
- `selected/`: approved assets
- `unused/`: discarded iterations

## Template prompt (starter)

```text
Subject:
Composition:
Style:
Color palette:
Lighting:
Constraints (no text / no logos / etc):
Output size:
Background:
```
