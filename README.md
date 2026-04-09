# Sales Leadership Board Blueprint

**Turn CRM call data into individualized coaching, automated training diagnostics, and ICP validation.**

15 EUR/month. No Gong. No vendor lock-in. Your code, your data.

---

## What This Does

Most sales dashboards show you WHAT happened. This system tells each rep WHAT TO PRACTICE.

| Feature | Description |
|---------|-------------|
| **Daily KPI Tracking** | Pulls calls, emails, meetings from Close.com or HubSpot API every day at 18:00 CET |
| **Call Scoring (6 Dimensions)** | Each call scored 1-10 on Opener, Pitch, Objection Handling, Closing, Depth, Rapport |
| **Email Scoring (6 Dimensions)** | Each email scored on Subject, Personalization, Value Prop, CTA, Tonality, Length |
| **Gap-Detection Matrix** | 2-axis diagnosis: Activity (calls+emails vs target) x Outcomes (connect rate+meetings+pipeline) |
| **Individualized Coaching** | Each rep gets 2 coaching focuses per week based on their weakest dimension |
| **4-Phase Ramping** | Auto-adjusting targets based on rep start date (Phase 1-4, day 0 to 90+) |
| **Objection Library** | 44 pre-written scripts with fuzzy-matching to lost reasons |
| **ICP Feedback Loop** | Lost reasons + call summaries feed back into targeting and pitch optimization |
| **Leaderboards** | Weekly rankings per metric across the team |
| **Telegram Briefing** | Daily summary with alerts, ramping checkpoints, coaching priorities |

---

## Architecture

```
Close.com / HubSpot CRM
    |
    | REST API (activity/call, activity/email, activity/meeting)
    v
+---------------------------+
|   Python Bot (cron daily) |
|   - Pagination + Retry    |
|   - Rate limiting         |
|   - Rep mapping           |
+---------------------------+
    |                    |
    v                    v
+-----------+    +----------------+
| Deepgram  |    | Claude API     |
| STT       |    | Call Scoring   |
| 0.0065/min|    | 0.002/call     |
+-----------+    +----------------+
    |                    |
    v                    v
+------------------------------------------+
|          Google Sheets (8 Tabs)           |
| - Master Dashboard (Gap Matrix, Trends)  |
| - Daily KPIs (raw data + formulas)       |
| - Call Analysis (per-call + transcript)  |
| - Email Analysis (per-email scoring)     |
| - Lost Reasons (objection tracking)      |
| - Q&A / Einwandbehandlung (44 scripts)   |
| - Leaderboards (weekly rankings)         |
| - Individual Coaching (per rep)          |
+------------------------------------------+
    |
    v
+------------------+
| Telegram Bot     |
| Daily briefing   |
| Ramping alerts   |
+------------------+
```

---

## Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| AWS Lightsail | 5 EUR/mo | Or any VPS / GitHub Actions |
| Deepgram | ~7 EUR/mo | 0.0065 EUR/min, ~18 hrs of calls/month |
| Claude API | ~3 EUR/mo | 0.002 EUR/call analysis, ~1500 calls/month |
| Google Sheets API | Free | Up to 60 req/min |
| Telegram Bot | Free | |
| **Total** | **~15 EUR/mo** | vs. Gong: ~9,300 EUR/yr for 3 users |

---

## Setup Guide

### Prerequisites

```
Python 3.10+
pip install requests google-api-python-client google-auth google-auth-oauthlib gspread python-telegram-bot anthropic deepgram-sdk python-dotenv
```

### Step 1: Environment Variables

Create a `.env` file:

```bash
# CRM (pick one)
CLOSE_API_KEY=api_xxxxxxxxxxxxxxxx
# HUBSPOT_API_KEY=pat-xxxxxxxx

# Google Sheets
GOOGLE_SHEET_ID=1aBcDeFgHiJkLmNoPqRsTuVwXyZ

# AI
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
DEEPGRAM_API_KEY=xxxxxxxxxxxxxxxx

# Notifications (optional)
TELEGRAM_BOT_TOKEN=123456:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=-1001234567890
```

