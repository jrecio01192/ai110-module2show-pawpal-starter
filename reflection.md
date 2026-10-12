# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. add feeding times for pets
2. add a pet
3. vetanarian check up history

FeedingRecord Class: The FeedingRecord class stores information about a pet's feeding history. It keeps track of the pet's name, owner's name, the date and time the pet was fed, and the type of food given. Its main responsibility is to maintain individual feeding records so owners can track when and what their pets have eaten.

VetVisit Class: The VetVisit class stores information about a pet's veterinary appointments. It records the pet's name, owner's name, date of the visit, veterinarian's name, and any notes from the appointment. Its main responsibility is to maintain a history of veterinary visits so owners can keep track of their pet's medical care.

Pet Class: The Pet class represents an individual pet and stores basic information such as its name, species, and owner's name. It also maintains lists of feeding records and veterinary visits. The class includes methods called add_feeding() and add_vet_visit(), which create new records and add them to the appropriate lists. Its main responsibility is to organize and manage all information related to a specific pet.

Owner Class: The Owner class represents a pet owner and manages their list of pets. It includes the add_pet() method, which allows owners to register new pets while preventing blank names and duplicate pet names. It also includes the rename() method, which updates the owner's name across their pets and existing feeding and veterinary records. Its main responsibility is to manage pet ownership information and maintain consistency throughout the system.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design changed during implementation when I added the Task and Scheduler classes. Initially, the application only managed basic pet information, feeding records, and veterinary visits. However, I needed a way to schedule and organize general pet care activities.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler mainly considers the scheduled date and time of each task, the pet associated with it, and whether the task has been completed. I focused on sorting tasks chronologically because I wanted users to easily understand which pet care activities needed to be completed first.

The scheduler can also filter tasks by pet name, date, and completion status. I prioritized these features because they were straightforward to implement and made the schedule easier to manage. More advanced constraints, such as task duration, owner availability, and priority levels, could be added in the future.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made with the Scheduler class is that it sorts tasks based on their scheduled date and time without checking for overlapping tasks. This makes the scheduling system simpler to implement and easier to manage, but it allows multiple tasks to be scheduled at the same time. In the future, I could improve the scheduler by adding task durations and checking for scheduling conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used an AI coding assistant throughout the project to help understand programming concepts, develop scheduling logic, and test my code. One of the most helpful features was the chat functionality, which allowed me to ask questions about specific methods and receive explanations with Python examples.

For example, I asked how to sort Task objects by their time attribute. The AI suggested using Python's sorted() function with a lambda expression. This helped me understand how to arrange tasks chronologically without changing the original list.

I also used AI to understand Streamlit's st.session_state and how to connect buttons in the user interface to methods in my classes.

Using separate chat sessions for different phases helped keep my work organized. I could focus on system design, implementation, and testing separately instead of mixing all my questions into one conversation. This also made it easier to review explanations related to each phase.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One example of evaluating an AI suggestion was when I asked about implementing Scheduler.sort_by_time(). The AI suggested creating a new method using sorted() and a lambda expression. However, my Scheduler class already had an organize_tasks() method that performed chronological sorting and included additional criteria for tasks scheduled at the same time.

Rather than immediately adding another method with similar functionality, I considered whether the new method was necessary. Keeping the existing method helped avoid duplicate code and made the Scheduler class easier to maintain.

I also tested the scheduling functionality through main.py by adding tasks out of chronological order and checking whether the output was sorted correctly. This helped me understand why AI-generated suggestions should be reviewed and tested instead of automatically accepted.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested several important functions of the Scheduler class, including task sorting, filtering, and completion tracking. I created sample pets and tasks in main.py and deliberately added the tasks out of chronological order to verify that the scheduler organized them correctly.

I also checked whether tasks could be filtered by pet name and completion status. These tests were important because they helped confirm that the scheduler could organize information correctly regardless of how the user entered it.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that the basic scheduling functions work correctly because the code is organized into separate methods and I was able to test the sorting and filtering logic.

However, I would still want to test more edge cases, such as multiple tasks scheduled at the same time, tasks with invalid information, and tasks scheduled on different dates. I would also test recurring tasks more thoroughly to make sure they generate their next scheduled occurrence correctly.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of the project I am most satisfied with is how the different classes work together. I was able to separate the application's data into individual classes and connect them through the Owner and Scheduler classes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the scheduling system by adding task durations, priority levels, and more advanced conflict detection. This would allow the application to create a more realistic daily schedule based on the owner's available time.

I would also consider adding permanent data storage so that pet information and scheduled tasks would remain available after the application closes.



**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important lesson I learned is that using AI does not replace the need to understand how a system is designed. Although AI helped me write and understand certain parts of the code, I still needed to decide which classes and methods belonged in the project and how they should interact.