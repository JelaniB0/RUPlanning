from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Task, Class, Commitment
from pydantic import BaseModel
from datetime import date, time, timedelta

# Initialize FastAPI
app = FastAPI()

# Initialize database
init_db()

# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Pydantic Schemas
# ---------------------------

class TaskCreate(BaseModel):
    title: str
    description: str
    duration_est: int  # estimated duration in minutes
    deadline: date
    priority: int = 1

class ClassCreate(BaseModel):
    name: str
    day_of_week: str
    start_time: time
    end_time: time

class CommitmentCreate(BaseModel):
    title: str
    day_of_week: str
    start_time: time
    end_time: time

# ---------------------------
# Routes
# ---------------------------

# Root
@app.get("/")
def root():
    return {"message": "RUPlanning API is running!"}

# --- Tasks ---
@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        duration_est=task.duration_est,
        deadline=task.deadline,
        priority=task.priority,
        user_id=1   # hardcoded user for now
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# --- Classes ---
@app.post("/classes")
def create_class(new_class: ClassCreate, db: Session = Depends(get_db)):
    db_class = Class(
        user_id=1,
        name=new_class.name,
        day_of_week=new_class.day_of_week,
        start_time=new_class.start_time,
        end_time=new_class.end_time
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@app.get("/classes")
def read_classes(db: Session = Depends(get_db)):
    return db.query(Class).all()

# --- Commitments ---
@app.post("/commitments")
def create_commitment(new_commit: CommitmentCreate, db: Session = Depends(get_db)):
    db_commit = Commitment(
        user_id=1,
        title=new_commit.title,
        day_of_week=new_commit.day_of_week,
        start_time=new_commit.start_time,
        end_time=new_commit.end_time
    )
    db.add(db_commit)
    db.commit()
    db.refresh(db_commit)
    return db_commit

@app.get("/commitments")
def read_commitments(db: Session = Depends(get_db)):
    return db.query(Commitment).all()

@app.get("/schedule")
def generate_schedule(db: Session = Depends(get_db)):
    # Days of week (keys for our schedule)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    schedule = {day: [] for day in days}

    # --- 1. Add classes ---
    classes = db.query(Class).all()
    for c in classes:
        schedule[c.day_of_week].append({
            "type": "class",
            "title": c.name,
            "start": str(c.start_time),
            "end": str(c.end_time)
        })

    # --- 2. Add commitments ---
    commitments = db.query(Commitment).all()
    for cm in commitments:
        schedule[cm.day_of_week].append({
            "type": "commitment",
            "title": cm.title,
            "start": str(cm.start_time),
            "end": str(cm.end_time)
        })

    # --- 3. Add tasks (naive scheduling) ---
    tasks = db.query(Task).all()
    for t in tasks:
        # Example: just put tasks in 1-hour blocks starting Monday 9am
        # Later, you’ll replace with smarter logic
        day = "Mon"
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = start_time + timedelta(minutes=t.duration_est)

        schedule[day].append({
            "type": "task",
            "title": t.title,
            "start": start_time.strftime("%H:%M"),
            "end": end_time.strftime("%H:%M"),
            "deadline": str(t.deadline),
            "priority": t.priority
        })

    # --- 4. Sort each day's events by start time ---
    for day in days:
        schedule[day] = sorted(schedule[day], key=lambda e: e["start"])

    return schedule