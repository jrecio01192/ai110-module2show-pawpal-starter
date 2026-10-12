"""Core data model for PawPal+ pet care records."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from itertools import combinations
from uuid import uuid4


@dataclass
class Task:
    """A scheduled care task associated with a pet and its owner."""

    description: str
    time: datetime
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""
    owner_name: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Normalize task text and validate required fields."""
        self.description = self.description.strip()
        self.frequency = self.frequency.strip()
        if not self.description:
            raise ValueError("Task description cannot be blank.")
        if not self.frequency:
            raise ValueError("Task frequency cannot be blank.")
        if not isinstance(self.time, datetime):
            raise TypeError("Task time must be a datetime.")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reopen(self) -> None:
        """Mark this task as incomplete again."""
        self.completed = False


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
    tasks: list[Task] = field(default_factory=list)
    feedings: list[FeedingRecord] = field(default_factory=list)
    vet_visits: list[VetVisit] = field(default_factory=list)

    def add_task(self, task: Task) -> Task:
        """Add a task and associate it with this pet and its owner."""
        if not isinstance(task, Task):
            raise TypeError("Pet tasks must be Task instances.")
        if any(existing.id == task.id for existing in self.tasks):
            raise ValueError(f"Task {task.id} is already assigned to {self.name}.")
        task.pet_name = self.name
        task.owner_name = self.owner_name
        self.tasks.append(task)
        return task

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        """Return this pet's tasks, optionally excluding completed tasks."""
        return [
            task
            for task in self.tasks
            if include_completed or not task.completed
        ]

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
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Owner name cannot be blank.")
        self.name = normalized_name
        for pet in self.pets:
            pet.owner_name = self.name
            for task in pet.tasks:
                task.owner_name = self.name
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

    def get_pet(self, pet_name: str) -> Pet:
        """Find one of this owner's pets by case-insensitive name."""
        normalized_name = pet_name.strip().casefold()
        for pet in self.pets:
            if pet.name.casefold() == normalized_name:
                return pet
        raise KeyError(f"No pet named {pet_name!r} belongs to {self.name}.")

    def add_task(self, pet_name: str, task: Task) -> Task:
        """Assign a task to one of this owner's pets."""
        return self.get_pet(pet_name).add_task(task)

    def get_tasks(
        self, pet_name: str | None = None, include_completed: bool = True
    ) -> list[Task]:
        """Collect tasks across all pets or for one named pet."""
        pets = [self.get_pet(pet_name)] if pet_name is not None else self.pets
        return [
            task
            for pet in pets
            for task in pet.get_tasks(include_completed=include_completed)
        ]


@dataclass
class Scheduler:
    """Retrieve, order, filter, and update an owner's pet-care tasks."""

    owner: Owner

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        """Retrieve tasks from every pet owned by this scheduler's owner."""
        return self.owner.get_tasks(include_completed=include_completed)

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Filter tasks by pet name, completion status, or both."""
        tasks = self.owner.get_tasks(pet_name=pet_name, include_completed=True)
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def organize_tasks(self, include_completed: bool = False) -> list[Task]:
        """Return tasks in chronological order, with pet name as a tie-breaker."""
        return sorted(
            self.get_tasks(include_completed=include_completed),
            key=lambda task: (task.time, task.pet_name.casefold(), task.id),
        )

    def find_conflicts(
        self, include_completed: bool = False
    ) -> list[tuple[Task, Task]]:
        """Return pairs of tasks scheduled for the exact same datetime."""
        tasks = self.get_tasks(include_completed=include_completed)
        return [
            (first, second)
            for first, second in combinations(tasks, 2)
            if first.time == second.time
        ]

    def get_tasks_for_day(
        self, day: date, include_completed: bool = False
    ) -> list[Task]:
        """Return chronologically ordered tasks scheduled on a particular day."""
        return [
            task
            for task in self.organize_tasks(include_completed=include_completed)
            if task.time.date() == day
        ]

    def complete_task(self, task_id: str) -> Task:
        """Complete a task and schedule its next occurrence if it repeats."""
        for task in self.get_tasks():
            if task.id == task_id:
                was_completed = task.completed
                task.mark_complete()
                if not was_completed:
                    frequency = task.frequency.casefold()
                    interval = {"daily": 1, "weekly": 7}.get(frequency)
                    if interval is not None:
                        next_task = Task(
                            task.description,
                            task.time + timedelta(days=interval),
                            task.frequency,
                        )
                        self.owner.get_pet(task.pet_name).add_task(next_task)
                return task
        raise KeyError(f"No task with ID {task_id!r} belongs to {self.owner.name}.")

    def reopen_task(self, task_id: str) -> Task:
        """Reopen a task by its unique ID and return the task."""
        for task in self.get_tasks():
            if task.id == task_id:
                task.reopen()
                return task
        raise KeyError(f"No task with ID {task_id!r} belongs to {self.owner.name}.")
