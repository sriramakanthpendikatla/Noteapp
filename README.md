# NoteApp

A simple note-taking application built with Flask and SQLAlchemy.

## Local Development

### Prerequisites
- Python 3.9+
- SQLite (included with Python)

### Setup

1. **Set up a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Generate a secure secret key:
     ```bash
     python -c 'import secrets; print(secrets.token_hex(16))'
     ```
     Add the output to `SECRET_KEY` in `.env`

4. **Initialize the database**
   ```bash
   python -c "from website import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

5. **Run the development server**
   ```bash
   python main.py
   ```

6. **Access the app**
   - Open http://localhost:5000 in your browser

## Features

- User authentication (login/register)
- Create, view, and delete notes
- Responsive design
- Secure password hashing
