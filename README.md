# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Core model

- `Task` stores a description, scheduled date/time, frequency, completion status,
  and the pet and owner it belongs to.
- `Pet` stores its details and care tasks. Its `add_task` method associates new
  tasks with that pet.
- `Owner` manages multiple pets and can retrieve or add tasks by pet name.
- `Scheduler` collects tasks across the owner's pets, sorts them chronologically,
  filters by day or completion status, and marks tasks complete or reopens them.

Completing a daily or weekly task creates the next occurrence one day or seven
days after its scheduled time. One-time tasks do not create future occurrences.
Feeding and vet-history records remain available to the Streamlit app separately
from the general task scheduler.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
Today's Schedule - Sunday, October 11, 2026
07:30 AM - Breakfast (Mochi)
09:00 AM - Morning walk (Biscuit)
06:00 PM - Dinner (Mochi)


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.organize_tasks` | Chronological order; pet name breaks time ties |
| Filtering | `Scheduler.filter_tasks`, `Scheduler.get_tasks_for_day` | Filter by pet name and/or completion status, or select a day |
| Conflict detection | `Scheduler.find_conflicts` | Returns task pairs scheduled at the exact same date and time |
| Completion | `Scheduler.complete_task`, `Scheduler.reopen_task` | Updates the task's completion status |
| Recurring tasks | `Task.frequency`, `Scheduler.complete_task` | Completing daily or weekly tasks schedules the next occurrence |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
