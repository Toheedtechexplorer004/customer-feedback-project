import sqlite3

#  Step 1: Database connection and cursor
conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

#  Step 2: Create raw_feedback table
cursor.execute("DROP TABLE IF EXISTS raw_feedback")
cursor.execute("""
CREATE TABLE raw_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedback_text TEXT
)
""")

#  Step 3: Insert raw feedback data directly from Python (10 lines)
raw_feedbacks = [
    "Name: Rahul, Age: 25, City: Delhi, Feedback: Great product!",
    "Name: Anjali, Age: 30, City: Mumbai, Feedback: Excellent service",
    "Name: Vikram, Age: 22, City: Jaipur, Feedback: Not satisfied",
    "Name: Sneha, Age: 28, City: Bangalore, Feedback: Loved it!",
    "Name: Aman, Age: 35, City: Pune, Feedback: Delivery was late but product was good",
    "Name: Neha, Age: 27, City: Hyderabad, Feedback: Very helpful support team",
    "Name: Ramesh, Age: 40, City: Chennai, Feedback: Poor packaging quality",
    "Name: Priya, Age: 23, City: Kolkata, Feedback: Totally satisfied with the experience",
    "Name: Karan, Age: 31, City: Ahmedabad, Feedback: Will definitely recommend to friends",
    "Name: Divya, Age: 29, City: Chandigarh, Feedback: Not happy with return policy"
]

for feedback in raw_feedbacks:
    cursor.execute("INSERT INTO raw_feedback (feedback_text) VALUES (?)", (feedback,))

conn.commit()

#  Step 4: Create structured_feedback table
cursor.execute("DROP TABLE IF EXISTS structured_feedback")
cursor.execute("""
CREATE TABLE structured_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    city TEXT,
    feedback TEXT
)
""")

#  Step 5: Use SQL to parse and insert structured data
cursor.execute("""
INSERT INTO structured_feedback (name, age, city, feedback)
SELECT
    TRIM(SUBSTR(feedback_text, INSTR(feedback_text, 'Name:') + 5, INSTR(feedback_text, ', Age:') - INSTR(feedback_text, 'Name:') - 5)),
    CAST(TRIM(SUBSTR(feedback_text, INSTR(feedback_text, 'Age:') + 4, INSTR(feedback_text, ', City:') - INSTR(feedback_text, 'Age:') - 4)) AS INTEGER),
    TRIM(SUBSTR(feedback_text, INSTR(feedback_text, 'City:') + 5, INSTR(feedback_text, ', Feedback:') - INSTR(feedback_text, 'City:') - 5)),
    TRIM(SUBSTR(feedback_text, INSTR(feedback_text, 'Feedback:') + 9))
FROM raw_feedback
""")

conn.commit()

#  Step 6: Show the structured table
print(" Final Structured Table:\n")
cursor.execute("SELECT * FROM structured_feedback")
rows = cursor.fetchall()

# Print neatly
print("{:<5} {:<10} {:<5} {:<12} {}".format("ID", "Name", "Age", "City", "Feedback"))
print("-" * 60)
for row in rows:
    print("{:<5} {:<10} {:<5} {:<12} {}".format(row[0], row[1], row[2], row[3], row[4]))

conn.close()
