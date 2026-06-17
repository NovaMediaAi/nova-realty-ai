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
