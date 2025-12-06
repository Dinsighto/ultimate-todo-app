from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
from models import db, Todo, User
from utils.email import send_reminder_email
import os

# Connect to same DB as app
db_url = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=8)  # Run daily at 8 AM UTC
def send_reminders():
    session = Session()
    tomorrow = date.today() + timedelta(days=1)
    
    # Query todos due tomorrow
    todos = session.query(Todo).join(User).filter(
        Todo.due_date == tomorrow,
        Todo.complete == False
    ).all()
    
    for todo in todos:
        send_reminder_email(todo.owner.email, todo.text, tomorrow)
    
    session.close()
    print("Daily reminders sent!")

if __name__ == '__main__':
    print("Starting email scheduler...")
    sched.start()