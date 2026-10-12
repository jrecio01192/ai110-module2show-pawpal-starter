
from datetime import datetime
from pawpal_system import Owner, Task, Scheduler

# Step 1: Create an owner and add pets
owner = Owner("Jordan")

owner.add_pet("Max", "Dog")
owner.add_pet("Bella", "Cat")

# Step 2: Create the scheduler
scheduler = Scheduler(owner)

# Step 3: Add tasks OUT OF ORDER
owner.add_task("Max", Task(
    description="Evening walk",
    time=datetime(2026, 10, 15, 18, 0)
))

owner.add_task("Bella", Task(
    description="Morning feeding",
    time=datetime(2026, 10, 15, 8, 0)
))

owner.add_task("Max", Task(
    description="Afternoon playtime",
    time=datetime(2026, 10, 15, 14, 0)
))

owner.add_task("Bella", Task(
    description="Vet appointment",
    time=datetime(2026, 10, 16, 10, 0)
))

# Step 4: Test sorting
print("\n=== TASKS SORTED BY TIME ===")

for task in scheduler.organize_tasks():
    print(f"{task.time} | {task.pet_name} | {task.description}")

# Step 5: Test filtering by pet
print("\n=== TASKS FOR MAX ===")

for task in scheduler.filter_tasks(pet_name="Max"):
    print(f"{task.pet_name} | {task.description}")

# Step 6: Test filtering by completion status
tasks = scheduler.get_tasks()
tasks[0].mark_complete()

print("\n=== INCOMPLETE TASKS ===")

for task in scheduler.filter_tasks(completed=False):
    print(f"{task.pet_name} | {task.description}")

print("\n=== COMPLETED TASKS ===")

for task in scheduler.filter_tasks(completed=True):
    print(f"{task.pet_name} | {task.description}")
