# Action Network wrapper — template + generator

Branding for **Action Network (AN) custom page wrappers**: the frame (colours,
fonts, logo, layout, footer, share buttons) that wraps an AN action — petition,
form, sign-up or donation page.

Two things live here:

1. **`wrapper.html`** — the self-contained wrapper template you paste into AN.
2. **`generator.html`** — a single-file, no-build web tool that themes
   `wrapper.html` with simple form controls, so non-coders never touch the code.

## Live links

| What | URL |
|------|-----|
| Public tool (Webflow page) | https://www.solidaritystudio.uk/tools/action-network-wrapper |
| Tool hosted directly (GitHub Pages) | https://jbrindle18.github.io/action-network-wrappers/generator.html |
| Repo | https://github.com/jbrindle18/action-network-wrappers |

The Webflow page embeds the GitHub Pages URL in an `<iframe>` (see
`webflow-embed.html`). Editing the repo + pushing to `main` updates both,
because GitHub Pages serves `main` and Webflow just frames it.

## Files

| File | What it is |
|------|------------|
| `wrapper.html` | **The deliverable and the single source of truth.** A self-contained AN page wrapper — all CSS is inline in `<style id="anw-embed-css">`, all JS is inline; the only asset you upload is the logo. Section 0 holds the theme tokens. |
| `generator.html` | The themeing tool. **Bakes a copy of `wrapper.html` into itself as base64** (`<script id="masterB64">`) and decodes it on boot — no network fetch. Renders a form from the tokens, rebuilds a themed wrapper, and offers Copy Header / Copy Footer / Save / Import. |
| `rebake.py` | Refreshes the base64 copy of `wrapper.html` inside `generator.html`. **Run after every `wrapper.html` edit** (see below). |
| `webflow-embed.html` | The `<iframe>` + auto-resize snippet to paste into a Webflow Embed element. |
| `Centrul Filia Wrapper.html` | A real themed wrapper (Centrul Filia), kept as a worked example. |
| `previews/` | Static, sanitized snapshots of AN's own widget markup (currently just `petition.html`), fetched by `generator.html`'s live preview pane and restyled in place as you edit. Not baked in — the tool fetches these at runtime, same as it fetches AN's own base whitelabel CSS. |
| `README.md` | This file. |

## How it works — whitelabel base + brand layer

The action widget is embedded with `?format=js&style=full&css=whitelabel`, so AN
ships only a minimal **structural** stylesheet (field layout, spacing). The
inline `<style>` block in `wrapper.html` paints the brand over that neutral
skeleton — few `!important`s, predictable base. All CSS is scoped under
`.an-homepage-embed` so nothing leaks into other embeds.

`generator.html` parses Section 0's `--token: value;` declarations into form
fields, plus a handful of config anchors (logo, fonts, layout, modules, share),
and rebuilds the wrapper via targeted string replacement. The encoding round-trip
is UTF-8-safe (handles £, em-dashes, etc.).

## Using the tool (the normal, no-code workflow)

1. Open the tool. Work through the sections — colours, fonts, logo, layout,
   footer, share options.
2. **Copy Header** → paste into the **Header** box of your AN page wrapper.
   **Copy Footer** → paste into the **Footer** box.
   (In AN: Start Organizing → your group → Page wrappers → new/edit wrapper.)
3. Save in AN; set your action to use that wrapper.
4. **Save Wrapper** keeps a `wrapper.html` file. Next time, **Import Saved
   Wrapper** reads its settings (colours, fonts, logo, layout, modules, share,
   footer) and applies them onto the **latest** template — so you keep every
   later fix/feature instead of resurrecting the old file. Renamed tokens are
   migrated automatically (e.g. an old single brand colour fans out to the new
   button / progress-bar / heading colours).

Always check the result in AN's own page-wrapper **Preview** before going live.

## ⚠️ Re-baking — the one maintenance rule

`generator.html` does **not** load `wrapper.html` at runtime; it carries a
**base64 copy baked inside it**. So if you edit `wrapper.html`, the hosted tool
keeps serving the OLD wrapper until you re-bake:

