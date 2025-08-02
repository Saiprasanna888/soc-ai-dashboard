import pandas as pd
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "sololeveling6868@gmail.com"          # Put your test Gmail here
    from_password = "wnit gcdo wdax bonm"          # Your password or app password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, from_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)


data = pd.read_csv('incident_event_log.csv')
print(data.head())
print("\nColumn names are:")
print(data.columns)

# Update this with the correct column name from your dataset!
sorted_alerts = data.sort_values('priority', ascending=False)
print(sorted_alerts.head(10))

def triage_alert(row):
    priority_str = str(row['priority']).lower()  # convert to lowercase for easier matching
    if '1' in priority_str or 'high' in priority_str:
        return 'High Priority'
    elif '2' in priority_str or 'medium' in priority_str:
        return 'Medium Priority'
    elif '3' in priority_str or 'moderate' in priority_str:
        return 'Low Priority'
    else:
        return 'Low Priority'  # default fallback

# Apply the function to your dataframe
data['triage_label'] = data.apply(triage_alert, axis=1)

# Display the first 20 rows of priority and triage label
print(data[['priority', 'triage_label']].head(20))

# Optional: print alerts labeled as High Priority
high_priority_alerts = data[data['triage_label'] == 'High Priority']
for i, alert in high_priority_alerts.iterrows():
    print(f"ALERT: High priority incident found - {alert['number']} with priority {alert['priority']}")


# Filter High Priority alerts and limit to top 3 for testing email notifications
alerts_to_notify = data[data['triage_label'] == 'High Priority'].head(3)

recipient_email = "sololeveling6868@gmail.com"  # Change to your target email address

if len(alerts_to_notify) == 0:
    print("No High Priority alerts found.")
else:
    print(f"\nSending emails for {len(alerts_to_notify)} high priority alerts...\n")
    for i, alert in alerts_to_notify.iterrows():
        subject = f"URGENT: High Priority Incident {alert['number']}"
        body = (
            f"Incident {alert['number']} requires immediate attention.\n"
            f"Priority: {alert['priority']}\n"
            f"State: {alert['incident_state']}\n"
            f"Opened At: {alert['opened_at']}\n"
            f"Assigned To: {alert.get('assigned_to', 'N/A')}\n"
            f"Impact: {alert.get('impact', 'N/A')}\n"
        )
        send_email(subject, body, recipient_email)
