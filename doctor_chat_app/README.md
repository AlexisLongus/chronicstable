# ChronicStable Doctor Chat App

A Streamlit-based chat application for doctors to interact with an LLM assistant for patient scheduling, consultation history, and medical information access.

## Features

- **AI-powered Chat Interface**: Using Ollama LLM through AWS load balancer
- **Patient Record Access**: View patient history and previous consultations
- **Appointment Scheduling**: Schedule and manage appointments
- **Context-Aware Responses**: LLM responses enhanced with patient context

## Requirements

- Python 3.9+
- Streamlit
- SQLAlchemy
- Requests
- Pandas
- Python-dotenv

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` with your configuration:
   ```
   cp .env.example .env
   ```
4. Update the `.env` file with your Ollama API URL and model name

## Running the Application

```bash
streamlit run app.py
```

## Development Workflow

### Updating the Application

1. **For Python Code Changes**:
   ```bash
   # Stop the current Streamlit app if it's running
   # Press Ctrl+C in the terminal
   
   # Start it again
   streamlit run app.py
   ```

2. **For Environment Changes**:
   ```bash
   # Stop the app
   # Press Ctrl+C
   
   # Restart the app
   streamlit run app.py
   ```

3. **For Database Schema Changes**:
   ```bash
   # Stop the app
   # Press Ctrl+C
   
   # Delete the existing database file
   rm chronicstable.db
   
   # Restart the app - it will recreate the database with new schema
   streamlit run app.py
   ```

4. **For New Dependencies**:
   ```bash
   # Install new dependencies
   pip install -r requirements.txt
   
   # Restart the app
   streamlit run app.py
   ```

5. **For Virtual Environment Updates**:
   ```bash
   # Deactivate current environment
   deactivate
   
   # Remove old environment
   rm -rf chronicstable_env/
   
   # Create new environment
   python3 -m venv chronicstable_env
   
   # Activate new environment
   source chronicstable_env/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the app
   streamlit run app.py
   ```

## Project Structure

```
doctor_chat_app/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .env.example            # Example environment variables
├── models/
│   └── schema.py           # Data models
├── services/
│   ├── database_service.py # Database interaction service
│   └── ollama_service.py   # Ollama LLM API service
└── utils/
    └── context_builder.py  # Context generation utilities
```

## Code Quality

The entire codebase follows [PEP 8](https://peps.python.org/pep-0008/) styling standards for Python, ensuring:

- Consistent code formatting and style
- Clear docstrings for all modules, classes, and functions
- Proper type hints
- Logical organization of imports
- Appropriate line length and indentation
- Descriptive variable and function names

This makes the code more readable, maintainable, and easier to extend.

## Usage

1. Select a doctor from the sidebar
2. Choose a patient to view their information
3. Use the tabs to:
   - Chat with the AI assistant about the patient
   - View patient history and previous consultations
   - Schedule and manage appointments

## Security Considerations

- This application handles sensitive medical data and should be used in a secure environment
- Ensure proper authentication and authorization in a production setting
- Do not expose the application to the public internet without proper security measures
- Consider encrypting the database in a production environment
