import httpx
from pathlib import Path


async def generate_music(
    style: str = "elegant ambient piano cinematic luxury American real estate premium",
    negative_tags: str = "",  # ElevenLabs sound-gen doesn't use negative tags
) -> dict:
    """Generate background music via ElevenLabs Sound Effects API.

    Returns dict with status and audio_url (local path) on success.
    """
    from config import ELEVENLABS_API_KEY

    if not ELEVENLABS_API_KEY:
        return {"status": "failed", "error": "ELEVENLABS_API_KEY not set"}

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": style,
        "duration_seconds": 22.0,
        "prompt_influence": 0.4,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.elevenlabs.io/v1/sound-generation",
            headers=headers,
            json=body,
        )
        resp.raise_for_status()
        # Response is raw MP3 bytes
        return {"status": "ready", "audio_bytes": resp.content}


async def download_audio(audio_url: str, output_path: str) -> bool:
    """Download audio from URL (kept for compatibility)."""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(audio_url)
        resp.raise_for_status()
        Path(output_path).write_bytes(resp.content)
    return True