### Step 2: Configure Targets

Create `targets.json`:

```json
{
  "reps": {
    "Jane Smith": {
      "ramping_level": "auto",
      "start_date": "2026-03-01"
    },
    "Max Mueller": {
      "ramping_level": "phase_4_fully_ramped"
    }
  },
  "targets": {
    "phase_1_month_1": {
      "calls_per_day": 40,
      "connect_rate": 0.05,
      "discovery_calls_booked_per_week": 2,
      "potential_revenue_eur": 30000,
      "speed_to_lead_minutes": 60,
      "emails_sent_per_day": 15
    },
    "phase_2_month_2": {
      "calls_per_day": 55,
      "connect_rate": 0.08,
      "discovery_calls_booked_per_week": 4,
      "potential_revenue_eur": 60000,
      "speed_to_lead_minutes": 30,
      "emails_sent_per_day": 25
    },
    "phase_3_month_3": {
      "calls_per_day": 65,
      "connect_rate": 0.10,
      "discovery_calls_booked_per_week": 6,
      "potential_revenue_eur": 100000,
      "speed_to_lead_minutes": 15,
      "emails_sent_per_day": 30
    },
    "phase_4_fully_ramped": {
      "calls_per_day": 70,
      "connect_rate": 0.12,
      "discovery_calls_booked_per_week": 8,
      "potential_revenue_eur": 150000,
      "speed_to_lead_minutes": 10,
      "emails_sent_per_day": 40
    }
  },
  "ampel": {
    "green_threshold": 1.0,
    "yellow_threshold": 0.8
  },
  "thresholds": {
    "opener_problem_connect_rate": 0.08,
    "pitch_problem_connect_rate": 0.10,
    "pitch_problem_conv_to_meeting": 0.10,
    "depth_problem_avg_duration_seconds": 180,
    "speed_problem_minutes": 30
  }
}
```

### Step 3: Schedule

```bash
# Linux/Mac cron (Mo-Fr 18:00 CET)
0 18 * * 1-5 cd /path/to/project && python main_closecom.py

# Or GitHub Actions (see .github/workflows/daily.yml example below)
```

---

## Gap-Detection Matrix

The core diagnostic logic replaces simple if/elif chains with a 2-axis classification:

```
                    Outcomes RED         Outcomes YELLOW      Outcomes GREEN
                    (CR/Meetings/        (close to target)    (hitting target)
                     Pipeline below)

Activity RED        EFFORT_GAP           EFFORT_GAP           EFFICIENCY_STAR
(calls+emails       "Do more. Period."   "Volume up =         "Great conversion.
 below target)                            results follow"      Scale volume."

Activity YELLOW     SKILL_GAP            PLATEAU              EFFICIENCY_STAR
(close to target)   "Quality over        "Both axes need      "Strong conversion.
                     quantity"            nudging"              Push volume."

Activity GREEN      SKILL_GAP            SKILL_GAP            SCALE_GAP
(hitting target)    "Doing enough,       "Conversion needs    "All green.
                     results missing"     work"                Optimize pipeline."
```

Each rep gets a **main diagnosis** plus **sub-diagnoses**:
- PITCH: Connects but no meetings -> Value prop problem
- OPENER: Connect rate too low -> Hook rotation needed
- DEPTH: Calls too short -> Open questions, SPIN
- SPEED: Speed-to-lead above threshold
- CLOSING: Proposals but no Won
- PROPOSAL: Meetings but no proposals

---

## Call Scoring Dimensions

Each call is scored 1-10 across 6 dimensions via Claude API:

