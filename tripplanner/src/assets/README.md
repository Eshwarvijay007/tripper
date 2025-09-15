Frontend assets
================

Use this folder to store static assets that are imported in components.

Structure
- images/: General images used in the UI
- logos/: Brand and partner logos

Usage (Vite + React)
- Import directly in components to get hashed, optimized URLs at build time.

Example:
  import heroImg from '@/assets/images/hero.jpg';
  import brandLogo from '@/assets/logos/brand.svg';

  <img src={heroImg} alt="Hero" />
  <img src={brandLogo} alt="Brand" />

Notes
- For truly static files that should be served as-is at the root (no hashing), prefer the `public/` folder.
- Aliases: `@` resolves to `src/` (Vite default in many setups). If not configured, use relative paths like `../assets/images/...`.

