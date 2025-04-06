from app import app
from database import db

with app.app_context():
    db.drop_all()  # ✅ Deletes old tables
    db.create_all()  # ✅ Creates new tables matching this branch's schema
    print("✅ Database recreated successfully!")
