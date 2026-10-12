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
    assert scheduler.organize_tasks() == [later, tomorrow]
    assert scheduler.organize_tasks(include_completed=True) == [
        earlier,
        later,
        tomorrow,
    ]
    assert scheduler.reopen_task(earlier.id) is earlier
    assert earlier.completed is False

    with pytest.raises(KeyError, match="No task with ID"):
        scheduler.complete_task("missing-task")