```bash
python rebake.py          # refresh the baked-in copy
python rebake.py --check  # exit 1 if stale (handy for CI / pre-commit)
```

Then commit **both** `wrapper.html` and `generator.html` together. If you ever
see the tool produce stale output, an un-baked `wrapper.html` edit is the first
thing to check.

## Live preview — a second maintenance note

The generator's preview pane renders a real, **static** capture of AN's own
widget markup (`previews/petition.html`), not a live AN embed. If Action
Network changes the structure of that widget (new field, new class, new
wrapper div), the preview can drift out of sync with reality even though
`wrapper.html` itself still works correctly against the real thing. If the
preview looks wrong: re-capture a fresh embed (format=js&source=widget&style=full,
with `style-embed-whitelabel-v3.css` linked, no custom wrapper), strip the
single-use CSRF/anti-bot tokens and `<script>` tags, add `onsubmit="return
false"` to the form, and replace `previews/petition.html`. This has no effect
on Copy Header/Footer/Save/Import — those never touch the preview fixture.

## Editing `wrapper.html` by hand (advanced)

Everything tweakable is searchable by the keyword **`CONFIG`**.

### Colours
Edit **Section 0 (THEME TOKENS)** at the top of `<style id="anw-embed-css">`.
Default palette is green. The colour system is deliberately small — 10 tokens
cover the whole theme:

| Token | Controls |
|-------|----------|
| `--body` | Body text **and** headings |
| `--accent` | Entry-title heading, progress bar + running total, links, required-field mark, input focus outline |
| `--button-bg` | Action / submit button background |
| `--button-text` | Action / submit button text |
| `--input-border` | Input field border |
| `--page-bg` | Page background |
| `--card-bg` | The form's own card ("Form colour") |
| `--header-bg` | Header bar background |
| `--footer-bg` | Footer background |
| `--footer-text` | Footer text |

Everything else (button hover, divider lines, the form card's border, the
quote-box accent bar and background, loading skeleton, shadow, placeholder
and helper-text grey) is declared in **Section 0b (DERIVED / STANDARD)**
right below Section 0 — either computed from the 10 tokens above via CSS
`color-mix()` (e.g. the divider is a lighter tint of `--accent`) or a fixed
brand-neutral value. Section 0b is a deliberately separate `.an-homepage-embed
{ }` rule: the generator tool only parses the *first* such rule for editable
fields, so anything in Section 0b stays out of the UI on purpose — it's not
meant to be set directly.

### Fonts
Set the families in `--font-body` / `--font-heading`, then load them one of two
ways:

- **Google Fonts** — update the `<link>` in the head (CONFIG: FONTS) and
  `ANW.fontUrl` to match; request only the weights you use. (In the tool: the
  "Google Fonts URL" box in the Fonts section.)
- **Self-hosted / non-Google fonts (incl. multiple)** — add `@font-face` rules in
  the **CONFIG: FONT-FACE** block (just below Section 0). One `@font-face` per
  weight; paste several blocks for several families; then point the `--font-*`
  tokens at the family names. Because the whole `<style>` block is also injected
  into AN's donation iframe, these fonts load there too — no `<link>` needed.
  Clear the Google Fonts URL when you use this (the tool/​generator then drops the
  Google `<link>` automatically). Example:

  ```css
  @font-face{font-family:"Aktiv Grotesk";src:url("https://YOURHOST/aktiv-400.woff2") format("woff2");font-weight:400;font-display:swap}
  @font-face{font-family:"Aktiv Grotesk";src:url("https://YOURHOST/aktiv-700.woff2") format("woff2");font-weight:700;font-display:swap}
  ```

### Logo
CONFIG: LOGO — set the `<img>` `src` + `alt` and the home link. The logo is the
**only** asset you upload — put it in AN `user_files` and use its absolute URL.
Size is controlled by `--logo-max-height` / `--logo-max-width`.

