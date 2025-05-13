from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ## means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import datetime

auth = Blueprint('auth', __name__)

# Helper function to log each step with timestamp
def log_step(action, email=None, note_id=None):
    with open("log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if email:
            log_file.write(f"{timestamp} - {action} - Email: {email}\n")
        elif note_id:
            log_file.write(f"{timestamp} - {action} - Note ID: {note_id}\n")
        else:
            log_file.write(f"{timestamp} - {action}\n")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        log_step("Login attempt", email)  # Log login attempt

        user = User.query.filter_by(email=email).first()

        if user:
            log_step("Email found, checking password", email)  # Log email found

            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                log_step("Login successful", email)  # Log successful login
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                log_step("Incorrect password", email)  # Log incorrect password
        else:
            flash('Email does not exist.', category='error')
            log_step("Email does not exist", email)  # Log email not found

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    log_step("Logout", current_user.email)  # Log logout
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/notes')
@login_required
def notes():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=user_notes, user=current_user)

@auth.route('/add-note', methods=['POST'])
@login_required
def add_note():
    note_content = request.form.get('note')
    note_title = request.form.get('title')
    
    if note_content and note_title:
        new_note = Note(title=note_title, data=note_content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        log_step("Note saved", current_user.email, new_note.id)  # Log note save
        flash('Note saved successfully!', category='success')
        
        # Check if the request came from the notes page or home page
        referrer = request.referrer
        if referrer and '/notes' in referrer:
            return redirect(url_for('auth.notes'))
        else:
            return redirect(url_for('views.home'))
    else:
        flash('Note cannot be empty.', category='error')
        return redirect(url_for('auth.notes'))

@auth.route('/delete-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note_to_delete = Note.query.get_or_404(note_id)

    # Ensure the note belongs to the current user
    if note_to_delete.user_id == current_user.id:
        db.session.delete(note_to_delete)
        db.session.commit()

        log_step("Note deleted", current_user.email, note_id)  # Log note delete
        flash('Note deleted successfully!', category='success')
    else:
        flash('You cannot delete this note.', category='error')
    
    # Redirect back to the page they came from, defaulting to notes page
    referrer = request.referrer
    if referrer and '/notes' in referrer:
        return redirect(url_for('auth.notes'))
    else:
        return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        log_step("Sign-up attempt", email)  # Log sign-up attempt

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            log_step("Email already exists", email)  # Log existing email
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            log_step("Email length too short", email)  # Log short email
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
            log_step("First name length too short", email)  # Log short first name
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            log_step("Passwords don't match", email)  # Log passwords mismatch
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            log_step("Password too short", email)  # Log short password
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            log_step("Account created and logged in", email)  # Log successful account creation
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
