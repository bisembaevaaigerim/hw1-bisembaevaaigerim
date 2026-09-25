"""Sublab Medium - one Kazakh-correction task, six models.

Six models, one prompt, eight sentences. What you are producing is evidence:
a table that says which models repaired which kind of damage, and what each one
charged you for the attempt.

Fill in every `TODO`. Keep the function signatures.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sublab_easy.registration_bot import (RATES_PER_MTOK,  # noqa: E402
                                          ask_once, estimate_cost)

DATA = Path(__file__).resolve().parent.parent / "data" / "kazakh_errors.json"

# Every model you must run. Keep the order - it is the order of your table.
MODELS = [
    #("openai", "gpt-5.6-luna"),
    #("openai", "gpt-5.6-terra"),
    #("openai", "gpt-5.6-sol"),
    ("openrouter", "nex-n2.5-mini:free"),
    ("openrouter", "laguna-s-2.1:free"),
    ("openrouter", "nemotron-3-ultra-550b-a55b:free"),
]

def load_sentences() -> list[dict]:
    """The eight corrupted sentences and their published originals."""
    return json.loads(DATA.read_text(encoding="utf-8"))["sentences"]


def build_prompt(corrupted: str) -> str:
    """Ask for a corrected sentence AND a list of the changes made.

    Requirements:
      - state that the text is Kazakh and may contain wrong letters, joined
        words, or letters from the wrong alphabet;
      - demand exactly this JSON and nothing else:
            {"corrected": "...", "changes": ["...", "..."]}
      - do not include the correct answer in the prompt. You are testing the
        model, not your own typing.

    Asking for a fixed shape instead of prose is how you make six models
    comparable. Week 3 turns this into a topic.
    """
    return (
        "The following Kazakh text has been damaged: some letters might be "
        "swapped for similar-looking Russian or Latin letters, a hyphen "
        "might be missing, two words might be joined together, or a letter "
        "might be doubled by mistake.\n\n"
        "Corrupted text: \"" + corrupted + "\"\n\n"
        "Please correct it back to proper Kazakh and tell me what you "
        "changed.\n\n"
        "Answer ONLY with this JSON, nothing else, no ```json fences:\n"
        '{"corrected": "...", "changes": ["...", "..."]}'
    )


def parse_response(text: str) -> dict:
    """Pull {"corrected": str, "changes": list} out of the model's reply.

    Models wrap JSON in prose, or in ```json fences, more often than you would
    like. Be forgiving: find the JSON, parse it, and raise ValueError with the
    offending text if you truly cannot.
    """
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        return {"corrected": data["corrected"], "changes": data["changes"]}
    except (json.JSONDecodeError, KeyError):
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found in model output: " + text)

    json_part = cleaned[start:end + 1]
    data = json.loads(json_part)

    if "corrected" not in data or "changes" not in data:
        raise ValueError("JSON is missing corrected/changes: " + text)

    return {"corrected": data["corrected"], "changes": data["changes"]}


def correct_with(model: str, corrupted: str, via: str) -> dict:
    """Send one sentence to one model.

    Returns:
        {"corrected": str, "changes": list, "input_tokens": int,
         "output_tokens": int, "model": str}

    `via` is "openai" or "openrouter" and goes straight through to
    `ask_once` from sublab_easy - there is no conversation here, just one
    prompt and one reply, eight times per model.
    """
    prompt = build_prompt(corrupted)
    reply = ask_once(prompt, model=model, via=via)
    parsed = parse_response(reply["text"])
    return {
        "corrected": parsed["corrected"],
        "changes": parsed["changes"],
        "input_tokens": reply["input_tokens"],
        "output_tokens": reply["output_tokens"],
        "model": model,
    }


def score_correction(returned: str, expected: str) -> dict:
    """Compare a model's output against the published original.

    Returns {"exact": bool, "char_diff": int} where char_diff is the number of
    differing characters (a simple positional comparison is enough; count the
    length difference too).

    READ THIS: `exact` is a signal, not a grade. Good Kazakh that differs from
    the original still counts as a correction. Your written analysis is where
    you make that call.
    """
    exact = (returned == expected)

    diff_count = 0
    shorter = min(len(returned), len(expected))
    for i in range(shorter):
        if returned[i] != expected[i]:
            diff_count += 1

    diff_count += abs(len(returned) - len(expected))

    return {"exact": exact, "char_diff": diff_count}


def run_all() -> list[dict]:
    """Every model against every sentence. One row per (model, sentence)."""
    rows = []
    for via, model in MODELS:
        for s in load_sentences():
            try:
                r = correct_with(model, s["corrupted"], via)
            except Exception as exc:            # a model failing IS a result
                rows.append({"model": model, "id": s["id"],
                             "errors": s["errors"], "failed": repr(exc)})
                continue
            rate_in, rate_out = RATES_PER_MTOK[model]
            rows.append({
                "model": model,
                "id": s["id"],
                "errors": s["errors"],
                "corrected": r["corrected"],
                "changes": r["changes"],
                **score_correction(r["corrected"], s["correct"]),
                "cost": estimate_cost(r["input_tokens"], r["output_tokens"],
                                      rate_in, rate_out),
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            })
    return rows


def summarise(rows: list[dict]) -> None:
    """Per-model totals, to paste into SUBMISSION.md."""
    print(f"{'model':38}{'exact':>7}{'failed':>8}{'tokens':>9}{'cost $':>10}")
    print("-" * 72)
    for _, model in MODELS:
        mine = [r for r in rows if r["model"] == model]
        exact = sum(1 for r in mine if r.get("exact"))
        failed = sum(1 for r in mine if r.get("failed"))
        toks = sum(r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in mine)
        cost = sum(r.get("cost", 0.0) for r in mine)
        print(f"{model:38}{exact:>7}{failed:>8}{toks:>9}{cost:>10.5f}")


if __name__ == "__main__":
    out = run_all()
    summarise(out)
    dest = Path(__file__).resolve().parent.parent / "outputs"
    dest.mkdir(exist_ok=True)
    (dest / "corrections.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote outputs/corrections.json ({len(out)} rows)")
