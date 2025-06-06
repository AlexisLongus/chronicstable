"""Context building utilities for enhancing LLM responses.

Provides functions to build context from patient data and create system prompts.
"""
from datetime import datetime
from typing import Dict, Any, List

from services.database_service import DatabaseService


def build_patient_context(patient_id: int, db_service: DatabaseService) -> str:
    """Build context string for the LLM with relevant patient information.
    
    Args:
        patient_id: ID of the patient
        db_service: Database service instance
        
    Returns:
        A formatted context string containing patient information
    """
    patient = db_service.get_patient(patient_id)
    if not patient:
        return "No patient data available."
    
    consultations = db_service.get_patient_consultations(patient_id)
    appointments = db_service.get_patient_appointments(patient_id)
    
    # Build context with patient information
    context_parts = [
        "PATIENT INFORMATION:",
        f"Name: {patient.name}",
        f"Date of Birth: {patient.date_of_birth}",
        f"Medical Record Number: {patient.medical_record_number}",
        f"Contact: {patient.contact_information}",
        f"Category: {patient.category.capitalize()}",
        "\n"
    ]
    
    # Add consultation history
    context_parts.append("CONSULTATION HISTORY:")
    if consultations:
        # Limit to most recent 3 consultations
        for i, consultation in enumerate(consultations[:3]):
            doc_name = db_service.get_doctor_name(consultation.doctor_id)
            context_parts.extend([
                f"Consultation on {consultation.date.strftime('%Y-%m-%d')} "
                f"with {doc_name}:",
                f"Diagnosis: {consultation.diagnosis}",
                f"Notes: {consultation.notes}",
                f"Treatment: {consultation.treatment_plan}",
                "\n"
            ])
    else:
        context_parts.append("No previous consultations found.")
    
    # Add upcoming appointments
    context_parts.append("UPCOMING APPOINTMENTS:")
    upcoming_appointments = [
        apt for apt in appointments 
        if apt.date_time > datetime.now() and apt.status == "scheduled"
    ]
    
    if upcoming_appointments:
        for appointment in upcoming_appointments:
            doc_name = db_service.get_doctor_name(appointment.doctor_id)
            context_parts.append(
                f"{appointment.date_time.strftime('%Y-%m-%d %H:%M')} with "
                f"{doc_name}: {appointment.purpose}"
            )
    else:
        context_parts.append("No upcoming appointments.")
    
    return "\n".join(context_parts)


def build_system_prompt() -> str:
    """Build the system prompt for the LLM.
    
    Returns:
        A system prompt string with guidelines for the AI assistant
    """
    return """You are an AI assistant for doctors. You help doctors access and interpret 
patient information, schedule appointments, and provide relevant medical information. 
Always maintain a professional and compassionate tone. Do not provide medical 
advice unless it's based on the patient's consultation history.
Focus on helping the doctor manage their workflow and provide relevant patient context.

When providing information:
1. Be concise and relevant
2. Prioritize recent medical history
3. Highlight important health concerns
4. Reference specific dates and doctors when mentioning consultations
5. Keep patient information confidential
"""
