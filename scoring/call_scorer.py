"""
Claude-based Call Scoring.
Scores each call transcript across 6 dimensions (1-10).
"""

import os
import json
import logging

log = logging.getLogger("slb.call_scorer")

SCORING_PROMPT = """You are an expert B2B sales coach. Analyze this cold call transcript and score it across 6 dimensions (1-10 each).

## Scoring Dimensions

1. **Opener** (1-10): Did the rep use a pattern-interrupt? Was the hook compelling? Did they bypass the gatekeeper effectively?
2. **Pitch** (1-10): Was the value proposition clear and problem-first? Did they use ROI arguments? Was it tailored to the prospect?
3. **Objection Handling** (1-10): Did they use the LARC framework (Listen-Acknowledge-Respond-Confirm)? Did they reframe objections? Did they ask counter-questions?
4. **Closing** (1-10): Did they ask for a next step? Did they use silence after the ask? Was there a clear commitment request?
5. **Depth** (1-10): Did they ask open questions? Did they use SPIN technique? Did they pause after questions (3-second rule)?
6. **Rapport** (1-10): Active listening signals? Mirroring? Labeling? Appropriate tonality?

## Transcript

Rep: {rep_name}
Company: {company_name}
Duration: {duration}

{transcript}

## Output Format (JSON only)

{{
  "opener": <score>,
  "pitch": <score>,
  "objection_handling": <score>,
  "closing": <score>,
  "depth": <score>,
  "rapport": <score>,
  "overall_score": <average>,
  "summary": "<2-sentence summary of the call>",
  "strengths": "<what went well>",
  "improvements": "<what to improve>",
  "objections_detected": "<list of objections raised by the prospect>",
  "key_moment": "<the most important moment in the call>",
  "training_recommendation": "<specific training focus based on weakest dimension>"
}}
"""


def score_call(
    transcript: str,
    rep_name: str,
    company_name: str,
    duration: str,
    api_key: str = None,
    model: str = "claude-sonnet-4-6",
) -> dict:
    """
    Score a single call transcript using Claude API.

    Returns dict with scores (1-10) for each dimension plus summary fields.
    Cost: ~0.002 EUR per call.
    """
    try:
        import anthropic
    except ImportError:
        log.error("pip install anthropic required for call scoring")
        return {}

    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    prompt = SCORING_PROMPT.format(
        rep_name=rep_name,
        company_name=company_name,
        duration=duration,
        transcript=transcript[:8000],  # Truncate to stay within token limits
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()

        # Extract JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    except Exception as e:
        log.error(f"Call scoring failed for {rep_name}/{company_name}: {e}")
        return {}


def score_email(
    subject: str,
    body: str,
    rep_name: str,
    api_key: str = None,
    model: str = "claude-sonnet-4-6",
) -> dict:
    """
    Score a single outbound email using Claude API.
    Dimensions: Subject Line, Personalization, Value Prop, CTA, Tonality, Length.
    """
    try:
        import anthropic
    except ImportError:
        return {}

    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Score this B2B cold email across 6 dimensions (1-10 each).

## Dimensions
1. **Subject Line** (1-10): Compelling? Personalized? Would you open it?
2. **Personalization** (1-10): Research evident? Trigger events? Relevant context?
3. **Value Proposition** (1-10): Clear? ROI-focused? Problem-first?
4. **CTA** (1-10): Single clear CTA? Calendar link? No double-CTA?
5. **Tonality** (1-10): Peer-to-peer? Not too formal? Conversational?
6. **Length** (1-10): Under 5 sentences? Bullet points? Scannable?

## Email
From: {rep_name}
Subject: {subject}

{body}

## Output (JSON only)
{{
  "subject_line": <score>,
  "personalization": <score>,
  "value_proposition": <score>,
  "cta": <score>,
  "tonality": <score>,
  "length": <score>,
  "overall_score": <average>,
  "improvements": "<what to improve>"
}}"""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)

    except Exception as e:
        log.error(f"Email scoring failed for {rep_name}: {e}")
        return {}
