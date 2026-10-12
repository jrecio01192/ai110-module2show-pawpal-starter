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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made with the Scheduler class is that it sorts tasks based on their scheduled date and time without checking for overlapping tasks. This makes the scheduling system simpler to implement and easier to manage, but it allows multiple tasks to be scheduled at the same time. In the future, I could improve the scheduler by adding task durations and checking for scheduling conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
