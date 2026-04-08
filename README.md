# Nails & Inspiration

Telegram bot + web gallery for nail inspiration.

## How it works

There are two layers:

1. **Main design catalog**
   - fixed set of nail images inside the project
   - every design has tags
   - the Telegram bot searches here

2. **Saved collection**
   - when the user presses save, the chosen design is linked to that Telegram user
   - the website shows only saved images for that user

So the logic is:

- `/random` -> random design from the full catalog
- `/long`, `/short`, `/solid`, `/creative` -> designs from the full catalog by tag
- `/save` -> save the current design to favorites
- `/my` -> open the personal web gallery

## Where to change images and tags

### Images
Put your own images into:

```bash
app/static/images/designs/
```

### Tags, titles, and descriptions
Edit:

```bash
app/seed_data.py
```

Example:

```python
{
    "image": "designs/design_01.jpg",
    "title": "Soft french",
    "description": "Clean white French set",
    "tags": ["long", "solid"]
}
```

After you change images or tags, run:

```bash
docker compose down -v
docker compose up --build
```

## Run locally or on VM

1. Copy `.env.example` to `.env`
2. Paste your Telegram bot token into `.env`
3. Run:

```bash
docker compose up --build
```

4. Open:

```text
http://YOUR_VM_IP:8000
```


## Theme switch

The website includes two themes:
- Dark Luxe (default)
- Light Luxe

The selected theme is saved in the browser.
