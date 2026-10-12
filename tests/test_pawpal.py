from datetime import date, datetime

import pytest

from pawpal_system import Owner, Scheduler, Task


def test_owner_can_add_multiple_pets():
    owner = Owner("Jordan")

    first_pet = owner.add_pet("Mochi", "Cat")
    second_pet = owner.add_pet("Biscuit", "Dog")

    assert owner.pets == [first_pet, second_pet]
    assert [pet.owner_name for pet in owner.pets] == ["Jordan", "Jordan"]


def test_owner_rejects_blank_and_duplicate_pet_names():
    owner = Owner("Jordan")
    owner.add_pet("Mochi", "Cat")

    with pytest.raises(ValueError, match="cannot be blank"):
        owner.add_pet("  ", "Dog")
    with pytest.raises(ValueError, match="already"):
        owner.add_pet("mochi", "Dog")


def test_pet_records_include_pet_and_owner_names():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")

    feeding = pet.add_feeding(datetime(2026, 10, 10, 8, 30), "Dry food")
    visit = pet.add_vet_visit(date(2026, 10, 9), "Happy Paws", "Annual checkup")

    assert (feeding.pet_name, feeding.owner_name, feeding.food) == (
        "Mochi",
        "Jordan",
        "Dry food",
    )
    assert (visit.pet_name, visit.owner_name, visit.veterinarian, visit.notes) == (
        "Mochi",
        "Jordan",
        "Happy Paws",
        "Annual checkup",
    )
    assert pet.feedings == [feeding]
    assert pet.vet_visits == [visit]


def test_renaming_owner_updates_pets_and_existing_records():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    feeding = pet.add_feeding(datetime(2026, 10, 10, 8, 30))
    visit = pet.add_vet_visit(date(2026, 10, 9), "Happy Paws", "Annual checkup")

    owner.rename("  Casey  ")

    assert owner.name == "Casey"
    assert pet.owner_name == "Casey"
    assert feeding.owner_name == "Casey"
    assert visit.owner_name == "Casey"


def test_cannot_add_pet_without_owner_name():
    with pytest.raises(ValueError, match="Owner name cannot be blank"):
        Owner(" ").add_pet("Mochi", "Cat")


def test_task_validates_required_fields_and_tracks_completion():
    task = Task("  Morning meal  ", datetime(2026, 10, 11, 8), "  daily  ")

    assert task.description == "Morning meal"
    assert task.frequency == "daily"
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True
    task.reopen()
    assert task.completed is False

    with pytest.raises(ValueError, match="description cannot be blank"):
        Task("  ", datetime(2026, 10, 11, 8))
    with pytest.raises(ValueError, match="frequency cannot be blank"):
        Task("Meal", datetime(2026, 10, 11, 8), " ")
    with pytest.raises(TypeError, match="datetime"):
        Task("Meal", date(2026, 10, 11))  # type: ignore[arg-type]


def test_owner_assigns_tasks_to_pets_and_updates_owner_attribution():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    task = Task("Morning meal", datetime(2026, 10, 11, 8), "daily")

    assert owner.add_task("mochi", task) is task
    assert pet.tasks == [task]
    assert (task.pet_name, task.owner_name) == ("Mochi", "Jordan")

    owner.rename("Casey")
    assert task.owner_name == "Casey"


def test_owner_rejects_tasks_for_unknown_pets_and_duplicate_task_ids():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    task = Task("Morning meal", datetime(2026, 10, 11, 8), id="meal-1")
    pet.add_task(task)

    with pytest.raises(KeyError, match="No pet named"):
        owner.add_task("Biscuit", Task("Walk", datetime(2026, 10, 11, 9)))
    with pytest.raises(ValueError, match="already assigned"):
        pet.add_task(Task("Evening meal", datetime(2026, 10, 11, 18), id="meal-1"))


def test_scheduler_organizes_filters_and_manages_tasks_across_pets():
    owner = Owner("Jordan")
    mochi = owner.add_pet("Mochi", "Cat")
    biscuit = owner.add_pet("Biscuit", "Dog")
    later = biscuit.add_task(Task("Evening meal", datetime(2026, 10, 11, 18), "daily"))
    earlier = mochi.add_task(Task("Morning meal", datetime(2026, 10, 11, 8), "daily"))
    tomorrow = mochi.add_task(
        Task("Vet checkup", datetime(2026, 10, 12, 10), "once")
    )
    scheduler = Scheduler(owner)

    assert scheduler.get_tasks() == [earlier, tomorrow, later]
    assert scheduler.organize_tasks() == [earlier, later, tomorrow]
    assert scheduler.get_tasks_for_day(date(2026, 10, 11)) == [earlier, later]

    assert scheduler.complete_task(earlier.id) is earlier
    assert earlier.completed is True
    next_morning_meal = mochi.tasks[-1]
    assert next_morning_meal.description == earlier.description
    assert next_morning_meal.time == datetime(2026, 10, 12, 8)
    assert scheduler.organize_tasks() == [later, next_morning_meal, tomorrow]
    assert scheduler.organize_tasks(include_completed=True) == [
        earlier,
        later,
        next_morning_meal,
        tomorrow,
    ]
    assert scheduler.reopen_task(earlier.id) is earlier
    assert earlier.completed is False

    with pytest.raises(KeyError, match="No task with ID"):
        scheduler.complete_task("missing-task")


