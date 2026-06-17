# Nova Realty AI

AI-powered real estate marketing platform. Fill out one form → get a full marketing package in under 2 minutes: professional PDF brochure, Instagram post/story/carousel, email HTML, voiceover MP3, and an MP4 video reel.

## Quick Install (with Claude Code)

Open Claude Code and paste this prompt — it handles everything automatically:

```
Clone the repository https://github.com/NovaMediaAi/nova-realty-ai.git, install all Python dependencies (in a .venv virtual environment) and Node.js dependencies (in the video/ folder), and create the .env file from .env.example. When done, guide me step by step to configure each API key, explaining what each one is for and how to get it. Then start the server automatically.
```

## Manual Install

```bash
# 1. Clone
git clone https://github.com/NovaMediaAi/nova-realty-ai.git
cd nova-realty-ai

# 2. Python env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Node (Remotion video)
cd video && npm install && cd ..

# 4. Environment
cp .env.example .env
# Edit .env and add your API keys

# 5. Start
python main.py
```

Open **http://localhost:8000** and start generating listings.

## API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `OPENAI_API_KEY` | **Yes** | All AI copy generation |
| `ELEVENLABS_API_KEY` | Optional | Voiceover + background music |
| `IMGBB_API_KEY` | Optional | Photo hosting for Remotion video |
| `UPLOADPOST_API_KEY` | Optional | Direct Instagram publishing |
| `SUPABASE_URL` / `SUPABASE_KEY` | Optional | Cloud storage (default: local disk) |

Without optional keys: PDF, Instagram post/story/carousel, and email work perfectly. Only video + Instagram publishing need the extras.

## What gets generated

For each listing submission:

- `nova_<id>.pdf` — Professional PDF brochure (classic or modern template)
- `instagram_<id>.png` — Square Instagram post
- `story_<id>.png` — Vertical story
- `carousel/` — Multi-slide carousel + ZIP
- `email_<id>.html` — Inline-CSS email ready to send
- `voiceover.mp3` — ElevenLabs narration (if key provided)
- `nova_<id>.mp4` — Remotion-rendered video reel (background job)

## Features

- **Bilingual** — EN/ES toggle in the form header
- **US market** — 50 states + Puerto Rico, USD pricing, MLS # and ZIP Code fields
- **Brand settings** — Upload logo, agent photo, set colors at `/plantilla`
- **Direct Instagram publish** — Post, story, carousel via Upload Post API
- **Video types** — Quick reel or narrated tour with scene-synced voiceover

## Architecture

See [CLAUDE.md](CLAUDE.md) for full architecture documentation.

## Contact

hello@nova-media.ai
