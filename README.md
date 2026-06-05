# Action Network wrapper — reusable template

A starting point for branding Action Network (AN) custom page wrappers across
client projects. Built on AN's **whitelabel** CSS base (layout styles only),
with a thin, fully tokenised brand layer on top.

## Files

| File            | What it is                                                              |
|-----------------|-------------------------------------------------------------------------|
| `wrapper.html`  | **The deliverable, and the single source.** A self-contained AN page wrapper — all styles are inline in the `<style id="anw-embed-css">` block and all JS is inline too, so there's nothing to upload but the logo. Edit this file directly; paste the whole thing into the AN wrapper template. |
| `README.md`     | This file.                                                              |

> There is no separate `.css` file or local preview harness any more — the
> wrapper HTML is everything. To check styling, use AN's own page-wrapper
> **Preview** (Groups → page wrappers → Preview).

## Approach: whitelabel base + brand layer

The widget is embedded with `?format=js&style=full&css=whitelabel`, so AN ships
only a minimal **structural** stylesheet (field layout, spacing). The inline
`<style>` block in `wrapper.html` paints the brand over that neutral skeleton.
This means few `!important`s and a predictable base — as opposed to overriding
AN's full default styles.

## Per-client setup (the 3 things you usually change)

Everything is searchable in `wrapper.html` by the keyword **`CONFIG`**.

### 1. Colours + Fonts
Edit **Section 0 (THEME TOKENS)** at the top of the `<style id="anw-embed-css">`
block in `wrapper.html` — brand colour, text, card, inputs, statement box,
footer, radii, etc. Then update the Google Fonts `<link>` (CONFIG: FONTS) to
match `--font-body` / `--font-heading`. Request only the weights you use.

### 2. Logo
In `wrapper.html` (CONFIG: LOGO) set the `<img>` `src` + `alt` and the home
link. The logo is the **only** asset you upload — put it in AN `user_files` and
use its absolute URL. Size is controlled by `--logo-max-height` /
`--logo-max-width` tokens.

> **No CSS upload / cache-bust.** Because the styles are inline in
> `wrapper.html`, there's no external stylesheet to upload and no `?v=N` to bump.
> The styles apply directly to the markup AN injects into the page.

## JavaScript / modules

`wrapper.html` carries a small amount of JS. Toggles live in the
**`window.ANW`** block near the top of `wrapper.html` (CONFIG: MODULES):

```js
window.ANW = {
  recurringPretick: false,        // pre-tick "Make This Recurring Monthly"
  hideFundraiserSidebar: false,   // hide the donation iframe's right sidebar
  shareButtons: true,             // WhatsApp+Facebook buttons on the thank-you page
  shareLabel: "Share this with your network",  // prompt text above the buttons
  fontUrl: "https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;700&display=swap"
};
```

- **Loader fade** *(always on)* — fades out the loading skeleton once AN's form
  (inline page) or donation iframe (fundraiser) has rendered.
- **Fundraiser iframe injection** *(always on)* — the donation widget renders in
  a same-origin iframe whose document AN replaces after its widget JS loads. This
  module copies the inline `<style id="anw-embed-css">` text and the font `<link>`
  into that iframe, and tags its `<body>` with `an-homepage-embed` (plus
  `an-hide-sidebar` when `hideFundraiserSidebar` is true), so the brand styles
  apply inside the iframe too. Because AN swaps the iframe document after its
  widget JS runs (wiping our styles), it sweeps **every** same-origin iframe —
  covering both fundraiser and ticketed-event widgets — re-injecting on the
  `load` event, on a ~30s poll, and via a MutationObserver. The sweep is
  idempotent, so re-runs are cheap.
- **Recurring pre-tick** *(toggle — `recurringPretick`)* — pre-ticks "Make This
  Recurring Monthly" on fundraiser pages by ticking the checkbox in the
  same-origin iframe.

  ⚠️ Pre-ticking recurring donations may be disallowed by some orgs / payment
  processors — ship OFF, enable only with the client's sign-off.
- **Share buttons** *(toggle — `shareButtons`, default ON)* — appends WhatsApp +
  Facebook share buttons to the thank-you page. AN injects the thank-you view
  (`#can_thank_you`) after submission, so the module watches for that node with a
  MutationObserver and adds the buttons once. Shares `window.location.href` (the
  AN action URL). Prompt text is set by `shareLabel`. Petition / form / letter
  thank-yous render inline; fundraiser thank-yous live in AN's own iframe and are
  not covered.

## Layout

Pick a class on `.gen_wrapper` in `wrapper.html` (CONFIG: LAYOUT):

| Class             | Description col | Form col | Use for                     |
|-------------------|-----------------|----------|-----------------------------|
| `layout--equal`   | 56%             | 40%      | Default — petitions/forms.  |
| `layout--reverse` | 30%             | 65%      | Long letters / big forms.   |
| `layout--full`    | 100%            | 100%     | Single column.              |

## Deploying

1. Upload the **logo** to AN **user_files**; copy its URL into `wrapper.html`
   (CONFIG: LOGO).
2. Theme the tokens in the `<style>` block (CONFIG: COLOURS+FONTS) and font
   `<link>`.
3. In AN, create/edit the page-wrapper template and paste the **whole**
   `wrapper.html`. AN injects the action widget at the
   `<!-- END TEMPLATE HEADER - START WIDGET -->` marker.
4. Ensure the widget embed uses `css=whitelabel` (see Approach above).

To update styling later: edit the `<style id="anw-embed-css">` block (or the
inline JS) in `wrapper.html`, re-paste the whole file into the AN page-wrapper
template, and check it in AN's **Preview**.

## Notes / gotchas

- **Fundraiser pages:** the donation widget renders inside a same-origin iframe
  whose document AN **replaces** after its widget JS runs. The injection module
  (see above) re-reads `contentDocument` and re-injects the brand CSS + font on
  the iframe's `load` event so the inside of the iframe matches the wrapper.
  Stripe owns the actual card fields, so those keep their processor styling. The
  card *around* the iframe is styled by the wrapper either way.
- All CSS is scoped under `.an-homepage-embed` so nothing leaks into host-site
  embeds.
- This template descends from the Reunite Families UK build (which used the
  override approach). The RFUK code under
  `…/Reunite Families/Code/` is kept only as reference.
