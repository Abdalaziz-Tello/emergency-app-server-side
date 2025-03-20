from sqlmodel import SQLModel, create_engine, Session
from models import User, EmergencyService
from auth import hash_password
from sqlalchemy import select

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
    # Create a session to add initial data
    with Session(engine) as session:
        # Check if we already have data
        if session.exec(select(User)).first():
            return
            
        # Create initial admin user
        admin_user = User(
            username="admin",
            password=hash_password("admin123")
        )
        session.add(admin_user)
        session.commit()
        
        # Create some initial emergency services
        initial_services = [
            EmergencyService(
                name="Fire Department",
                latitude=40.7128,
                longitude=-74.0060,
                priority=3,
                user_id=admin_user.id
            ),
            EmergencyService(
                name="Police Department",
                latitude=40.7128,
                longitude=-74.0060,
                priority=3,
                user_id=admin_user.id
            ),
            EmergencyService(
                name="Ambulance Service",
                latitude=40.7128,
                longitude=-74.0060,
                priority=2,
                user_id=admin_user.id
            ),
            EmergencyService(
                name="Road Maintenance",
                latitude=40.7128,
                longitude=-74.0060,
                priority=1,
                user_id=admin_user.id
            )
        ]
        
        for service in initial_services:
            session.add(service)
        
        session.commit()

def get_session():
    with Session(engine) as session:
        yield session
