from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Patient:
    """Patient data model"""
    id: int
    name: str
    date_of_birth: str
    contact_information: str
    medical_record_number: str
    category: str  # 'chronic' or 'acute'


@dataclass
class Doctor:
    """Doctor data model"""
    id: int
    name: str
    specialization: str
    credentials: str


@dataclass
class Consultation:
    """Patient consultation data model"""
    id: int
    patient_id: int
    doctor_id: int
    date: datetime
    notes: str
    diagnosis: str
    treatment_plan: str


@dataclass
class Appointment:
    """Appointment data model"""
    id: int
    patient_id: int
    doctor_id: int
    date_time: datetime
    status: str
    purpose: str
