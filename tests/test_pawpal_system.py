from datetime import date, datetime

import pytest

from pawpal_system import Owner


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
