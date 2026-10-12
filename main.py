"""Run a small PawPal+ pet-care schedule demo."""

from datetime import date, datetime, time

from pawpal_system import Owner, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    owner.add_pet("Mochi", "Cat")
    owner.add_pet("Biscuit", "Dog")

    today = date.today()
    owner.add_task(
        "Mochi",
        Task("Breakfast", datetime.combine(today, time(7, 30)), "daily"),
    )
    owner.add_task(
        "Biscuit",
        Task("Morning walk", datetime.combine(today, time(9, 0)), "daily"),
    )
    owner.add_task(
        "Mochi",
        Task("Dinner", datetime.combine(today, time(18, 0)), "daily"),
    )

    scheduler = Scheduler(owner)
    print(f"Today's Schedule - {today:%A, %B %d, %Y}")
    for task in scheduler.get_tasks_for_day(today):
        print(f"{task.time:%I:%M %p} - {task.description} ({task.pet_name})")


if __name__ == "__main__":
    main()
