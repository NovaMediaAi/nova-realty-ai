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
