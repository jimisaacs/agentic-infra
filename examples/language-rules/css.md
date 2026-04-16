# CSS Conventions (Example)

> This is an example language-specific rule. Copy to `.genai/rules/css.md` and customize for your project.
> Add a corresponding `.cursor/rules/css.mdc` wrapper with `globs: ["**/*.css"]`.

## Spacing

- Flex/grid parent → use `gap` on the parent.
- No outer margins on leaf components — parent owns spacing.
- All spacing values use design tokens. Never hardcode `px`, `rem`, or `em`.

## Layout

- Single row/column → `display: flex` + `gap`.
- Two-dimensional → `display: grid`.
- Auto-wrapping → `flex-wrap: wrap` + `gap`.

## Design Tokens

All CSS custom properties use your project's token prefix. Never hardcode colors or spacing.

- Surfaces: `--prefix-surface-bg`, `--prefix-surface-elevated`
- Text: `--prefix-text-primary`, `--prefix-text-secondary`
- Spacing: `--prefix-spacing-*`
- Radii: `--prefix-radius-*`

## Accessibility

- Every interactive element has `:focus-visible`.
- Every animation has `prefers-reduced-motion: reduce`.
- Hover states visible in both light and dark mode.

## Anti-Patterns

- No inline `style={}` for layout, spacing, font-size, or color.
- No hardcoded hex colors — use tokens.
- No `filter: brightness()` for hover states — use `color-mix()`.
