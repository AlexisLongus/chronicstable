"""ChronicStable Doctor Chat Application.

A Streamlit-based app for doctors to manage patient information,
appointments, and interact with an LLM assistant.
"""
# Standard library imports
import os
import time
from datetime import datetime

# Third-party imports
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Local application imports
from services.ollama_service import OllamaService
from services.database_service import DatabaseService
from utils.context_builder import build_patient_context
from models.schema import Patient, Consultation, Appointment

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ChronicStable - Doctor Chat",
    page_icon="🏥",
    layout="wide",
)


@st.cache_resource
def init_services():
    """Initialize database and Ollama services.
    
    Returns:
        Tuple containing database_service and ollama_service instances.
    """
    # Initialize database service
    db_service = DatabaseService(
        os.getenv("DATABASE_URL", "sqlite:///chronicstable.db")
    )
    
    # Initialize Ollama service with AWS load balancer endpoint
    ollama_service = OllamaService(
        base_url=os.getenv("OLLAMA_API_URL", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "phi"),
    )
    
    return db_service, ollama_service


db_service, ollama_service = init_services()

# UI Components
st.sidebar.title("ChronicStable")
st.sidebar.subheader("Doctor's Assistant")

# Doctor selection (for demo purposes)
doctor_id = st.sidebar.selectbox(
    "Select Doctor",
    options=db_service.get_all_doctors(),
    format_func=lambda x: db_service.get_doctor_name(x)
)

# Patient category filter
patient_category_filter = st.sidebar.radio(
    "Filter Patients By Category",
    options=["all", "chronic", "acute"],
    horizontal=True,
    index=0,
    format_func=lambda x: x.capitalize()
)

# Patient selection with filtering
if patient_category_filter == "all":
    patient_list = db_service.get_patients_for_doctor(doctor_id)
else:
    patient_list = db_service.get_patients_by_category(
        doctor_id, patient_category_filter
    )

# Show count of patients by category
if patient_list:
    st.sidebar.caption(f"Showing {len(patient_list)} patient(s)")

patient_id = st.sidebar.selectbox(
    "Select Patient",
    options=patient_list,
    format_func=lambda x: (
        f"{db_service.get_patient_name(x)} "
        f"({db_service.get_patient_category(x).capitalize()})"
    )
)

# Tab navigation
tab1, tab2, tab3 = st.tabs(["Chat", "Patient History", "Schedule"])

# Tab 1: Chat Interface
with tab1:
    st.header("Doctor AI Assistant")
    
    # Display selected patient info
    if patient_id:
        patient = db_service.get_patient(patient_id)
        st.subheader(f"Patient: {patient.name}")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Create containers for messages and status
        message_container = st.container()
        status_container = st.container()
        
        # Display chat history in the message container
        with message_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Display the input at the bottom
        prompt = st.chat_input("Ask about your patient...")
        
        # Track if we're currently processing a response in the session state
        if "processing" not in st.session_state:
            st.session_state.processing = False
        
        # Process the user input
        if prompt and not st.session_state.processing:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Set the processing flag to prevent duplicate processing
            st.session_state.processing = True
            st.rerun()
        
        # Handle response generation
        if (st.session_state.processing and 
                len(st.session_state.messages) > 0 and 
                st.session_state.messages[-1]["role"] == "user"):
            # Get the last message from the user
            last_prompt = st.session_state.messages[-1]["content"]
            
            # Build context for the LLM with patient information
            context = build_patient_context(
                patient_id=patient_id,
                db_service=db_service
            )
            
            # Show thinking spinner while getting response
            with status_container:
                with st.spinner("Thinking..."):
                    response = ollama_service.get_response(last_prompt, context)
            
            # Add assistant message to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            # Reset the processing flag
            st.session_state.processing = False
            st.rerun()
    else:
        st.info("Please select a patient to start chatting")

# Tab 2: Patient History
with tab2:
    st.header("Patient Medical History")
    
    if patient_id:
        patient = db_service.get_patient(patient_id)
        st.subheader(f"Patient: {patient.name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Date of Birth:** {patient.date_of_birth}")
            st.markdown(
                f"**Medical Record Number:** {patient.medical_record_number}"
            )
        
        with col2:
            # Display current category with appropriate highlighting
            if patient.category == "chronic":
                st.markdown(
                    "**Patient Category:** <span style='background-color:#FFDDDD; "
                    "padding:3px 8px; border-radius:3px;'>⚠️ Chronic</span>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "**Patient Category:** <span style='background-color:#DDFFDD; "
                    "padding:3px 8px; border-radius:3px;'>✓ Acute</span>",
                    unsafe_allow_html=True
                )
            
            # Allow doctor to change patient category
            new_category = st.radio(
                "Change patient category:",
                options=["chronic", "acute"],
                horizontal=True,
                index=0 if patient.category == "chronic" else 1
            )
            
            if st.button("Update Category"):
                # Update patient category in database
                db_service.update_patient_category(patient_id, new_category)
                st.success(f"Patient category updated to {new_category}")
                # Add a small delay before reloading the page
                time.sleep(0.5)
                st.rerun()
        
        # Previous consultations
        st.subheader("Previous Consultations")
        consultations = db_service.get_patient_consultations(patient_id)
        
        if consultations:
            for consultation in consultations:
                with st.expander(
                    f"{consultation.date} - {consultation.diagnosis}"
                ):
                    st.markdown(f"**Notes:** {consultation.notes}")
                    st.markdown(
                        f"**Treatment Plan:** {consultation.treatment_plan}"
                    )
        else:
            st.info("No previous consultations found")
    else:
        st.info("Please select a patient to view history")

# Tab 3: Scheduling
with tab3:
    st.header("Appointment Scheduling")
    
    if patient_id:
        patient = db_service.get_patient(patient_id)
        st.subheader(f"Patient: {patient.name}")
        
        # Current appointments
        st.subheader("Current Appointments")
        appointments = db_service.get_patient_appointments(patient_id)
        
        if appointments:
            appointments_df = pd.DataFrame([
                {
                    "Date": apt.date_time.strftime("%Y-%m-%d %H:%M"),
                    "Purpose": apt.purpose,
                    "Status": apt.status
                } for apt in appointments
            ])
            
            st.dataframe(appointments_df)
        else:
            st.info("No appointments scheduled")
        
        # Schedule new appointment
        st.subheader("Schedule New Appointment")
        
        with st.form("schedule_form"):
            apt_date = st.date_input("Date")
            apt_time = st.time_input("Time")
            apt_purpose = st.text_input("Purpose")
            
            # Combine date and time
            apt_datetime = datetime.combine(apt_date, apt_time)
            
            submit = st.form_submit_button("Schedule Appointment")
            
            if submit:
                new_apt = db_service.create_appointment(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    date_time=apt_datetime,
                    purpose=apt_purpose,
                    status="scheduled"
                )
                
                st.success(
                    f"Appointment scheduled for "
                    f"{apt_datetime.strftime('%Y-%m-%d %H:%M')}"
                )
    else:
        st.info("Please select a patient to schedule appointments")


# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "ChronicStable - AI-powered assistant for healthcare professionals. "
    "All patient data is handled securely and confidentially."
)
