# PawPal+

PawPal+ is a Streamlit pet-care tracker for managing multiple pets, logging
feeding times, and keeping veterinary checkup history. Each pet and care record
is associated with its owner.

## Run the app

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app keeps its data in the current Streamlit session. Add pets in the **Pets**
tab, record feedings in **Feeding**, and add checkups in **Vet history**.

## Data model

- `Owner` manages a list of pets and can add pets or update the owner's name.
- `Pet` stores its owner and has methods to add feeding records and vet visits.
- `FeedingRecord` and `VetVisit` both retain the pet and owner names alongside
  their care details.

The corresponding class diagram is in [diagrams/uml.mmd](diagrams/uml.mmd).

## Tests

Run the core data-model tests with:

```bash
pytest
```
