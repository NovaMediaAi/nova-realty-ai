# Nova Realty AI — USA Rebrand Design Spec

**Date:** 2026-06-16  
**Scope:** Full rebrand of ListaPro → Nova Realty AI, USA market only (50 states + Puerto Rico)

---

## 1. Branding & Visual Identity

### Name
`ListaPro` → `Nova Realty AI` everywhere: UI titles, PDF, video, emails, template editor.

### Color Palette

| Token | Old Value | New Value |
|-------|-----------|-----------|
| `color_primary` | `#1a365d` | `#0A1628` (Navy) |
| `color_accent` | `#e53e3e` | `#C9A84C` (Gold) |
| `color_background` (video) | `#0f2137` | `#0A1628` |
| `color_accent` (video) | `#c9a84c` | `#C9A84C` (unchanged) |
| `color_cta` (video) | `#c8102e` | `#C9A84C` |

All defaults in `template_settings.py` (`DEFAULT_SETTINGS`) updated to Navy/Gold values.

### Logo Placeholder
- Text `NRA` in serif font, Gold `#C9A84C` on Navy background
- Used in: PDF header, Instagram/story/carousel footer, Remotion Opening + ContactCTA scenes, email footer
- User can replace via `/plantilla` by uploading real logo — no code change needed

### Suno Music Default
```
"elegant ambient piano cinematic luxury American real estate premium"
```

---

## 2. Market Data (`config.py`)

### Geography
- Remove: all 10 LATAM country entries
- Add: 50 US states + Puerto Rico as `STATES` dict
- Each entry: `{"name": "California", "abbreviation": "CA"}`
- Currency: USD only — `format_price()` simplified to `$1,250,000` format (no currency key needed)

### Address Fields
| Old Field | New Field |
|-----------|-----------|
| `ciudad` | `city` |
| `pais` (country dropdown) | `state` (state dropdown) |
| — | `zip_code` (new, optional text) |
| — | `mls_number` (new, optional text) |

### Property Types
```python
PROPERTY_TYPES = [
    "Single Family Home", "Condo/Apartment", "Townhouse",
    "Multi-Family", "Land/Lot", "Commercial", "Office Space",
    "Warehouse/Industrial", "Penthouse", "Studio"
]
```

### Operations
```python
OPERATIONS = ["For Sale", "For Rent", "Short-Term Rental"]
```

### Amenities
```python
AMENITIES = [
    "Garage", "Swimming Pool", "Backyard/Yard", "Deck/Patio",
    "Gym/Fitness Center", "24/7 Security", "Elevator", "In-unit Laundry",
    "HOA", "Basement", "Rooftop", "Pet Friendly", "Furnished",
    "Central A/C", "Fireplace", "Smart Home"
]
```

---

## 3. Form UI + Templates

### `templates/form.html`
- App title + navbar: "Nova Realty AI", Navy/Gold colors
- `País` dropdown → `State` dropdown (50 states + PR)
- Add `ZIP Code` field (optional text input)
- Add `MLS #` field (optional text input)
- Language toggle in header: `EN | ES` — sets `idioma` hidden field
- Field labels bilingual: show English when EN, Spanish when ES
  - Examples: Bedrooms/Recámaras, Bathrooms/Baños, Price/Precio, Sq Ft/m²

### `templates/results.html`
- Branding updated to Nova Realty AI, Navy/Gold
- Labels follow selected language

### `templates/template_editor.html`
- Title updated
- NRA logo placeholder shown in preview if no logo uploaded

### `templates/historial.html`
- `País` column → `State`
- Navy/Gold colors

### `templates/script_review.html`
- Branding updated

---

## 4. AI Generator (`ai_generator.py`)

- System prompt updated to US real estate context
- When `idioma="en"`: generate copy in English, use US terminology
  - sq ft (not m²), HOA, MLS, price per sqft, neighborhoods
- When `idioma="es"`: generate in Spanish but with USA market context (city/state refs, USD prices)
- `MLS #` and `ZIP Code` included in property context passed to OpenAI if present
- `m2_construidos` passed as `sq_ft` label in English outputs

