from database import db
from app import app  # Import app AFTER db to avoid circular import

with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
