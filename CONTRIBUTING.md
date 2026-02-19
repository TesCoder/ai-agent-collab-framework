# Contributing

Thanks for helping improve this repo.

## What to contribute

- Fix broken references/links in docs
- Improve clarity of prompts and guardrails (keep changes minimal and explicit)
- Add examples (Work Packets, evidence bundles, merge/approval patterns)
- Add small, dependency-free tooling that supports the workflow (linting, validation)

## Repo conventions

- Prefer **additive** changes over large rewrites.
- Keep paths and links **self-contained** within the repo.
- Avoid project-specific identifiers in published artifacts (use placeholders like `<project-slug>`).

## Before opening a PR

- Ensure the demo packet still lints:

```bash
python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md
```

- If you add new docs, make sure README links still resolve on GitHub.

## License

By contributing, you agree that your contributions will be licensed under the terms in `LICENSE`.
