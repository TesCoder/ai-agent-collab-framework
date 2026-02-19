# Troubleshooting

## Node “command not found” (macOS/Homebrew)

If `node` is missing on a new machine and you installed `node@18` via Homebrew, add it to your PATH:

```bash
export PATH="/usr/local/opt/node@18/bin:$PATH"
source ~/.zshrc
node -v
```

If you’re on Apple Silicon and Homebrew lives under `/opt/homebrew`, use:

```bash
export PATH="/opt/homebrew/opt/node@18/bin:$PATH"
source ~/.zshrc
node -v
```

## Broken links inside the repo

- Prefer relative links that resolve inside this repository.
- If a doc references a path that doesn’t exist, either:
  - update the reference to the correct file, or
  - add a minimal placeholder under `docs/` / `shared-tools/` / `projects/_template/` so the repo remains self-contained.