| Dimension | What It Measures | Training Module |
|-----------|-----------------|-----------------|
| **Opener** | Hook quality, pattern-interrupt, gatekeeper bypass | Hook-Rotation, verschiedene Opener testen |
| **Pitch** | Value prop clarity, problem-first approach, ROI argument | Value Prop Workshop, ROI-Kalkulator |
| **Objection Handling** | LARC framework execution, reframing, counter-questions | LARC drill, Adesso War Story, Reframing |
| **Closing** | Ask clarity, silence after ask, commitment language | 1-10 Close, Hypothetical, Summary, Trial |
| **Depth** | Open questions, SPIN technique, mirroring | SPIN Selling, 3-second pause, mirroring |
| **Rapport** | Active listening, tonality, labeling | Mirroring, Labeling, Tonality training |

The system automatically finds the **weakest dimension per rep** (14-day rolling window) and maps it to the correct training module.

---

## Email Scoring Dimensions

| Dimension | What It Measures | Training Module |
|-----------|-----------------|-----------------|
| **Subject Line** | Open-rate optimization, personalization | A/B Test Subject Lines |
| **Personalization** | Lead research, trigger events | Deeper lead research |
| **Value Proposition** | ROI arguments, concrete numbers | Case Studies, ROI calculator |
| **CTA** | Single clear CTA, calendar link | CTA optimization |
| **Tonality** | Peer-to-peer, conversational | Less formal, more human |
| **Length** | Max 5 sentences, bullet points | Brevity training |

---

## Training Methodology: The WHY

### LARC Framework (Objection Handling)
- **L**isten: Let them finish. No interrupting.
- **A**cknowledge: "I understand." / "That makes sense."
- **R**espond: Address the real concern, not the surface objection.
- **C**onfirm: "Does that address your concern?"

**Why LARC?** Unstructured objection handling leads to argument mode. LARC keeps the conversation collaborative. Reps who drill LARC see 2-3x improvement in objection-to-meeting conversion.

### SPIN Selling (Discovery)
- **S**ituation: Current state questions
- **P**roblem: Pain identification
- **I**mplication: Cost of inaction
- **N**eed-payoff: Value of solving

**Why SPIN?** Prospects don't buy features. They buy solutions to problems they've articulated themselves. SPIN makes the prospect sell themselves on the meeting.

### Pattern-Interrupt (Openers)
First 7 seconds determine if the call continues. Standard openers ("Hi, this is X from Y, we do Z") trigger an automatic "not interested" response.

**Why?** Decision-makers receive 5-15 cold outreach messages per week. Pattern-interrupts bypass the autopilot rejection.

### 3-Second Pause Rule
After every question, count to 3 before speaking. The prospect fills silence with real information.

**Why?** Average sales reps wait 0.8 seconds. Top performers wait 3-5 seconds. Silence is uncomfortable but productive.

### Ramping Phases
New reps need different targets than fully ramped reps. Comparing a Week-2 rep to a Month-6 rep on the same KPIs produces false negatives and demotivation.

**Why 4 phases?** Based on typical B2B SDR ramp-up curves:
- Month 1: Learning the product, market, tools. Lower volume, higher tolerance.
- Month 2: Building muscle memory. Volume increasing, quality emerging.
- Month 3: Approaching full capacity. Fine-tuning conversion.
- Month 4+: Fully ramped. Full targets, optimization focus.

---

## ICP Feedback Loop

The Sales Leadership Board is not just a coaching tool. It is an ICP validation engine.

### How It Works

1. **Lost Reasons** are tracked per deal with company context
2. **Call summaries** capture objections verbatim from transcripts
3. **Pattern analysis** across 200+ calls reveals market shifts:
   - "Too many applicants" appearing in 10+ calls = market shift, not rep problem
   - "Already working with 3 recruiters" = positioning problem, not pitch problem
   - 52% gatekeeper blockade = targeting problem, not skill problem

### Output

- **ICP tightening**: Remove segments that consistently reject (e.g., companies with <50 employees)
- **Pitch rewriting**: Align messaging to ACTUAL objections, not assumed ones
- **Objection script library**: 44 scripts fuzzy-matched to real lost reasons
- **Targeting shift**: From "anyone with an open role" to "companies drowning in 200 applications but zero qualified candidates"

---

## File Structure

