# Nova Realty AI — USA Rebrand Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand ListaPro → Nova Realty AI, adapt all market data for USA + Puerto Rico (USD, 50 states, US property types), add MLS # and ZIP fields, update colors to Navy #0A1628 / Gold #C9A84C throughout.

**Architecture:** Full replacement approach — swap LATAM country data with US states, update all color defaults in Python generators and Remotion, update bilingual labels for US terminology, wire new ZIP/MLS fields through form → AI → PDF/images.

**Tech Stack:** Python 3 (FastAPI, Pillow, FPDF2), Jinja2 templates, TypeScript/React (Remotion), OpenAI API

---

## Task 1: Market Data Foundation (`config.py` + `template_settings.py`)

**Files:**
- Modify: `config.py`
- Modify: `template_settings.py`

- [ ] **Step 1: Replace COUNTRIES dict with US STATES in `config.py`**

Replace the entire content of `config.py` with:

```python
import os
from pathlib import Path

# Load .env file if present
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().strip().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")
SUNO_API_KEY = os.getenv("SUNO_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
UPLOADPOST_API_KEY = os.getenv("UPLOADPOST_API_KEY", "")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
STORAGE_MODE = os.getenv("STORAGE_MODE", "local")  # "local" or "supabase"

STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico",
}

PROPERTY_TYPES = [
    "Single Family Home",
    "Condo/Apartment",
    "Townhouse",
    "Multi-Family",
    "Land/Lot",
    "Commercial",
    "Office Space",
    "Warehouse/Industrial",
    "Penthouse",
    "Studio",
]

OPERATIONS = ["For Sale", "For Rent", "Short-Term Rental"]

AMENITIES = [
    "Garage",
    "Swimming Pool",
    "Backyard/Yard",
    "Deck/Patio",
    "Gym/Fitness Center",
    "24/7 Security",
    "Elevator",
    "In-unit Laundry",
    "HOA",
    "Basement",
    "Rooftop",
    "Pet Friendly",
    "Furnished",
    "Central A/C",
    "Fireplace",
    "Smart Home",
]


def format_price(price: float, state_key: str = "") -> str:
    """Format price in USD."""
    return f"${price:,.0f} USD"
```

- [ ] **Step 2: Update DEFAULT_SETTINGS colors in `template_settings.py`**

Change lines 12–33 in `template_settings.py`:

```python
DEFAULT_SETTINGS = {
    "pdf": {
        "color_primary": "#0A1628",
        "color_accent": "#C9A84C",
        "pdf_template": "clasico",
    },
    "video": {
        "color_background": "#0A1628",
        "color_accent": "#C9A84C",
        "color_cta": "#C9A84C",
        "video_style": "elegante",
    },
    "music": {
        "style": "elegant ambient piano cinematic luxury American real estate premium",
        "negative_tags": "vocals, singing, heavy metal, aggressive, loud",
    },
    "branding": {
        "logo_path": "",
        "agent_photo_path": "",
        "qr_enabled": False,
        "qr_url": "",
    },
}
```

- [ ] **Step 3: Verify config loads correctly**

```bash
cd "/Users/angellooez/Desktop/Nova Realty AI v2"
source .venv/bin/activate
python -c "from config import STATES, PROPERTY_TYPES, OPERATIONS, AMENITIES, format_price; print(len(STATES), 'states'); print(format_price(850000))"
```

Expected output:
```
51 states
$850,000 USD
```

- [ ] **Step 4: Commit**

```bash
git add config.py template_settings.py
git commit -m "feat: replace LATAM countries with US states + PR, update default colors to Navy/Gold"
```

---

## Task 2: Bilingual Label System (`labels.py`)

**Files:**
- Modify: `labels.py`

- [ ] **Step 1: Replace LABELS dict content in `labels.py`**

Replace the `LABELS` dict and helper functions with:

