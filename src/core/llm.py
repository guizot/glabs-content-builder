"""
LLM Integration Service

Handles the communication with the OpenAI API to generate
the JSON schema from user prompts.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from src.config.prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)

def generate_batch_json(user_prompt: str, context: str = "", model: str = "deepseek-v3.2") -> list:
    """
    Sends the user prompt and context to the LLM and asks for the structured JSON batch.
    """
    
    # Combine user prompt and context if available
    final_prompt = user_prompt
    if context:
        final_prompt += f"\n\nAdditional Context Provided by User:\n{context}"

    print(f"  🧠 Calling LLM ({model})...")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": final_prompt},
            ],
            temperature=0.7,
        )
        
        raw_text = response.choices[0].message.content
        
        # Clean up Markdown JSON blocks if the LLM ignored instruction #1
        raw_text = raw_text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Failed to parse LLM response as JSON: {e}")
        print(f"  Raw response: {raw_text}")
        return []
    except Exception as e:
        print(f"  ❌ Failed to call LLM: {str(e)}")
        return []
