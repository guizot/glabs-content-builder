"""
Content Builder AI Generator

Usage:
    python generate.py
    python generate.py --prompt src/inputs/prompt.txt
"""

import argparse
import sys
import os
import json
from datetime import datetime

# Ensure the project root is in the path so `src.` imports work
sys.path.insert(0, os.path.dirname(__file__))

from src.core.scraper import get_scraped_context
from src.core.llm import generate_batch_json
from src.core.builder import build_from_json

def main():
    parser = argparse.ArgumentParser(
        description="✨ AI Content Generator — Generate social media JSON and Images from a text prompt."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="src/inputs/prompt.txt",
        help="Path to the user prompt text file (default: src/inputs/prompt.txt)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs",
        help="Output directory for images (default: outputs/)",
    )

    args = parser.parse_args()

    print("=" * 50)
    print("  ✨ AI CONTENT GENERATOR v1 ✨")
    print("=" * 50)

    # 1. Read the user's text prompt
    prompt_path = args.prompt
    if not os.path.exists(prompt_path):
        print(f"❌ Prompt file not found: {prompt_path}")
        print("Please create it and write your prompt.")
        sys.exit(1)

    with open(prompt_path, "r", encoding="utf-8") as f:
        user_prompt = f.read().strip()
        
    if not user_prompt:
        print(f"❌ Prompt file is empty: {prompt_path}")
        sys.exit(1)

    print(f"  📝 Reading prompt from: {prompt_path}")
    print(f"  >> \"{user_prompt[:100]}...\"" if len(user_prompt) > 100 else f"  >> \"{user_prompt}\"")

    # 2. Scrape any context from URLs
    print("\n[Step 1] Scraping context (if any URLs are present)...")
    context = get_scraped_context(user_prompt)

    # 3. Generate JSON via LLM
    print("\n[Step 2] Translating prompt into structured Content Builder JSON...")
    batch_data = generate_batch_json(user_prompt, context)
    
    if not batch_data:
        print("❌ Generation failed. Exiting.")
        sys.exit(1)

    # 4. Save generated JSON
    timestamp_for_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_out_path = f"src/inputs/generated_{timestamp_for_file}.json"
    
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(batch_data, f, indent=4)
        
    print(f"  ✅ Saved generated JSON Payload: {json_out_path}")

    # 5. Build images from the JSON
    print("\n[Step 3] Dispatching to Content Builder Pipeline...")
    timestamp_for_folder = datetime.now().strftime("%d %B %Y %H:%M:%S")
    final_output = os.path.join(args.output, timestamp_for_folder)

    build_from_json(json_out_path, final_output)

if __name__ == "__main__":
    main()