```python
"""
Bilingual label system for Nova Realty AI.
Centralizes all translatable strings for image generators, PDF, and carousel.
"""

LABELS = {
    # Stats (short labels for images)
    "recamaras": {"es": "Rec.", "en": "Bed."},
    "banos": {"es": "Baños", "en": "Bath."},
    "m2_construidos": {"es": "m²", "en": "Sq Ft"},
    "estacionamientos": {"es": "Estac.", "en": "Parking"},

    # Stats (full labels for PDF)
    "recamaras_full": {"es": "Recámaras", "en": "Bedrooms"},
    "banos_full": {"es": "Baños", "en": "Bathrooms"},
    "m2_construidos_full": {"es": "m² Construidos", "en": "Square Feet"},
    "m2_terreno_full": {"es": "m² Terreno", "en": "Lot Size (sq ft)"},
    "estacionamientos_full": {"es": "Estacionamientos", "en": "Parking Spots"},
    "pisos_full": {"es": "Pisos", "en": "Floors"},
    "direccion": {"es": "Dirección", "en": "Address"},
    "pisos_niveles": {"es": "Pisos / Niveles", "en": "Floors / Levels"},
    "superficie_construida": {"es": "Superficie construida", "en": "Square footage"},
    "superficie_terreno": {"es": "Superficie terreno", "en": "Lot size"},

    # New USA fields
    "mls_number": {"es": "MLS #", "en": "MLS #"},
    "zip_code": {"es": "Código ZIP", "en": "ZIP Code"},
    "state": {"es": "Estado", "en": "State"},

    # Operations (uppercase badges)
    "For Sale": {"es": "EN VENTA", "en": "FOR SALE"},
    "For Rent": {"es": "EN RENTA", "en": "FOR RENT"},
    "Short-Term Rental": {"es": "RENTA TEMPORAL", "en": "SHORT-TERM RENTAL"},

    # Operations (lowercase for headings)
    "for_sale_lower": {"es": "en venta", "en": "for sale"},
    "for_rent_lower": {"es": "en renta", "en": "for rent"},
    "short_term_lower": {"es": "renta temporal", "en": "short-term rental"},

    # Property types (US)
    "Single Family Home": {"es": "Casa Unifamiliar", "en": "Single Family Home"},
    "Condo/Apartment": {"es": "Condominio/Apartamento", "en": "Condo/Apartment"},
    "Townhouse": {"es": "Townhouse", "en": "Townhouse"},
    "Multi-Family": {"es": "Multi-Familiar", "en": "Multi-Family"},
    "Land/Lot": {"es": "Terreno/Lote", "en": "Land/Lot"},
    "Commercial": {"es": "Comercial", "en": "Commercial"},
    "Office Space": {"es": "Oficina", "en": "Office Space"},
    "Warehouse/Industrial": {"es": "Bodega/Industrial", "en": "Warehouse/Industrial"},
    "Penthouse": {"es": "Penthouse", "en": "Penthouse"},
    "Studio": {"es": "Estudio", "en": "Studio"},

    # PDF section headers
    "amenidades": {"es": "Amenidades", "en": "Amenities"},
    "galeria": {"es": "Galería de Fotos", "en": "Photo Gallery"},
    "especificaciones": {"es": "Especificaciones", "en": "Specifications"},
    "descripcion": {"es": "Descripción", "en": "Description"},

    # PDF spec labels
    "tipo_propiedad": {"es": "Tipo de propiedad", "en": "Property type"},
    "operacion_label": {"es": "Operación", "en": "Operation"},
    "precio_label": {"es": "Precio", "en": "Price"},
    "ubicacion": {"es": "Ubicación", "en": "Location"},

    # Carousel text
    "slide_contact_title": {"es": "Agenda tu visita", "en": "Schedule a visit"},
    "slide_stats_title": {"es": "Características", "en": "Features"},
    "contacto": {"es": "Contacto", "en": "Contact"},

    # Video CTA
    "video_cta": {"es": "Agenda tu visita", "en": "Schedule a Tour"},
    "video_scan": {"es": "ESCANEA PARA MÁS INFO", "en": "SCAN FOR MORE INFO"},
    "video_watermark": {"es": "NOVA REALTY AI", "en": "NOVA REALTY AI"},

    # Heading pattern: "{tipo} {connector} {operacion}"
    "heading_en": {"es": "en", "en": "for"},
}


def get_label(key: str, lang: str = "es") -> str:
    """Get a label in the specified language. Falls back to key itself."""
    entry = LABELS.get(key)
    if entry:
        return entry.get(lang, entry.get("es", key))
    return key


def get_operation(operation: str, lang: str = "es", uppercase: bool = True) -> str:
    """Translate operation. uppercase=True for badges, False for headings."""
    if uppercase:
        return get_label(operation, lang)
    lower_map = {
        "For Sale": "for_sale_lower",
        "For Rent": "for_rent_lower",
        "Short-Term Rental": "short_term_lower",
    }
    key = lower_map.get(operation, operation)
    return get_label(key, lang)


def get_property_type(tipo: str, lang: str = "es") -> str:
    """Translate property type."""
    return get_label(tipo, lang)
```

- [ ] **Step 2: Verify labels load**

```bash
python -c "from labels import get_label, get_operation, get_property_type; print(get_operation('For Sale','en')); print(get_property_type('Single Family Home','es')); print(get_label('m2_construidos','en'))"
```

