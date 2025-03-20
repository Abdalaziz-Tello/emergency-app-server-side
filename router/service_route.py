from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import EmergencyService, User
from auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from datetime import timedelta
from typing import Optional
from jose import jwt

router = APIRouter(prefix="/services", tags=["Emergency Services"])

def get_current_user(token: str, session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/")
def create_service(
    name: str, 
    latitude: float, 
    longitude: float, 
    priority: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = EmergencyService(
        name=name, 
        latitude=latitude, 
        longitude=longitude, 
        priority=priority,
        user_id=current_user.id
    )
    session.add(service)
    session.commit()
    return service

@router.get("/")
def list_services(session: Session = Depends(get_session)):
    return session.exec(select(EmergencyService)).all()

@router.get("/{service_id}")
def get_service(service_id: int, session: Session = Depends(get_session)):
    service = session.get(EmergencyService, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}")
def update_service(
    service_id: int, 
    status: str, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = session.get(EmergencyService, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this service")
    
    service.status = status
    session.add(service)
    session.commit()
    return {"message": "Service updated"}

@router.delete("/{service_id}")
def delete_service(
    service_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = session.get(EmergencyService, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this service")
    
    session.delete(service)
    session.commit()
    return {"message": "Service deleted"}
