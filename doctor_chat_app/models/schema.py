"""Data models for ChronicStable Doctor Chat application.

Defines the core data structures used throughout the application.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Patient:
    """Patient data model."""
    id: int
    name: str
    date_of_birth: str
    contact_information: str
    medical_record_number: str
    category: str  # 'chronic' or 'acute'


@dataclass
class Doctor:
    """Doctor data model with professional information."""
    id: int
    name: str
    specialization: str
    credentials: str


@dataclass
class Consultation:
    """Patient consultation data model for medical visits."""
    id: int
    patient_id: int
    doctor_id: int
    date: datetime
    notes: str
    diagnosis: str
    treatment_plan: str


@dataclass
class Appointment:
    """Appointment data model for scheduling patient visits."""
    id: int
    patient_id: int
    doctor_id: int
    date_time: datetime
    status: str  # 'scheduled', 'completed', 'canceled'
    purpose: str