Expected:
```
FOR SALE
Casa Unifamiliar
Sq Ft
```

- [ ] **Step 3: Commit**

```bash
git add labels.py
git commit -m "feat: update bilingual labels for US market (property types, operations, new MLS/ZIP/state fields)"
```

---

## Task 3: Image Helpers Default Colors (`image_helpers.py`)

**Files:**
- Modify: `image_helpers.py`

- [ ] **Step 1: Update `parse_colors()` defaults**

In `image_helpers.py`, change lines 136–143 (`parse_colors` function):

```python
def parse_colors(color_overrides: dict = None) -> tuple:
    """Parse color overrides, return (primary, accent) RGB tuples."""
    primary = (10, 22, 40)    # #0A1628 Navy
    accent = (201, 168, 76)   # #C9A84C Gold
    if color_overrides:
        if "color_primary" in color_overrides:
            primary = hex_to_rgb(color_overrides["color_primary"])
        if "color_accent" in color_overrides:
            accent = hex_to_rgb(color_overrides["color_accent"])
    return primary, accent
```

- [ ] **Step 2: Update `extract_stats()` to use `sq ft` suffix in English**

In `image_helpers.py`, replace the `extract_stats` function (lines 117–132):

```python
def extract_stats(data: dict, lang: str = "es") -> list:
    """Extract stats as (value, label, icon_key) tuples with language support."""
    stats = []
    rec = str(data.get("recamaras", "0") or "0")
    if rec != "0":
        stats.append((rec, get_label("recamaras", lang), "recamaras"))
    ban = str(data.get("banos", "0") or "0")
    if ban != "0":
        stats.append((ban, get_label("banos", lang), "banos"))
    m2 = str(data.get("m2_construidos", "") or "")
    if m2 and m2 != "0":
        suffix = " sq ft" if lang == "en" else "m²"
        stats.append((f"{m2}{suffix}", get_label("m2_construidos", lang), "m2_construidos"))
    est = str(data.get("estacionamientos", "0") or "0")
    if est != "0":
        stats.append((est, get_label("estacionamientos", lang), "estacionamientos"))
    return stats
```

- [ ] **Step 3: Check image generators for hardcoded "ListaPro" text and update**

```bash
grep -n "ListaPro\|LISTAPRO\|listapro" instagram_generator.py story_generator.py carousel_generator.py
```

For each occurrence found, replace with `Nova Realty AI` / `NOVA REALTY AI`.

- [ ] **Step 2: Verify**

```bash
python -c "from image_helpers import parse_colors; p, a = parse_colors(); print(p, a)"
```

Expected:
```
(10, 22, 40) (201, 168, 76)
```

- [ ] **Step 3: Commit**

```bash
git add image_helpers.py
git commit -m "feat: update image helper default colors to Nova Realty AI Navy/Gold"
```

---

## Task 4: Form Handler — New Fields (`main.py`)

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Add `zip_code` and `mls_number` to `generar_listado` signature**

In `main.py`, in the `generar_listado` function signature (around line 302), add after `otras_amenidades`:

```python
    zip_code: str = Form(""),
    mls_number: str = Form(""),
```

- [ ] **Step 2: Add new fields to `property_data` dict**

In the same function, in the `property_data` dict (around line 337), add:

```python
        "zip_code": zip_code,
        "mls_number": mls_number,
        "state": pais,  # pais field now carries state abbreviation
```

- [ ] **Step 3: Update `ai_generator` import in `main.py`**

In `main.py` line 14, change:

```python
from config import COUNTRIES, PROPERTY_TYPES, OPERATIONS, AMENITIES, format_price, SUNO_API_KEY
```

to:

```python
from config import STATES, PROPERTY_TYPES, OPERATIONS, AMENITIES, format_price, SUNO_API_KEY
```

- [ ] **Step 4: Update all `COUNTRIES` references in `main.py` to `STATES`**

`main.py` uses `COUNTRIES` in the form route and historial. Replace all occurrences:

- Line ~259 in `show_form`: change `"countries": COUNTRIES` → `"states": STATES`
- Line ~189 in `historial`: change `country_key = pd.get("pais", "mexico")` → `state_key = pd.get("pais", "")` and `country = COUNTRIES.get(country_key, COUNTRIES["mexico"])` → `state_name = STATES.get(state_key, state_key)`
- In `historial` listings dict: change `"pais_nombre": country["name"]` → `"pais_nombre": state_name`
- In `generar_listado` (around line 428): replace country lookup:

```python
        state_key = pais  # pais field = state abbreviation (e.g. "FL")
        state_name = STATES.get(state_key, state_key)
        precio_fmt = format_price(precio)
```