---

## 5. Label System (`labels.py`)

Central bilingual string store — all generators import from here.

- Update `LABELS` dict: add new property types, new operations, new fields
- `m2_construidos` / `m2_construidos_full` → English value becomes `"Sq Ft"` / `"Square Feet"`
- `m2_terreno_full` → English: `"Lot Size (sq ft)"`
- Add keys: `"mls_number"` (`MLS # / MLS #`), `"zip_code"` (`ZIP Code / Código ZIP`), `"state"` (`State / Estado`)
- Update operation keys: `"Venta"→"For Sale"`, `"Renta"→"For Rent"`, `"Renta Temporal"→"Short-Term Rental"` for en labels
- Add new property type entries for all USA types

---

## 6. PDF Generator (`pdf_generator.py`)

- Default colors → Navy `#0A1628`, Gold `#C9A84C`
- NRA logo: rendered as styled text block (serif, Gold on Navy) when no logo file uploaded
- Field labels bilingual based on `lang` param
- MLS # shown in header/info section if present
- ZIP Code shown alongside City/State in address line
- `pais_nombre` → `state_name` in data passed to generator

---

## 6. Image Generators (Instagram/Story/Carousel)

**Files:** `instagram_generator.py`, `story_generator.py`, `carousel_generator.py`

- Default `color_overrides`: Navy/Gold
- Footer text: "Nova Realty AI" (replacing "ListaPro")
- NRA logo placeholder rendered via Pillow text when no branding logo provided
- Property stats labels: bilingual (Beds/Recámaras, Baths/Baños, Sq Ft/m²)

---

## 7. Video / Remotion (`video_generator.py` + `video/src/`)

### Python side
- Props passed to Remotion updated with new color defaults
- `video_colors` defaults: `color_background=#0A1628`, `color_accent=#C9A84C`, `color_cta=#C9A84C`

### Remotion side (`video/src/`)
- `video/src/lib/constants.ts`: update default color constants
- `Opening.tsx`: "Nova Realty AI" branding text + NRA monogram
- `ContactCTA.tsx`: "Nova Realty AI" footer text
- Stats labels: bilingual based on `lang` prop passed via `props.json`

---

## 8. Email Generator (`email_generator.py`)

- Footer: "Nova Realty AI" branding, Navy/Gold colors
- Subject line copy updated for US market
- Bilingual: English body when `lang="en"`, Spanish when `lang="es"`
- MLS # included in listing details section if present

---

## Files Changed Summary

| File | Change Type |
|------|-------------|
| `config.py` | Replace LATAM countries with US states, update property types/operations/amenities, simplify `format_price()` |
| `labels.py` | Add new property types (Single Family Home, etc.), update operations (For Sale/For Rent/Short-Term Rental), add MLS/ZIP/State labels, update `m2_construidos` → `sq_ft` label in English |
| `template_settings.py` | Update `DEFAULT_SETTINGS` colors |
| `pdf_generator.py` | Colors, NRA logo, bilingual labels, MLS/ZIP fields |
| `instagram_generator.py` | Colors, NRA logo, bilingual labels |
| `story_generator.py` | Colors, NRA logo, bilingual labels |
| `carousel_generator.py` | Colors, NRA logo, bilingual labels |
| `email_generator.py` | Branding, bilingual, MLS field |
| `ai_generator.py` | USA market prompts, bilingual, MLS/ZIP context |
| `video_generator.py` | Color defaults |
| `main.py` | Pass `zip_code`, `mls_number` through form → property_data |
| `templates/form.html` | State dropdown, ZIP/MLS fields, language toggle, Navy/Gold |
| `templates/results.html` | Branding update |
| `templates/historial.html` | State column, branding |
| `templates/template_editor.html` | Branding update |
| `templates/script_review.html` | Branding update |
| `video/src/lib/constants.ts` | Color constants |
| `video/src/scenes/Opening.tsx` | NRA branding |
| `video/src/scenes/ContactCTA.tsx` | NRA branding |
