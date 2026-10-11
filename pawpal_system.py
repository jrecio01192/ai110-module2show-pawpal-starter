"""Core data model for PawPal+ pet care records."""

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class FeedingRecord:
    pet_name: str
    owner_name: str
    fed_at: datetime
    food: str = ""


@dataclass
class VetVisit:
    pet_name: str
    owner_name: str
    visit_date: date
    veterinarian: str
    notes: str


@dataclass
class Pet:
    name: str
    species: str
    owner_name: str
    feedings: list[FeedingRecord] = field(default_factory=list)
    vet_visits: list[VetVisit] = field(default_factory=list)

    def add_feeding(self, fed_at: datetime, food: str = "") -> FeedingRecord:
        """Record a feeding for this pet and return the new entry."""
        record = FeedingRecord(self.name, self.owner_name, fed_at, food.strip())
        self.feedings.append(record)
        return record

    def add_vet_visit(
        self, visit_date: date, veterinarian: str, notes: str
    ) -> VetVisit:
        """Record a vet visit for this pet and return the new entry."""
        record = VetVisit(
            self.name, self.owner_name, visit_date, veterinarian.strip(), notes.strip()
        )
        self.vet_visits.append(record)
        return record


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def rename(self, name: str) -> None:
        """Update the owner name on the owner, pets, and their existing records."""
        self.name = name.strip()
        for pet in self.pets:
            pet.owner_name = self.name
            for record in pet.feedings:
                record.owner_name = self.name
            for visit in pet.vet_visits:
                visit.owner_name = self.name

    def add_pet(self, name: str, species: str) -> Pet:
        """Add a pet to this owner, rejecting blank or duplicate names."""
        pet_name = name.strip()
        if not pet_name:
            raise ValueError("Pet name cannot be blank.")
        if any(pet.name.casefold() == pet_name.casefold() for pet in self.pets):
            raise ValueError(f"{pet_name} is already on this owner's pet list.")
        if not self.name.strip():
            raise ValueError("Owner name cannot be blank.")

        pet = Pet(pet_name, species.strip(), self.name)
        self.pets.append(pet)
        return pet