and update all `country["name"]` → `state_name`, `format_price(precio, pais)` → `format_price(precio)` throughout the function.

- [ ] **Step 5: Verify server starts without error**

```bash
source .venv/bin/activate && python -c "import main; print('OK')"
```

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add main.py
git commit -m "feat: add zip_code and mls_number form fields, switch from COUNTRIES to STATES in main.py"
```

---

## Task 5: AI Generator — USA Prompts (`ai_generator.py`)

**Files:**
- Modify: `ai_generator.py`

- [ ] **Step 1: Replace `ai_generator.py` content**

Replace entire file:

```python
import json
from openai import OpenAI
from config import OPENAI_API_KEY, STATES, format_price


def generate_listing_copy(property_data: dict) -> dict:
    """Generate real estate listing copy using OpenAI API."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    state_key = property_data.get("pais", "")
    state_name = STATES.get(state_key, state_key)
    precio = float(property_data.get("precio", 0))
    precio_fmt = format_price(precio)
    lang = property_data.get("idioma", "es")

    amenidades = property_data.get("amenidades", [])
    if isinstance(amenidades, str):
        amenidades = [amenidades]
    otras = property_data.get("otras_amenidades", "")
    if otras:
        amenidades.extend([a.strip() for a in otras.split(",") if a.strip()])
    amenidades_str = ", ".join(amenidades) if amenidades else ("Not specified" if lang == "en" else "No especificadas")

    mls = property_data.get("mls_number", "")
    zip_code = property_data.get("zip_code", "")
    city = property_data.get("ciudad", "")
    location = f"{city}, {state_name}" + (f" {zip_code}" if zip_code else "")

    if lang == "en":
        system_prompt = """You are a professional real estate copywriter specializing in the US market. Create attractive, professional listing copy in English.

RULES:
- Use US real estate vocabulary: sq ft (not m²), bedrooms/bathrooms, HOA, MLS, price per sq ft
- All prices in USD
- Professional yet approachable tone
- Highlight the most attractive features
- Do NOT invent data not provided
- ALL content in English

Respond ONLY with valid JSON (no markdown, no backticks) with these 5 keys:

1. "descripcion_pdf": Professional 2-3 paragraph description for a real estate brochure. Elegant and descriptive. Mention location, main features, notable amenities.