def test_scheduler_filters_tasks_by_pet_name_and_completion_status():
    owner = Owner("Jordan")
    mochi = owner.add_pet("Mochi", "Cat")
    biscuit = owner.add_pet("Biscuit", "Dog")
    completed_task = mochi.add_task(Task("Morning meal", datetime(2026, 10, 11, 8)))
    active_task = biscuit.add_task(Task("Walk", datetime(2026, 10, 11, 9)))
    completed_task.mark_complete()
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=True) == [completed_task]
    assert scheduler.filter_tasks(completed=False) == [active_task]
    assert scheduler.filter_tasks(pet_name="mOcHi") == [completed_task]
    assert scheduler.filter_tasks(pet_name="Mochi", completed=True) == [completed_task]
    assert scheduler.filter_tasks(pet_name="Biscuit", completed=True) == []

    with pytest.raises(KeyError, match="No pet named"):
        scheduler.filter_tasks(pet_name="Unknown")


@pytest.mark.parametrize(
    ("frequency", "expected_time"),
    [
        ("daily", datetime(2026, 10, 12, 8, 30)),
        ("weekly", datetime(2026, 10, 18, 8, 30)),
    ],
)
def test_completing_recurring_task_schedules_next_occurrence(
    frequency, expected_time
):
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    task = pet.add_task(Task("Medication", datetime(2026, 10, 11, 8, 30), frequency))
    scheduler = Scheduler(owner)

    assert scheduler.complete_task(task.id) is task

    assert task.completed is True
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task is not task
    assert next_task.id != task.id
    assert next_task.description == task.description
    assert next_task.time == expected_time
    assert next_task.frequency == task.frequency
    assert next_task.completed is False
    assert (next_task.pet_name, next_task.owner_name) == ("Mochi", "Jordan")

    scheduler.complete_task(task.id)
    assert len(pet.tasks) == 2


def test_completing_one_time_task_does_not_schedule_another_occurrence():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    task = pet.add_task(Task("Vet appointment", datetime(2026, 10, 11, 8, 30)))

    Scheduler(owner).complete_task(task.id)

    assert task.completed is True
    assert pet.tasks == [task]


def test_scheduler_returns_tasks_in_chronological_order():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    evening = pet.add_task(Task("Dinner", datetime(2026, 10, 11, 18)))
    morning = pet.add_task(Task("Breakfast", datetime(2026, 10, 11, 8)))
    afternoon = pet.add_task(Task("Walk", datetime(2026, 10, 11, 13)))

    assert Scheduler(owner).organize_tasks() == [morning, afternoon, evening]


def test_completing_daily_task_creates_next_day_occurrence():
    owner = Owner("Jordan")
    pet = owner.add_pet("Mochi", "Cat")
    task = pet.add_task(
        Task("Medication", datetime(2026, 10, 11, 8, 30), "daily")
    )

    Scheduler(owner).complete_task(task.id)

    assert len(pet.tasks) == 2
    next_occurrence = pet.tasks[1]
    assert next_occurrence.time == datetime(2026, 10, 12, 8, 30)
    assert next_occurrence.description == task.description
    assert next_occurrence.frequency == "daily"
    assert next_occurrence.completed is False


def test_scheduler_finds_tasks_with_duplicate_times():
    owner = Owner("Jordan")
    mochi = owner.add_pet("Mochi", "Cat")
    biscuit = owner.add_pet("Biscuit", "Dog")
    shared_time = datetime(2026, 10, 11, 8)
    first = mochi.add_task(Task("Breakfast", shared_time))
    second = biscuit.add_task(Task("Medication", shared_time))
    unique = mochi.add_task(Task("Walk", datetime(2026, 10, 11, 9)))

    conflicts = Scheduler(owner).find_conflicts()
    assert conflicts == [(first, second)]
    assert all(unique not in conflict for conflict in conflicts)
