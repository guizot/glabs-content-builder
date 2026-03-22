# Glabs Content Builder

A modular AI content generation system that automatically creates Instagram posts from scheduled prompts. Deployed on Render and triggered via cron jobs.

## Features

- **Full AI Pipeline**: Prompt → Scraper (context) → LLM (structured JSON) → Canvas (image rendering)
- **JSON-only Mode**: Generate images directly from existing JSON payloads
- **Telegram Bot**: Interactive bot for manual triggering and scheduling
- **Scheduler Integration**: Cron-friendly with `/trigger?slot=HH:MM&key=...` endpoint
- **Modular Design**: Each feature (scraper, LLM, canvas, telegram, scheduler) is plug-and-play

## Project Structure

```
glabs-content-builder/
├── .gitignore
├── main.py                 # Entry point with three modes
├── requirements.txt        # Python dependencies
├── inputs/
│   ├── schedule.csv       # Scheduled prompts (triggered by cron)
│   ├── prompt.txt         # Manual prompt for full pipeline
│   └── sample_batch.json  # Sample JSON for json-only mode
├── outputs/               # Generated content (timestamped folders)
└── features/              # Modular components
    ├── scraper_feature/   # Web scraping for context
    ├── llm_feature/       # LLM JSON generation (OpenAI)
    ├── canvas_feature/    # Image rendering (Canvas API)
    ├── image_gen_feature/ # Optional image generation
    ├── telegram_feature/  # Telegram bot integration
    └── scheduler_feature/ # Cron job scheduler logic
```

## schedule.csv Format

The `inputs/schedule.csv` drives automated content creation. Columns:

| Column | Description |
|--------|-------------|
| `prompt` | Full instruction for the AI (what to create) |
| `scheduled_time` | Time in UTC when the job should trigger (e.g., `2026-03-22 08:00`) |
| `status` | Currently `pending`; set to `completed` after execution (optional) |
| `last_run` | Timestamp of last execution (auto-updated by the system) |

**Example rows:**
```csv
prompt,scheduled_time,status,last_run
create instagram post that has 1 quote using design2 quote about productivity and quote and caption is in Bahasa Indonesia,2026-03-22 08:00,pending,
"create instagram post that has 1 hook 3 content & 1 CTA using design2 content about productivity and hook, content, cta and caption is in Bahasa Indonesia",2026-03-22 12:00,pending,
```

- Newlines inside prompts must be quoted
- Times should be in UTC (cron uses system timezone; adjust accordingly)
- The system finds the row matching the requested `slot` (e.g., `08:00`) and marks it as processed

## Usage Modes

### 1. Full AI Pipeline (Prompt → Images)

```bash
python main.py --prompt inputs/prompt.txt --output outputs/
```

- Reads `prompt.txt`
- Scrapes context URLs (ScraperFeature)
- Generates structured JSON via LLM (LLMFeature)
- Renders images using Canvas (CanvasFeature)
- Saves to `outputs/<timestamp>/`

### 2. JSON-only Pipeline (Direct Rendering)

```bash
python main.py --input inputs/sample_batch.json --output outputs/
```

- Skips LLM and scraping
- Directly renders images from a valid JSON payload

### 3. Telegram Bot

```bash
python main.py --telegram
```

- Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- Provides interactive commands to trigger generation, view schedule, etc.
- Uses APScheduler for cron-like scheduling if desired

## Render Deployment

This app is designed to run on Render with a webhook endpoint:

### Environment Variables (Render)

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | Token to fetch `schedule.csv` from GitHub (optional if using local file) |
| `OPENAI_API_KEY` | OpenAI API key for LLMFeature |
| `CANVAS_API_KEY` | API key for Canvas rendering service |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (if using Telegram) |
| `TELEGRAM_CHAT_ID` | Your chat ID for Telegram notifications |
| `PORT` | Port number (Render sets automatically) |

### Trigger Webhook

The Render service should expose an endpoint:

```
GET /trigger?slot=HH:MM&key=YOUR_SECRET_KEY
```

- `slot` — scheduled time (e.g., `08:00`, `12:00`, `16:00`, `20:00`)
- `key` — secret key to authenticate the cron trigger

The handler should:
1. Authenticate the `key`
2. Find the row in `schedule.csv` where `scheduled_time` matches `slot` (date-agnostic, just time part)
3. Run the full generation pipeline using that prompt
4. Update the row's `status` to `completed` and `last_run` to current timestamp

### Cron Job Setup (on your server)

```bash
0 8,12,16,20 * * * curl -s "https://your-render-service.onrender.com/trigger?slot=HH:MM&key=YOUR_KEY" > /dev/null 2>&1
```

- Use 4 separate cron entries for 8am, 12pm, 4pm, 8pm (in your timezone)
- The `slot` parameter must match the time format in `schedule.csv` (24h, HH:MM)

## Local Development

1. **Clone and install dependencies:**
   ```bash
   git clone https://github.com/guizot/glabs-content-builder.git
   cd glabs-content-builder
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** (for local testing) with required keys:
   ```env
   OPENAI_API_KEY=sk-...
   CANVAS_API_KEY=...
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   ```

3. **Test manually:**
   ```bash
   python main.py --prompt inputs/prompt.txt
   python main.py --input inputs/sample_batch.json
   ```

## Adding New Scheduled Posts

1. Edit `inputs/schedule.csv` and add new rows with:
   - `prompt`: Your detailed instruction
   - `scheduled_time`: The UTC time slot (e.g., `2026-03-23 08:00`)
   - `status`: `pending`
   - `last_run`: leave empty

2. Commit and push to GitHub (Render will auto-redeploy if using GitHub integration)

3. The next cron trigger will pick up the new entry

## Notes

- All generated outputs are saved under `outputs/` with a timestamp folder
- The system expects `schedule.csv` to be in the `inputs/` directory
- The trigger mechanism should handle concurrency (avoid running same slot twice)
- Consider adding a lock file or database for production robustness

## License

[Add your license here]

---

**Maintained by:** Rinaldi Guizot