2. "copy_instagram": Instagram/Facebook post in English. Include relevant emojis (don't overdo it), hashtags at the end (5-8 including the city and state), and a call to action. Max 250 words.

3. "mensaje_whatsapp": Short WhatsApp message (3-4 lines max) in English. Include price, location, one attractive feature. Minimal emojis. Direct and engaging.

4. "frase_gancho": Short impactful phrase (max 8 words) capturing the property essence. Examples: "Your dream home awaits", "Luxury living redefined", "Where elegance meets comfort". NO emojis. Emotional and aspirational.

5. "copy_email": Professional email body for a property blast. Write a compelling subject line as the FIRST line (prefix "Subject: "), blank line, then 3-4 short paragraphs: opening hook, key features, call to action. Professional but warm. NO HTML tags. NO agent name/phone."""

        user_message = f"""PROPERTY DATA:
- Type: {property_data.get('tipo_propiedad', 'Not specified')}
- Operation: {property_data.get('operacion', 'For Sale')}
- Price: {precio_fmt}
- Location: {location}
- Address: {property_data.get('direccion', 'Not published')}
- MLS #: {mls if mls else 'N/A'}
- Bedrooms: {property_data.get('recamaras', 'Not specified')}
- Bathrooms: {property_data.get('banos', 'Not specified')}
- Square Feet: {property_data.get('m2_construidos', 'Not specified')} sq ft
- Lot Size: {property_data.get('m2_terreno', 'Not specified')} sq ft
- Parking: {property_data.get('estacionamientos', 'Not specified')}
- Floors: {property_data.get('pisos', 'Not specified')}
- Amenities: {amenidades_str}
- Additional notes: {property_data.get('notas', 'None')}
- Agent: {property_data.get('agente_nombre', '')}
- Phone: {property_data.get('agente_telefono', '')}"""

    else:
        system_prompt = """Eres un copywriter profesional de bienes raíces especializado en el mercado de Estados Unidos. Crea textos atractivos y profesionales para listados de propiedades en inglés y español.

REGLAS:
- Usa vocabulario inmobiliario apropiado para el mercado de USA
- Los precios se expresan en USD
- Sé formal pero accesible
- Destaca las características más atractivas
- NO inventes datos que no estén en la información proporcionada
- Contenido en español, pero con referencias geográficas de USA (ciudad, estado)

Responde ÚNICAMENTE con un JSON válido (sin markdown, sin backticks) con estas 5 claves:

1. "descripcion_pdf": Descripción profesional de 2-3 párrafos para un folleto inmobiliario. Tono elegante. Menciona ubicación, características principales y amenidades.

2. "copy_instagram": Post para Instagram/Facebook. Emojis relevantes (sin exagerar), hashtags al final (5-8 incluyendo ciudad y estado), llamado a la acción. Máximo 250 palabras.

3. "mensaje_whatsapp": Mensaje corto para WhatsApp (3-4 líneas). Incluye precio, ubicación, dato atractivo. Emojis mínimos. Directo.

4. "frase_gancho": Frase corta e impactante (máximo 8 palabras). Ejemplos: "Tu hogar soñado te espera", "Lujo y confort en cada detalle". Sin emojis. Emotiva y aspiracional.

5. "copy_email": Email profesional para blast inmobiliario. Asunto atractivo en la PRIMERA línea (prefijo "Asunto: "), línea en blanco, después 3-4 párrafos cortos. Sin etiquetas HTML. Sin nombre/teléfono del agente."""

        user_message = f"""DATOS DE LA PROPIEDAD:
- Tipo: {property_data.get('tipo_propiedad', 'No especificado')}
- Operación: {property_data.get('operacion', 'For Sale')}
- Precio: {precio_fmt}
- Ubicación: {location}
- Dirección: {property_data.get('direccion', 'No publicada')}
- MLS #: {mls if mls else 'N/A'}
- Recámaras: {property_data.get('recamaras', 'No especificado')}
- Baños: {property_data.get('banos', 'No especificado')}
- Superficie: {property_data.get('m2_construidos', 'No especificado')} sq ft
- Terreno: {property_data.get('m2_terreno', 'No especificado')} sq ft
- Estacionamientos: {property_data.get('estacionamientos', 'No especificado')}
- Pisos: {property_data.get('pisos', 'No especificado')}
- Amenidades: {amenidades_str}
- Notas adicionales: {property_data.get('notas', 'Ninguna')}
- Agente: {property_data.get('agente_nombre', '')}
- Teléfono: {property_data.get('agente_telefono', '')}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=2500,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        if "```" in raw:
            json_str = raw.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
            result = json.loads(json_str.strip())
        else:
            result = {
                "descripcion_pdf": raw,
                "copy_instagram": "Error generating social media copy." if lang == "en" else "Error al generar el copy para redes sociales.",
                "mensaje_whatsapp": "Error generating WhatsApp message." if lang == "en" else "Error al generar el mensaje de WhatsApp.",
            }

    return result
```

- [ ] **Step 2: Verify import**

```bash
python -c "from ai_generator import generate_listing_copy; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add ai_generator.py
git commit -m "feat: update AI generator for US market prompts, bilingual, MLS/ZIP/state context"
```

---

## Task 6: PDF Generator Colors + MLS/ZIP (`pdf_generator.py`)

**Files:**
- Modify: `pdf_generator.py`

- [ ] **Step 1: Update hardcoded colors in `ListaProPDF.__init__`**

In `pdf_generator.py`, change the color assignments in `ListaProPDF.__init__` (lines 35–43):

```python
        # Colors — Nova Realty AI Navy/Gold
        self.PRIMARY = (10, 22, 40)        # #0A1628 Navy
        self.ACCENT = (201, 168, 76)       # #C9A84C Gold
        self.TEXT_DARK = (45, 55, 72)      # #2d3748
        self.TEXT_LIGHT = (113, 128, 150)  # #718096
        self.BG_LIGHT = (247, 250, 252)    # #f7fafc
        self.BORDER = (226, 232, 240)      # #e2e8f0
        self.WHITE = (255, 255, 255)
        self.STAT_BG = (10, 22, 40)        # #0A1628 Navy
```

- [ ] **Step 2: Replace "ListaPro" watermark text in `pdf_generator.py`**

Lines 212 and 215 both say `"Generado con ListaPro"`. Replace both with `"Nova Realty AI"`:

```python
pdf.cell(55, 4, "Nova Realty AI", align="R")
```

- [ ] **Step 3: Update the three location strings to include ZIP Code**

Lines 257–259, 471–473, and 540–542 all contain this pattern:
```python
    ciudad = property_data.get("ciudad", "")
    pais_nombre = property_data.get("pais_nombre", "")
    location = f"{ciudad}, {pais_nombre}" if pais_nombre else ciudad
```

Replace all three occurrences with:
```python
    ciudad = property_data.get("ciudad", "")
    pais_nombre = property_data.get("pais_nombre", "")
    zip_code = property_data.get("zip_code", "")
    location = f"{ciudad}, {pais_nombre}" if pais_nombre else ciudad
    if zip_code:
        location = f"{location} {zip_code}"
```

- [ ] **Step 3: Verify PDF generator imports without error**

```bash
python -c "from pdf_generator import generate_pdf; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add pdf_generator.py
git commit -m "feat: update PDF generator colors to Navy/Gold, add MLS # and ZIP display"
```

---

## Task 7: Email Generator — Branding + USA Amenities (`email_generator.py`)

**Files:**
- Modify: `email_generator.py`

- [ ] **Step 1: Update `AMENITY_EMOJIS` dict with USA amenities**

Replace the `AMENITY_EMOJIS` dict at the top of `email_generator.py`:

```python
AMENITY_EMOJIS = {
    "Garage": "🚗", "Swimming Pool": "🏊", "Backyard/Yard": "🌿",
    "Deck/Patio": "🌅", "Gym/Fitness Center": "🏋️", "24/7 Security": "🔒",
    "Elevator": "🛗", "In-unit Laundry": "🧺", "HOA": "🏘️",
    "Basement": "⬇️", "Rooftop": "🌇", "Pet Friendly": "🐾",
    "Furnished": "🛋️", "Central A/C": "❄️", "Fireplace": "🔥",
    "Smart Home": "🏠",
}
```

- [ ] **Step 2: Find "ListaPro" / "LISTAPRO" in `email_generator.py` and replace with "Nova Realty AI"**

```bash
grep -n "ListaPro\|LISTAPRO\|listapro" email_generator.py
```

Replace every occurrence with `Nova Realty AI` (or `NOVA REALTY AI` where uppercase is used).

- [ ] **Step 3: Update `_op_badge` mapping to use new operation names**

Replace the `_op_badge` function:

```python
def _op_badge(operacion: str, lang: str = "es") -> str:
    op_map = {
        "For Sale": "en_venta",
        "For Rent": "en_renta",
        "Short-Term Rental": "en_renta_temporal",
    }
    return _el(op_map.get(operacion, "en_venta"), lang)
```

And update `_EMAIL_LABELS` operation keys:

```python
    "en_venta": {"es": "En Venta", "en": "For Sale"},
    "en_renta": {"es": "En Renta", "en": "For Rent"},
    "en_renta_temporal": {"es": "Renta Temporal", "en": "Short-Term Rental"},
```

- [ ] **Step 4: Update subject fallback to use state instead of country**

In `generate_email_html`, find the fallback subject line:
```python
    if not subject:
        prep = "in" if lang == "en" else "en"
        subject = f"{tipo_translated} {prep} {ciudad} · {precio_fmt}"
```
This stays the same — `ciudad` will now hold city name. No change needed.

- [ ] **Step 5: Verify email generator imports**

```bash
python -c "from email_generator import generate_email_html; print('OK')"
```

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add email_generator.py
git commit -m "feat: update email generator branding to Nova Realty AI, USA amenity emojis, new operation names"
```

---

## Task 8: Form Template (`templates/form.html`)

**Files:**
- Modify: `templates/form.html`

- [ ] **Step 1: Update page title and header logo**

Find and replace:
```html
<title>ListaPro - Genera Listados Inmobiliarios Profesionales</title>
```
→
```html
<title>Nova Realty AI - Professional Listing Generator</title>
```

Find the header logo:
```html
<h1>Lista<span>Pro</span></h1>
```
→
```html
<h1>Nova Realty <span>AI</span></h1>
```

- [ ] **Step 2: Replace País dropdown with State dropdown**

Find the country select block (lines 83–92):
```html
<div class="form-group">
    <label>País <span class="required">*</span></label>
    <select name="pais" id="countrySelect" required>
        {% for key, country in countries.items() %}
        <option value="{{ key }}" data-symbol="{{ country.symbol }}" data-currency="{{ country.currency }}">
            {{ country.name }}
        </option>
        {% endfor %}
    </select>
</div>
```

Replace with:
```html
<div class="form-group">
    <label>State <span class="required">*</span></label>
    <select name="pais" id="stateSelect" required>
        <option value="">Select state...</option>
        {% for abbr, name in states.items() %}
        <option value="{{ abbr }}">{{ name }}</option>
        {% endfor %}
    </select>
</div>
```

- [ ] **Step 3: Add ZIP Code and MLS # fields**

After the city/address fields in Step 1 of the wizard, add:
```html
<div class="form-group">
    <label>ZIP Code</label>
    <input type="text" name="zip_code" placeholder="e.g. 33139" maxlength="10">
</div>
<div class="form-group">
    <label>MLS #</label>
    <input type="text" name="mls_number" placeholder="Optional MLS number">
</div>
```

- [ ] **Step 4: Update currency badge — simplify to USD-only**

Find the JavaScript that updates `currencyBadge` based on country selection, or just find the badge element:
```html
<span class="currency-badge" id="currencyBadge">$ MXN</span>
```
→
```html
<span class="currency-badge" id="currencyBadge">$ USD</span>
```

Remove any JS that was updating the currency badge dynamically based on country, or replace it with a no-op.

- [ ] **Step 5: Update Step 1 hero text**

```html
<h2>Datos de la Propiedad</h2>
<p class="step-subtitle">Tipo, ubicación y operación</p>
```
→
```html
<h2>Property Details</h2>
<p class="step-subtitle">Type, location, and operation</p>
```

Update `<div class="step-number">Paso 01</div>` → `<div class="step-number">Step 01</div>` (and all other step numbers).

- [ ] **Step 6: Update `show_form` route in `main.py` to pass `states` instead of `countries`**

In `main.py`, find the `show_form` route (around line 257):
```python
    return templates.TemplateResponse("form.html", {
        "request": request,
        "countries": COUNTRIES,
        "property_types": PROPERTY_TYPES,
        "operations": OPERATIONS,
        "amenities": AMENITIES,
        "error": error,
    })
```
Change `"countries": COUNTRIES` → `"states": STATES` (already done in Task 4, verify it's there).

Also fix the `generar_listado` error return (2 occurrences) that also passes `countries`:
```python
        return templates.TemplateResponse("form.html", {
            "request": request,
            "states": STATES,   # was "countries": COUNTRIES
            "property_types": PROPERTY_TYPES,
            "operations": OPERATIONS,
            "amenities": AMENITIES,
            "error": f"...",
        })
```

- [ ] **Step 7: Start server and verify form renders**

```bash
source .venv/bin/activate && python main.py &
sleep 2 && curl -s http://localhost:8000 | grep -i "Nova Realty\|state\|MLS"
```

Expected: lines containing "Nova Realty AI", "State", "MLS"

Kill server: `pkill -f "python main.py"`

- [ ] **Step 8: Commit**

```bash
git add templates/form.html main.py
git commit -m "feat: update form template to Nova Realty AI branding, US state dropdown, ZIP and MLS fields"
```

---

## Task 9: Other Templates Branding

**Files:**
- Modify: `templates/results.html`
- Modify: `templates/historial.html`
- Modify: `templates/template_editor.html`
- Modify: `templates/script_review.html`

- [ ] **Step 1: Replace "ListaPro" with "Nova Realty AI" in all templates**

```bash
grep -rn "ListaPro\|LISTAPRO" templates/
```

For each occurrence, replace with `Nova Realty AI` (or `NOVA REALTY AI` in uppercase contexts).

Run for each file:
```bash
sed -i '' 's/Lista<span>Pro<\/span>/Nova Realty <span>AI<\/span>/g' templates/results.html templates/historial.html templates/template_editor.html templates/script_review.html
sed -i '' 's/ListaPro/Nova Realty AI/g' templates/results.html templates/historial.html templates/template_editor.html templates/script_review.html
sed -i '' 's/<title>ListaPro/<title>Nova Realty AI/g' templates/results.html templates/historial.html templates/template_editor.html templates/script_review.html
```

- [ ] **Step 2: Replace "País" with "State" in `historial.html` table headers**

```bash
grep -n "País\|pais" templates/historial.html
```

Replace the `País` column header → `State` and `pais_nombre` display stays the same (it already holds state name).

- [ ] **Step 3: Verify no "ListaPro" remains in templates**

```bash
grep -rn "ListaPro" templates/
```

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add templates/
git commit -m "feat: rebrand all templates to Nova Realty AI, update Estado/State labels"
```

---

## Task 10: Remotion Color Defaults (`video/src/lib/constants.ts`)

**Files:**
- Modify: `video/src/lib/constants.ts`

- [ ] **Step 1: Update `elegante` preset colors**

In `video/src/lib/constants.ts`, change the `elegante` entry in `STYLE_PRESETS`:

```typescript
  elegante: {
    bgColor: "#0A1628",
    bgSecondary: "#1a2d4a",
    accentColor: "#C9A84C",
    ctaColor: "#C9A84C",
    textColor: "#ffffff",
    textLight: "rgba(255,255,255,0.7)",
    fontHeading: "'Playfair Display', Georgia, serif",
    fontBody: "'DM Sans', 'Helvetica Neue', sans-serif",
    animSpeed: 1,
  },
```

- [ ] **Step 2: Build Remotion to verify no TS errors**

```bash
cd "/Users/angellooez/Desktop/Nova Realty AI v2/video"
npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add video/src/lib/constants.ts
git commit -m "feat: update Remotion elegante preset to Navy/Gold color scheme"
```

---

## Task 11: Remotion Branding (`video/src/scenes/ContactCTA.tsx`)

**Files:**
- Modify: `video/src/scenes/ContactCTA.tsx`

- [ ] **Step 1: Add `lang` prop to `ContactCTAProps` and component**

In `ContactCTA.tsx`, update the type and component to accept `lang`:

```typescript
type ContactCTAProps = {
  agenteNombre: string;
  agenteTelefono: string;
  agenciaNombre: string;
  logoUrl?: string;
  agentPhotoUrl?: string;
  qrUrl?: string;
  bgPhotoUrl?: string;
  style: StylePreset;
  lang?: string;
};

export const ContactCTA: React.FC<ContactCTAProps> = ({
  agenteNombre,
  agenteTelefono,
  agenciaNombre,
  logoUrl,
  agentPhotoUrl,
  qrUrl,
  bgPhotoUrl,
  style: s,
  lang = "en",
}) => {
```

- [ ] **Step 2: Update hardcoded Spanish strings in `ContactCTA.tsx`**

Find the CTA text element (around line 214):
```tsx
      >
        Agenda tu visita
      </div>
```
Replace with:
```tsx
      >
        {lang === "en" ? "Schedule a Tour" : "Agenda tu visita"}
      </div>
```

Find the QR scan label (around line 317):
```tsx
            >
              ESCANEA PARA MÁS INFO
            </div>
```
Replace with:
```tsx
            >
              {lang === "en" ? "SCAN FOR MORE INFO" : "ESCANEA PARA MÁS INFO"}
            </div>
```

Find the watermark (around line 354):
```tsx
      >
        LISTAPRO
      </div>
```
Replace with:
```tsx
      >
        NOVA REALTY AI
      </div>
```

- [ ] **Step 3: Update `ListingReel.tsx` to pass `lang` prop to `ContactCTA`**

```bash
grep -n "ContactCTA\|lang" "/Users/angellooez/Desktop/Nova Realty AI v2/video/src/ListingReel.tsx"
```

Find where `<ContactCTA` is rendered in `ListingReel.tsx` and add `lang={lang}` prop. Also ensure `lang` is part of the props type in `ListingReel.tsx`. Check that `props.json` (written by Python) includes a `lang` field — update `video_generator.py` if needed.

- [ ] **Step 4: Update `video_generator.py` to include `lang` in Remotion props**

In `video_generator.py`, find where `props.json` is built and ensure `lang` from `property_data` is included:

```bash
grep -n "props\|lang" "/Users/angellooez/Desktop/Nova Realty AI v2/video_generator.py" | head -30
```

Find the dict written to `props.json` and add:
```python
"lang": property_data.get("idioma", "en"),
```

- [ ] **Step 5: Build Remotion to verify no TS errors**

```bash
cd "/Users/angellooez/Desktop/Nova Realty AI v2/video"
npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add video/src/scenes/ContactCTA.tsx video/src/ video_generator.py
git commit -m "feat: update Remotion ContactCTA to Nova Realty AI watermark, bilingual CTA text, lang prop"
```

---

## Task 12: End-to-End Verification

- [ ] **Step 1: Start the server**

```bash
cd "/Users/angellooez/Desktop/Nova Realty AI v2"
source .venv/bin/activate
python main.py
```

- [ ] **Step 2: Verify form at http://localhost:8000**

Check:
- Header shows "Nova Realty AI"
- State dropdown shows US states (not LATAM countries)
- ZIP Code field present
- MLS # field present
- Currency shows "$ USD" (not "$ MXN")
- Property types show "Single Family Home", "Condo/Apartment", etc.
- Operations show "For Sale", "For Rent", "Short-Term Rental"
- Amenities show "Garage", "Swimming Pool", etc.

- [ ] **Step 3: Verify template editor at http://localhost:8000/plantilla**

Check:
- Header shows "Nova Realty AI"
- Color pickers default to Navy/Gold

- [ ] **Step 4: Submit a test listing (no OpenAI key needed for structure check)**

Fill form with: Single Family Home, For Sale, CA, Miami, $500000, 3 bed, 2 bath, 1500 sq ft.
Expected: redirects to `/resultado/<job_id>`, PDF generates, Instagram image generates.

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat: complete Nova Realty AI USA rebrand — Navy/Gold, US states, bilingual, MLS/ZIP, Remotion branding"
```
