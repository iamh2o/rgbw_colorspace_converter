Javascript-based webapp to control show running.

## Get started

Install the dependencies...

```bash
npm install
```

...then start [Rollup](https://rollupjs.org):

```bash
npm run dev
```

Navigate to [localhost:5000](http://localhost:5000). You should see your app running. Edit a component file in `src`, save it, and the page will reload.

## Building

To build the app, which will later be served by python:

```bash
npm run build
```

## About

[Svelte](https://svelte.dev/) is the framework used, which is a lot simpler than React + libraries. Pretty much everything needed to know about Svelte is in the short [tutorial](https://svelte.dev/tutorial/basics).

[TailwindCSS](https://tailwindcss.com/) is used to make shorter work of styling. Styling is straightforward by adding class attributes. For example, to get a black background and white text:

```html
<div class="bg-black text-white"></div>
```

TailwindCSS doesn't have any good solution for making sliders useful. It also doesn't give us a dialog modal. A couple components from [Svelte Material UI](https://sveltematerialui.com/) are pulled in for these. This requires a file for theming (just colors) at `src/theme/_smui-theme.scss`.
