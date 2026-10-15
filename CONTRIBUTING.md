# Contributing

## Formatting

All files are formatted with [Prettier](https://prettier.io), and a CI check
enforces it on every push and pull request.

Run the same pinned version CI uses (see
[`.github/workflows/prettier.yml`](.github/workflows/prettier.yml)):

```sh
# check formatting (same as CI)
npx prettier@3.9.1 --check .

# auto-fix
npx prettier@3.9.1 --write .
```
