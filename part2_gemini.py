from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from texts import CORPUS, LANGUAGES

load_dotenv()

OUTPUT_PATH = Path(__file__).with_name("measurements.json")
DEFAULT_MODEL = "gemini-2.5-flash"


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")
    return genai.Client(api_key=api_key)


def count_tokens(client: genai.Client, model_id: str, text: str) -> int:
    """Return the number of input tokens ``text`` costs on Gemini."""
    result = client.models.count_tokens(
        model=model_id,
        contents=text,
    )
    return result.total_tokens


def count_request_tokens(client: genai.Client, model_id: str, lang: str) -> int:
    """Return input tokens for one real request: system prompt + complaint."""
    combined = CORPUS["system_prompt"][lang] + "\n\n" + CORPUS["complaint"][lang]
    result = client.models.count_tokens(
        model=model_id,
        contents=combined,
    )
    return result.total_tokens

def one_real_request(
    client: genai.Client, model_id: str, lang: str
) -> Optional[Dict[str, int]]:
    """Send one request and print the answer and its billed usage."""
    config = types.GenerateContentConfig(
        system_instruction=CORPUS["system_prompt"][lang]
    )
    
    response = client.models.generate_content(
        model=model_id,
        contents=CORPUS["complaint"][lang],
        config=config,
    )

    if hasattr(response, "text") and response.text:
        print("  --- answer ---")
        print("  " + response.text.replace("\n", "\n  "))

    usage = response.usage_metadata
    print(f"  billed: {usage.prompt_token_count} in, {usage.candidates_token_count} out")
    
    return {
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Part 2 Measurement using Gemini API")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"which model to price against (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--call",
        action="store_true",
        help="also answer the complaint in each language",
    )
    args = parser.parse_args()

    try:
        client = get_client()
    except Exception as exc:
        print(f"Could not build Gemini client: {exc}", file=sys.stderr)
        return 1

    counts: Dict[str, Dict[str, int]] = {}
    print(f"Counting tokens on Gemini model '{args.model}' (free, no model run)...")
    
    try:
        for item_id, versions in CORPUS.items():
            counts[item_id] = {
                lang: count_tokens(client, args.model, versions[lang])
                for lang in LANGUAGES
            }
            row = "  ".join(f"{lang}={counts[item_id][lang]}" for lang in LANGUAGES)
            print(f"  {item_id:<14} {row}")

        request_tokens: Dict[str, int] = {
            lang: count_request_tokens(client, args.model, lang) for lang in LANGUAGES
        }
        row = "  ".join(f"{lang}={request_tokens[lang]}" for lang in LANGUAGES)
        print(f"  {'request':<14} {row}  (system + complaint, one call)")
    except Exception as exc:
        print(f"Error while counting tokens: {exc}", file=sys.stderr)
        return 1

    billed: Dict[str, Dict[str, int]] = {}
    if args.call:
        print(f"\nAnswering complaint on {args.model} in each language:")
        for lang in LANGUAGES:
            print(f"\n[{lang}]")
            try:
                result = one_real_request(client, args.model, lang)
                if result is not None:
                    billed[lang] = result
            except Exception as exc:
                print(f"API Error on [{lang}]: {exc}", file=sys.stderr)
                return 1

    payload = {
        "model": args.model,
        "model_id": args.model,
        "token_counts": counts,
        "request_tokens": request_tokens,
        "one_request_billed": billed or None,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {OUTPUT_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())