```
sales-leadership-board/
  main_closecom.py          # Entry point for Close.com
  main_hubspot.py           # Entry point for HubSpot
  crm/
    closecom.py             # Close.com API client
    hubspot.py              # HubSpot API client
    base.py                 # Abstract CRM interface
  scoring/
    call_scorer.py          # Claude-based call scoring
    email_scorer.py         # Claude-based email scoring
    gap_matrix.py           # Gap-Detection Matrix logic
  training/
    ramping.py              # 4-phase ramping logic
    coaching.py             # Weakest-dimension detection
    objection_library.py    # LARC scripts + fuzzy matching
  output/
    sheets_writer.py        # Google Sheets output (8 tabs)
    telegram_notifier.py    # Telegram daily briefing
  config/
    targets.json            # Rep config + phase targets
  .env.example              # Environment variable template
  requirements.txt          # Python dependencies
  README.md                 # This file
```

---

## Quick Start (Close.com)

```python
# main_closecom.py - Minimal working example
import os
from dotenv import load_dotenv
from crm.closecom import CloseComClient
from scoring.gap_matrix import diagnose
from output.sheets_writer import write_dashboard

load_dotenv()

client = CloseComClient(os.getenv("CLOSE_API_KEY"))
daily_data = client.collect_daily()  # Pulls today's calls, emails, meetings

for rep_name, metrics in daily_data.items():
    diagnosis = diagnose(metrics, phase="phase_2_month_2")
    print(f"{rep_name}: {diagnosis['main_diagnosis']} -> {diagnosis['coaching_focus']}")

write_dashboard(daily_data, os.getenv("GOOGLE_SHEET_ID"))
```

---

## Quick Start (HubSpot)

```python
# main_hubspot.py - Minimal working example
import os
from dotenv import load_dotenv
from crm.hubspot import HubSpotClient
from scoring.gap_matrix import diagnose
from output.sheets_writer import write_dashboard

load_dotenv()

client = HubSpotClient(os.getenv("HUBSPOT_API_KEY"))
daily_data = client.collect_daily()  # Pulls today's calls, emails, meetings

for rep_name, metrics in daily_data.items():
    diagnosis = diagnose(metrics, phase="auto")
    print(f"{rep_name}: {diagnosis['main_diagnosis']} -> {diagnosis['coaching_focus']}")

write_dashboard(daily_data, os.getenv("GOOGLE_SHEET_ID"))
```

---

## CRM API Reference

### Close.com Endpoints Used

| Endpoint | Purpose | Auth |
|----------|---------|------|
| `GET /api/v1/activity/call/` | Call records with duration, disposition, notes | Basic Auth (API key as username) |
| `GET /api/v1/activity/email/` | Email activity tracking | Basic Auth |
| `GET /api/v1/activity/meeting/` | Meeting records | Basic Auth |
| `GET /api/v1/user/` | User mapping (rep names to IDs) | Basic Auth |
| `GET /api/v1/lead/{id}/` | Lead details (company name, status) | Basic Auth |

**Rate Limiting**: 15s pause every 80 requests. Exponential backoff on 429/5xx (1, 2, 4 seconds).

**Pagination**: `_skip` + `_limit=100` until `has_more=false`.

### HubSpot Endpoints Used

| Endpoint | Purpose | Auth |
|----------|---------|------|
| `GET /crm/v3/objects/calls` | Call engagement records | Bearer token |
| `GET /crm/v3/objects/emails` | Email engagement records | Bearer token |
| `GET /crm/v3/objects/meetings` | Meeting engagement records | Bearer token |
| `GET /crm/v3/owners` | Owner/rep mapping | Bearer token |
| `GET /crm/v3/objects/contacts/{id}` | Contact details | Bearer token |
| `GET /crm/v3/objects/deals` | Deal pipeline + revenue | Bearer token |

**Rate Limiting**: 100 requests/10 seconds (private apps). Use `after` cursor for pagination.

---

## License

MIT. Use it, modify it, share it. Attribution appreciated but not required.

Built by Christoph Erler / Erler Ventures.
