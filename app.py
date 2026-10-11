from datetime import date, datetime

import streamlit as st

from pawpal_system import Owner, Pet


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Keep your pets, feeding times, and veterinary checkups in one place.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner: Owner = st.session_state.owner
owner_name = st.sidebar.text_input("Owner name", value=owner.name, key="owner_name_input")
owner.rename(owner_name)

pets_tab, feeding_tab, vet_tab = st.tabs(["Pets", "Feeding", "Vet history"])

with pets_tab:
    st.subheader("Your pets")
    st.caption(f"Owner: {owner.name or 'Enter an owner name in the sidebar'}")

    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        add_pet = st.form_submit_button("Add pet")

    if add_pet:
        try:
            pet = owner.add_pet(pet_name, species)
            st.success(f"Added {pet.name}.")
        except ValueError as error:
            st.error(str(error))

    if owner.pets:
        for pet in owner.pets:
            st.markdown(f"**{pet.name}** · {pet.species} · Owner: {pet.owner_name}")
    else:
        st.info("No pets yet. Add your first pet above.")

with feeding_tab:
    st.subheader("Feeding log")
    if not owner.pets:
        st.info("Add a pet before recording a feeding.")
    else:
        with st.form("add_feeding_form", clear_on_submit=True):
            selected_pet: Pet = st.selectbox(
                "Pet", owner.pets, format_func=lambda pet: pet.name
            )
            feeding_date = st.date_input("Date", value=date.today())
            feeding_time = st.time_input(
                "Feeding time", value=datetime.now().time().replace(second=0, microsecond=0)
            )
            food = st.text_input("Food (optional)")
            add_feeding = st.form_submit_button("Record feeding")

        if add_feeding:
            fed_at = datetime.combine(feeding_date, feeding_time)
            selected_pet.add_feeding(fed_at, food)
            st.success(f"Recorded feeding for {selected_pet.name}.")

        feeding_rows = [
            {
                "Date and time": record.fed_at.strftime("%Y-%m-%d %I:%M %p"),
                "Pet": record.pet_name,
                "Owner": record.owner_name,
                "Food": record.food or "—",
            }
            for pet in owner.pets
            for record in pet.feedings
        ]
        if feeding_rows:
            st.dataframe(feeding_rows, hide_index=True, use_container_width=True)
        else:
            st.info("No feedings recorded yet.")

with vet_tab:
    st.subheader("Veterinary checkup history")
    if not owner.pets:
        st.info("Add a pet before recording a vet visit.")
    else:
        with st.form("add_vet_visit_form", clear_on_submit=True):
            selected_pet: Pet = st.selectbox(
                "Pet", owner.pets, format_func=lambda pet: pet.name
            )
            visit_date = st.date_input("Visit date", value=date.today(), key="visit_date")
            veterinarian = st.text_input("Veterinarian or clinic")
            notes = st.text_area("Checkup notes")
            add_visit = st.form_submit_button("Add vet visit")

        if add_visit:
            if not veterinarian.strip():
                st.error("Enter the veterinarian or clinic name.")
            else:
                selected_pet.add_vet_visit(visit_date, veterinarian, notes)
                st.success(f"Added vet visit for {selected_pet.name}.")

        visit_rows = [
            {
                "Date": visit.visit_date.isoformat(),
                "Pet": visit.pet_name,
                "Owner": visit.owner_name,
                "Veterinarian / clinic": visit.veterinarian,
                "Notes": visit.notes or "—",
            }
            for pet in owner.pets
            for visit in pet.vet_visits
        ]
        if visit_rows:
            st.dataframe(visit_rows, hide_index=True, use_container_width=True)
        else:
            st.info("No vet visits recorded yet.")
