import resend
import os

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_reminder_email(user_email, todo_text, due_date):
    """Send email reminder 24h before due date"""
    params = {
        "from": "Todo App <noreply@yourapp.com>",
        "to": [user_email],
        "subject": f"Reminder: '{todo_text}' due tomorrow!",
        "html": f"""
        <h2>⏰ Todo Reminder</h2>
        <p><strong>{todo_text}</strong> is due on {due_date.strftime('%Y-%m-%d')}.</p>
        <p><a href="{os.environ.get('APP_URL', 'https://your-app.onrender.com')}">Open App</a></p>
        <p>Stay productive! 🚀</p>
        """
    }
    try:
        resend.Emails.send(params)
        print(f"Reminder sent to {user_email}")
    except Exception as e:
        print(f"Email error: {e}")