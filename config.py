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