> No CSS upload / cache-bust: styles are inline, so there's no external
> stylesheet to upload and no `?v=N` to bump.

### Modules (`window.ANW`)
Toggles live in the `window.ANW` block (CONFIG: MODULES):

```js
window.ANW = {
  recurringPretick: false,        // pre-tick "Make This Recurring Monthly"
  hideFundraiserSidebar: false,   // hide the donation iframe's right sidebar
  shareButtons: true,             // share buttons on the thank-you page
  shareLabel: "Share this with your network",
  fontUrl: "https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;700&display=swap"
};
```

- **Loader fade** *(always on)* — fades out the loading skeleton once AN's form
  or donation iframe has rendered.
- **Fundraiser iframe injection** *(always on)* — the donation widget renders in
  a same-origin iframe whose document AN replaces after its widget JS loads. This
  module copies the inline CSS + font `<link>` into that iframe and tags its
  `<body>` so the brand styles apply inside it too. It re-injects on `load`, on a
  ~30s poll, and via a MutationObserver; the sweep is idempotent.
- **Recurring pre-tick** *(toggle)* — pre-ticks "Make This Recurring Monthly".
  ⚠️ May be disallowed by some orgs / payment processors — ships OFF.
- **Share buttons** *(toggle, default ON)* — appends share buttons to the
  thank-you page (`#can_thank_you`), watched via MutationObserver. Shares the AN
  action URL. Fundraiser thank-yous live in AN's own iframe and aren't covered.

### Layout
Pick a class on `.gen_wrapper` (CONFIG: LAYOUT):

| Class | Description col | Form col | Use for |
|-------|-----------------|----------|---------|
| `layout--equal` | 56% | 40% | Default — petitions/forms |
| `layout--reverse` | 30% | 65% | Long letters / big forms |
| `layout--full` | 100% | 100% | Single column |

## Deploying to Action Network

1. Upload the **logo** to AN **user_files**; copy its URL into the wrapper
   (CONFIG: LOGO) — or set it in the tool.
2. Theme the tokens + font `<link>` (or use the tool).
3. In AN, create/edit the page-wrapper template and paste the Header + Footer
   (the tool splits them at `<!-- END TEMPLATE HEADER - START WIDGET -->`).
4. Ensure the widget embed uses `css=whitelabel`.

## Hosting the tool

`generator.html` is a static file served from GitHub Pages (`main` branch,
root). To update: edit, **re-bake if `wrapper.html` changed**, commit, push.
Pages rebuilds in ~1–2 min. The Webflow page frames it via `webflow-embed.html`;
the iframe auto-grows to the tool's height via `postMessage`. The section
sidebar shows in the embed when the container is ≥ 860px wide and folds away
below that.

## Notes / gotchas

- **Cross-origin embed:** the tool (github.io) inside the Webflow page is
  cross-origin, so sidebar section links open + highlight a section but can't
  scroll the parent page to it. True click-to-scroll would need a small
  `postMessage` handshake.
- **Fundraiser pages:** Stripe owns the card fields, so those keep processor
  styling; the card *around* the iframe is styled by the wrapper.
- **`.action_letter` (the "letter to target" box) has a hidden decorative
  element:** AN renders a `::before` pseudo-element on it — a 12px grey
  "folded corner" strip — completely independent of the `border` property. If
  you accent that box's border (e.g. a coloured `border-left`), this strip
  still shows and reads as a second, conflicting border. Hide it explicitly:
  `.action_letter::before { display: none !important; }`.
- **SVG logo renders as 0×0:** if you size a logo `<img>` with only
  `max-height` (no `max-width`, no explicit `height`) and the source SVG has
  no `width`/`height` attributes (only a `viewBox`), some renderers can't
  resolve `width: auto` against it and the image collapses to nothing. Set an
  explicit `height` (not `max-height`) when sizing a lone image this way — the
  header logo already does this safely via `max-height` **+** `max-width`
  together, which doesn't hit the bug.
- This template descends from the Reunite Families UK build (which used a CSS
  *override* approach rather than whitelabel); that code is reference only.
