from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from typing import List, Optional, Dict, Any

# Database models
Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    credentials = Column(String(100))
    
    # Relationships
    consultations = relationship("Consultation", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(String(10))
    contact_information = Column(String(100))
    medical_record_number = Column(String(20), unique=True)
    
    # Relationships
    consultations = relationship("Consultation", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(DateTime, default=datetime.now)
    notes = Column(Text)
    diagnosis = Column(String(100))
    treatment_plan = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date_time = Column(DateTime)
    status = Column(String(20))  # scheduled, completed, canceled
    purpose = Column(String(200))
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class DatabaseService:
    """
    Service for interacting with the database
    """
    
    def __init__(self, database_url: str):
        """
        Initialize the database service
        
        Args:
            database_url: URL for the database connection
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Initialize with sample data if empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Add sample data if the database is empty"""
        session = self.Session()
        
        # Check if we already have data
        if session.query(Doctor).count() == 0:
            # Create sample doctors
            doctor1 = Doctor(name="Dr. Jane Smith", specialization="Cardiology", credentials="MD, FACC")
            doctor2 = Doctor(name="Dr. Robert Johnson", specialization="Family Medicine", credentials="MD")
            doctor3 = Doctor(name="Dr. Maria Garcia", specialization="Endocrinology", credentials="MD, PhD")
            doctor4 = Doctor(name="Dr. David Chen", specialization="Neurology", credentials="MD, FAAN")
            session.add_all([doctor1, doctor2, doctor3, doctor4])
            session.commit()
            
            # Create sample patients with more detailed information
            patient1 = Patient(
                name="John Doe", 
                date_of_birth="1980-05-15", 
                contact_information="john.doe@email.com, (555) 123-4567", 
                medical_record_number="MRN12345"
            )
            patient2 = Patient(
                name="Sarah Williams", 
                date_of_birth="1992-09-23", 
                contact_information="sarah.w@email.com, (555) 987-6543", 
                medical_record_number="MRN67890"
            )
            patient3 = Patient(
                name="Michael Rodriguez", 
                date_of_birth="1975-12-10", 
                contact_information="m.rodriguez@email.com, (555) 555-5555", 
                medical_record_number="MRN24680"
            )
            patient4 = Patient(
                name="Emily Johnson", 
                date_of_birth="1988-03-27", 
                contact_information="emily.j@email.com, (555) 222-3333", 
                medical_record_number="MRN13579"
            )
            session.add_all([patient1, patient2, patient3, patient4])
            session.commit()
            
            # Create comprehensive consultation history
            # Patient 1 - John Doe - Cardiac patient
            consultations1 = [
                Consultation(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date=datetime(2024, 11, 10),
                    notes="Initial visit. Patient reports occasional chest pain during physical exertion. Family history of coronary artery disease. Father had MI at 58. Blood pressure 145/90. BMI 29.4.",
                    diagnosis="Suspected coronary artery disease",
                    treatment_plan="Ordered ECG and stress test. Prescribed atorvastatin 20mg daily. Recommended lifestyle changes including Mediterranean diet and moderate exercise."
                ),
                Consultation(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date=datetime(2025, 1, 15),
                    notes="Follow-up visit. Stress test reveals moderate ischemia. Patient reports improved symptoms with medication but still experiences occasional angina with exertion. Blood pressure improved to 138/85.",
                    diagnosis="Stable angina",
                    treatment_plan="Continued current medication. Added metoprolol 25mg twice daily. Scheduled coronary angiogram for further evaluation."
                ),
                Consultation(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date=datetime(2025, 3, 5),
                    notes="Post-angiogram follow-up. Angiogram showed 70% stenosis in LAD. Stent placed successfully. Patient reports no chest pain since procedure. Blood pressure 132/80.",
                    diagnosis="Coronary artery disease, status post stent placement",
                    treatment_plan="Continue atorvastatin and metoprolol. Added clopidogrel 75mg daily for 12 months. Cardiac rehabilitation recommended 3x weekly."
                ),
                Consultation(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date=datetime(2025, 5, 20),
                    notes="Patient presented with chest pain and shortness of breath. States he missed 3 doses of medication last week. ECG shows no acute changes. Blood pressure elevated at 152/92.",
                    diagnosis="Angina pectoris",
                    treatment_plan="Reinforced medication adherence. Prescribed nitroglycerin sublingual for acute episodes. Follow-up in 2 weeks."
                )
            ]
            
            # Patient 2 - Sarah Williams - Generally healthy
            consultations2 = [
                Consultation(
                    patient_id=patient2.id,
                    doctor_id=doctor2.id,
                    date=datetime(2024, 8, 12),
                    notes="Annual physical examination. Patient reports good overall health with occasional headaches after long work hours. No significant findings on physical exam. BMI 23.1, BP 118/78.",
                    diagnosis="Healthy check-up, tension headaches",
                    treatment_plan="Recommended regular breaks when working, proper hydration. Follow up in 12 months or as needed."
                ),
                Consultation(
                    patient_id=patient2.id,
                    doctor_id=doctor2.id,
                    date=datetime(2025, 2, 3),
                    notes="Patient presented with fever, cough, and congestion for 5 days. Temp 100.4°F. Lungs clear. Rapid COVID and flu tests negative.",
                    diagnosis="Upper respiratory tract infection, likely viral",
                    treatment_plan="Symptomatic treatment with acetaminophen, fluids, and rest. Return if symptoms worsen or persist beyond 10 days."
                )
            ]
            
            # Patient 3 - Michael Rodriguez - Diabetes patient
            consultations3 = [
                Consultation(
                    patient_id=patient3.id,
                    doctor_id=doctor3.id,
                    date=datetime(2024, 7, 22),
                    notes="Initial visit for diabetes management. Patient reports polyuria, polydipsia, and unintentional weight loss of 15 lbs over 3 months. Random blood glucose 278 mg/dL. HbA1c 9.2%. Family history of T2DM.",
                    diagnosis="Type 2 Diabetes Mellitus, newly diagnosed",
                    treatment_plan="Started on metformin 500mg BID with meals. Diabetes education provided. Referral to nutritionist. Recommended daily blood glucose monitoring."
                ),
                Consultation(
                    patient_id=patient3.id,
                    doctor_id=doctor3.id,
                    date=datetime(2024, 10, 18),
                    notes="Follow-up visit. Patient reports improved symptoms. Has lost 5 more pounds intentionally through diet changes. Blood glucose readings averaging 160-180 mg/dL. HbA1c improved to 8.1%.",
                    diagnosis="Type 2 Diabetes Mellitus, improving",
                    treatment_plan="Increased metformin to 1000mg BID. Continued lifestyle modifications. Lab work ordered for kidney function and lipid panel."
                ),
                Consultation(
                    patient_id=patient3.id,
                    doctor_id=doctor3.id,
                    date=datetime(2025, 1, 25),
                    notes="Quarterly follow-up. Patient doing well with medication and diet compliance. Blood glucose readings now averaging 120-140 mg/dL. HbA1c 7.2%. Mild neuropathic symptoms noted in feet.",
                    diagnosis="Type 2 Diabetes Mellitus with early peripheral neuropathy",
                    treatment_plan="Continued current medication. Added alpha-lipoic acid supplement. Referred to podiatry for comprehensive foot evaluation."
                ),
                Consultation(
                    patient_id=patient3.id,
                    doctor_id=doctor1.id,
                    date=datetime(2025, 4, 30),
                    notes="Cardiology consultation for diabetes and newly detected hypertension. ECG normal. BP 148/88. Patient reports occasional palpitations.",
                    diagnosis="Essential hypertension, Type 2 Diabetes Mellitus",
                    treatment_plan="Started on lisinopril 10mg daily. Recommended DASH diet in addition to diabetic diet. 24-hour Holter monitor ordered for palpitations."
                )
            ]
            
            # Patient 4 - Emily Johnson - Neurological issues
            consultations4 = [
                Consultation(
                    patient_id=patient4.id,
                    doctor_id=doctor4.id,
                    date=datetime(2024, 9, 5),
                    notes="New patient consultation for recurring headaches. Patient describes intense, throbbing pain predominantly on right side with photophobia and nausea, lasting 4-12 hours. Occurring 2-3 times monthly for past year. Family history of migraines.",
                    diagnosis="Migraine without aura",
                    treatment_plan="Prescribed sumatriptan 50mg for acute attacks. Recommended headache diary to identify triggers. Discussed stress reduction techniques."
                ),
                Consultation(
                    patient_id=patient4.id,
                    doctor_id=doctor4.id,
                    date=datetime(2024, 12, 12),
                    notes="Follow-up for migraines. Frequency increased to weekly episodes. Headache diary reveals correlation with menstrual cycle and lack of sleep. Sumatriptan provides relief but patient concerned about usage frequency.",
                    diagnosis="Migraine without aura, increasing frequency",
                    treatment_plan="Added propranolol 40mg daily for prevention. Continued acute treatment with sumatriptan. Ordered brain MRI to rule out secondary causes."
                ),
                Consultation(
                    patient_id=patient4.id,
                    doctor_id=doctor4.id,
                    date=datetime(2025, 2, 28),
                    notes="MRI results normal. Patient reports 40% reduction in headache frequency with propranolol. Sleep improved with recommended sleep hygiene practices. Still has severe episodes around menstruation.",
                    diagnosis="Migraine without aura, menstrually-related",
                    treatment_plan="Continued propranolol. Added naproxen sodium 500mg BID for 5 days around expected menstruation. Recommended CoQ10 supplement."
                ),
                Consultation(
                    patient_id=patient4.id,
                    doctor_id=doctor2.id,
                    date=datetime(2025, 5, 15),
                    notes="Patient seen for upper respiratory symptoms and concern about impact on migraines. Reports nasal congestion, sore throat for 3 days. No fever. Rapid strep test negative.",
                    diagnosis="Viral upper respiratory infection, Migraine disorder (stable)",
                    treatment_plan="Supportive care for URI. Continue current migraine management. Contact neurology if significant headache exacerbation occurs."
                )
            ]
            
            # Add all consultations
            all_consultations = consultations1 + consultations2 + consultations3 + consultations4
            session.add_all(all_consultations)
            
            # Create sample appointments
            appointments = [
                Appointment(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date_time=datetime(2025, 6, 10, 14, 30),
                    status="scheduled",
                    purpose="Follow-up appointment for angina"
                ),
                Appointment(
                    patient_id=patient2.id,
                    doctor_id=doctor2.id,
                    date_time=datetime(2025, 6, 15, 10, 0),
                    status="scheduled",
                    purpose="Annual check-up"
                ),
                Appointment(
                    patient_id=patient3.id,
                    doctor_id=doctor3.id,
                    date_time=datetime(2025, 6, 12, 11, 15),
                    status="scheduled",
                    purpose="Quarterly diabetes monitoring"
                ),
                Appointment(
                    patient_id=patient4.id,
                    doctor_id=doctor4.id,
                    date_time=datetime(2025, 6, 18, 9, 30),
                    status="scheduled",
                    purpose="Migraine therapy evaluation"
                ),
                Appointment(
                    patient_id=patient1.id,
                    doctor_id=doctor1.id,
                    date_time=datetime(2025, 8, 5, 13, 0),
                    status="scheduled",
                    purpose="Cardiac stress test follow-up"
                ),
                Appointment(
                    patient_id=patient3.id,
                    doctor_id=doctor3.id,
                    date_time=datetime(2025, 9, 10, 15, 45),
                    status="scheduled",
                    purpose="HbA1c check and medication review"
                )
            ]
            session.add_all(appointments)
            
            session.commit()
        
        session.close()
    
    def get_all_doctors(self) -> List[int]:
        """Get IDs of all doctors"""
        session = self.Session()
        doctors = session.query(Doctor.id).all()
        session.close()
        return [doctor[0] for doctor in doctors]
    
    def get_doctor_name(self, doctor_id: int) -> str:
        """Get name of doctor by ID"""
        session = self.Session()
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        session.close()
        return doctor.name if doctor else "Unknown Doctor"
    
    def get_patients_for_doctor(self, doctor_id: int) -> List[int]:
        """Get IDs of patients associated with a doctor"""
        session = self.Session()
        
        # Get unique patient IDs from consultations and appointments
        patient_ids_from_consultations = session.query(Consultation.patient_id).filter(
            Consultation.doctor_id == doctor_id
        ).distinct().all()
        
        patient_ids_from_appointments = session.query(Appointment.patient_id).filter(
            Appointment.doctor_id == doctor_id
        ).distinct().all()
        
        # Combine and deduplicate
        all_patient_ids = set([p[0] for p in patient_ids_from_consultations + patient_ids_from_appointments])
        
        session.close()
        return list(all_patient_ids)
    
    def get_patient_name(self, patient_id: int) -> str:
        """Get name of patient by ID"""
        session = self.Session()
        patient = session.query(Patient).filter(Patient.id == patient_id).first()
        session.close()
        return patient.name if patient else "Unknown Patient"
    
    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Get patient details by ID"""
        session = self.Session()
        patient = session.query(Patient).filter(Patient.id == patient_id).first()
        session.close()
        return patient
    
    def get_patient_consultations(self, patient_id: int) -> List[Consultation]:
        """Get consultations for a patient"""
        session = self.Session()
        consultations = session.query(Consultation).filter(
            Consultation.patient_id == patient_id
        ).order_by(Consultation.date.desc()).all()
        session.close()
        return consultations
    
    def get_patient_appointments(self, patient_id: int) -> List[Appointment]:
        """Get appointments for a patient"""
        session = self.Session()
        appointments = session.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).order_by(Appointment.date_time.asc()).all()
        session.close()
        return appointments
    
    def create_appointment(self, patient_id: int, doctor_id: int, date_time: datetime, 
                          purpose: str, status: str = "scheduled") -> Appointment:
        """Create a new appointment"""
        session = self.Session()
        
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date_time=date_time,
            purpose=purpose,
            status=status
        )
        
        session.add(appointment)
        session.commit()
        
        # Refresh to get the ID
        session.refresh(appointment)
        
        # Close session and return
        result = appointment
        session.close()
        return result
    
    def create_consultation(self, patient_id: int, doctor_id: int, notes: str, 
                           diagnosis: str, treatment_plan: str) -> Consultation:
        """Create a new consultation"""
        session = self.Session()
        
        consultation = Consultation(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=datetime.now(),
            notes=notes,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan
        )
        
        session.add(consultation)
        session.commit()
        
        # Refresh to get the ID
        session.refresh(consultation)
        
        # Close session and return
        result = consultation
        session.close()
        return result
