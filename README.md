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

tests\test_pawpal.py ................                                                     [100%]

====================================== 16 passed in 0.04s ======================================

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.organize_tasks` | Chronological order; pet name breaks time ties |
| Filtering | `Scheduler.filter_tasks`, `Scheduler.get_tasks_for_day` | Filter by pet name and/or completion status, or select a day |
| Conflict detection | `Scheduler.find_conflicts` | Returns task pairs scheduled at the exact same date and time |
| Completion | `Scheduler.complete_task`, `Scheduler.reopen_task` | Updates the task's completion status |
| Recurring tasks | `Task.frequency`, `Scheduler.complete_task` | Completing daily or weekly tasks schedules the next occurrence |

## 📸 Demo Walkthrough

### 1. Launch the Application
Run the Streamlit application using `py -m streamlit run app.py`. The PawPal+ interface allows users to manage their pets, feeding records, veterinary visits, and scheduled care tasks. Users can also update their owner's name through the sidebar.

### 2. Add a Pet
Navigate to the Pets tab and enter the pet's name and species. Click the **Add pet** button to register the pet. The application displays the registered pets and prevents duplicate or blank pet names.

### 3. Schedule Pet Care Tasks
Select a registered pet and create a care task by entering its description, scheduled date and time, and frequency. For example, a user can schedule breakfast for Mochi at 7:30 AM and a morning walk for Biscuit at 9:00 AM. Tasks are associated with their respective pets and owners.

### 4. View Today's Schedule
The Scheduler organizes tasks chronologically, regardless of the order in which they were created. Users can view tasks scheduled for a particular day using `Scheduler.get_tasks_for_day()`.

Example daily schedule:

**Today's Schedule - Sunday, October 11, 2026**

- 07:30 AM - Breakfast (Mochi)
- 09:00 AM - Morning walk (Biscuit)
- 06:00 PM - Dinner (Mochi)

### 5. Sorting, Filtering, and Conflict Detection
The Scheduler provides several features for organizing pet care responsibilities:

- **Sorting:** `organize_tasks()` arranges tasks from earliest to latest.
- **Filtering:** `filter_tasks()` displays tasks based on pet name or completion status.
- **Daily schedule:** `get_tasks_for_day()` retrieves tasks scheduled for a selected date.
- **Conflict detection:** `find_conflicts()` identifies tasks scheduled at the exact same date and time.
- **Completion tracking:** `complete_task()` marks tasks as completed, while `reopen_task()` marks them as incomplete again.
- **Recurring tasks:** Completing a daily or weekly task creates its next scheduled occurrence.

Conflict detection only identifies identical scheduled times and does not account for overlapping task durations.

### 6. Test the Scheduler in the Terminal
Run `py main.py` to test the scheduling logic independently of the Streamlit interface. Tasks are intentionally added out of chronological order to verify that sorting and filtering work correctly.

**Sample CLI output (illustrative):**

```text
=== TASKS SORTED BY TIME ===
2026-10-15 08:00:00 | Bella | Morning feeding
2026-10-15 14:00:00 | Max | Afternoon playtime
2026-10-15 18:00:00 | Max | Evening walk
2026-10-16 10:00:00 | Bella | Vet appointment

=== TASKS FOR MAX ===
Max | Evening walk
Max | Afternoon playtime

=== INCOMPLETE TASKS ===
Bella | Morning feeding
Max | Afternoon playtime
Bella | Vet appointment

=== COMPLETED TASKS ===
Max | Evening walk
```

### 7. Verify Application Functionality
Run `pytest` to execute the automated tests. These tests verify important scheduling behaviors, including sorting, filtering, task completion, and other implemented scheduling features.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
