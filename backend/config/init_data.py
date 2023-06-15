import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

database_file = os.path.join(current_dir, '..', 'quizdata.db')

conn = sqlite3.connect(database_file)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        category TEXT,
        last_used TIMESTAMP
    )
''')

initial_data = [

    ('What is the capital of France?', 'Paris', 'Geography', '2022-06-01 10:30:00'),
    ('Who painted the Mona Lisa?', 'Leonardo da Vinci', 'Art', '2022-06-08 15:45:00'),
    ('What is the largest planet in our solar system?', 'Jupiter', 'Science', '2022-06-15 09:15:00'),
    ('What is the currency of Japan?', 'Japanese yen', 'Finance', '2022-06-22 14:20:00'),
    ('Who wrote the play "Romeo and Juliet"?', 'William Shakespeare', 'Literature', '2022-06-29 11:00:00'),
    ('What is the chemical symbol for gold?', 'Au', 'Science', '2022-07-06 16:30:00'),
    ('Who is the current President of the United States?', 'Joe Biden', 'Politics', '2022-07-13 08:45:00'),
    ('What is the tallest mountain in the world?', 'Mount Everest', 'Geography', '2022-07-20 13:10:00'),
    ('Who painted the ceiling of the Sistine Chapel?', 'Michelangelo', 'Art', '2022-07-27 10:15:00'),
    ('What is the formula for the area of a circle?', 'πr²', 'Mathematics', '2022-08-03 15:00:00'),
    ('Who is the author of "Pride and Prejudice"?', 'Jane Austen', 'Literature', '2022-08-10 09:20:00'),
    ('What is the largest ocean on Earth?', 'Pacific Ocean', 'Geography', '2022-08-17 12:45:00'),
    ('Who discovered penicillin?', 'Alexander Fleming', 'Science', '2022-08-24 14:30:00'),
    ('What is the capital of Spain?', 'Madrid', 'Geography', '2022-08-31 11:10:00'),
    ('Who painted "The Starry Night"?', 'Vincent van Gogh', 'Art', '2022-09-07 16:00:00'),
    ('What is the largest country in the world by land area?', 'Russia', 'Geography', '2022-09-14 08:30:00'),
    ('What is the symbol for the element oxygen?', 'O', 'Science', '2022-09-21 13:20:00'),
    ('Who is the current Prime Minister of the United Kingdom?', 'Boris Johnson', 'Politics', '2022-09-28 09:45:00'),
    ('Who wrote the novel "To Kill a Mockingbird"?', 'Harper Lee', 'Literature', '2022-10-05 14:15:00'),
    ('What is the formula for calculating density?', 'mass/volume', 'Physics', '2022-10-12 10:00:00'),
    ('Who is the artist of the famous painting "The Last Supper"?', 'Leonardo da Vinci', 'Art', '2022-10-19 15:30:00'),
    ('What is the largest desert in the world?', 'Sahara Desert', 'Geography', '2022-10-26 11:25:00'),
    ('Who proposed the theory of general relativity?', 'Albert Einstein', 'Science', '2022-11-02 14:50:00'),
    ('What is the capital of Australia?', 'Canberra', 'Geography', '2022-11-09 10:05:00'),
    ('Who painted the ceiling of the Sistine Chapel?', 'Michelangelo', 'Art', '2022-11-16 15:15:00'),
    ('What is the square root of 64?', '8', 'Mathematics', '2022-11-23 09:30:00'),
    ('Who is the author of "1984"?', 'George Orwell', 'Literature', '2022-11-30 13:40:00'),
    ('What is the deepest part of the ocean?', 'Mariana Trench', 'Geography', '2022-12-07 10:20:00'),
    ('Who discovered the theory of evolution?', 'Charles Darwin', 'Science', '2022-12-14 15:50:00'),
    ('What is the capital of Germany?', 'Berlin', 'Geography', '2022-12-21 11:15:00'),
    ('Who painted the "Mona Lisa"?', 'Leonardo da Vinci', 'Art', '2022-12-28 16:25:00'),
    ('What is the boiling point of water in Celsius?', '100 degrees', 'Science', '2023-01-04 09:55:00'),
    ('Who is the current Chancellor of Germany?', 'Angela Merkel', 'Politics', '2023-01-11 14:05:00'),
    ('Who wrote the play "Hamlet"?', 'William Shakespeare', 'Literature', '2023-01-18 10:10:00'),
    ('What is the formula for acceleration?', 'acceleration = change in velocity / time', 'Physics',
     '2023-01-25 15:35:00'),
    ('What is the largest river in the world?', 'Amazon River', 'Geography', '2023-02-01 11:40:00'),
    ('Who discovered the theory of gravity?', 'Isaac Newton', 'Science', '2023-02-08 09:15:00'),
    ('What is the capital of Brazil?', 'Brasília', 'Geography', '2023-02-15 14:30:00'),
    ('Who painted "The Persistence of Memory"?', 'Salvador Dalí', 'Art', '2023-02-22 10:50:00'),
    ('What is the value of pi (π)?', 'approximately 3.14159', 'Mathematics', '2023-03-01 15:20:00'),
    ('Who is the author of "The Great Gatsby"?', 'F. Scott Fitzgerald', 'Literature', '2023-03-08 11:25:00'),
    ('What is the largest island in the world?', 'Greenland', 'Geography', '2023-03-15 16:45:00'),
    ('Who discovered electricity?', 'Benjamin Franklin', 'Science', '2023-03-22 10:35:00'),
    ('What is the capital of Canada?', 'Ottawa', 'Geography', '2023-03-29 15:55:00'),
    ('Who painted "The Birth of Venus"?', 'Sandro Botticelli', 'Art', '2023-04-05 11:10:00'),
    ('What is the largest continent?', 'Asia', 'Geography', '2023-04-12 16:30:00'),
    ('Who proposed the theory of relativity?', 'Albert Einstein', 'Science', '2023-04-19 09:50:00'),
    ('What is the currency of Canada?', 'Canadian dollar', 'Finance', '2023-04-26 14:15:00'),
    ('Who is the current President of France?', 'Emmanuel Macron', 'Politics', '2023-05-03 10:25:00'),
    ('Who wrote the novel "Moby-Dick"?', 'Herman Melville', 'Literature', '2023-05-10 15:40:00'),
    ('What is the formula for calculating work?', 'work = force × distance', 'Physics', '2023-05-17 11:55:00'),
    ('What is the capital of Italy?', 'Rome', 'Geography', '2023-05-24 16:05:00'),
    ('Who painted "The Girl with a Pearl Earring"?', 'Johannes Vermeer', 'Art', '2023-05-31 10:45:00'),
    ('What is the largest waterfall in the world?', 'Angel Falls', 'Geography', '2023-06-07 15:10:00'),
    ('Who discovered the theory of relativity?', 'Albert Einstein', 'Science', '2023-06-14 11:15:00'),
    ('What is the capital of China?', 'Beijing', 'Geography', '2023-06-21 16:35:00'),
    ('Who painted the "The Night Watch"?', 'Rembrandt', 'Art', '2023-06-28 10:50:00'),
    ('What is the freezing point of water in Fahrenheit?', '32 degrees', 'Science', '2023-07-05 15:15:00'),
    ('Who is the current Prime Minister of Canada?', 'Justin Trudeau', 'Politics', '2023-07-12 11:20:00'),
    ('Who wrote the novel "The Catcher in the Rye"?', 'J.D. Salinger', 'Literature', '2023-07-19 16:40:00'),
    ('What is the formula for calculating power?', 'power = work/time', 'Physics', '2023-07-26 10:35:00'),
    ('What is the highest mountain in Africa?', 'Mount Kilimanjaro', 'Geography', '2023-08-02 15:55:00'),
    ('Who discovered the laws of motion?', 'Isaac Newton', 'Science', '2023-08-09 11:10:00'),
    ('What is the capital of India?', 'New Delhi', 'Geography', '2023-08-16 16:30:00'),
    ('Who painted "The Creation of Adam"?', 'Michelangelo', 'Art', '2023-08-23 10:50:00'),
    ('What is the value of the mathematical constant "e"?', 'approximately 2.71828', 'Mathematics',
     '2023-08-30 15:10:00'),
    ('Who is the author of "The Hobbit"?', 'J.R.R. Tolkien', 'Literature', '2023-09-06 11:25:00'),
    ('What is the deepest lake in the world?', 'Lake Baikal', 'Geography', '2023-09-13 16:45:00'),
    ('Who discovered the theory of electromagnetism?', 'James Clerk Maxwell', 'Science', '2023-09-20 10:35:00'),
    ('What is the capital of Russia?', 'Moscow', 'Geography', '2023-09-27 15:55:00'),
    ('Who painted "The Scream"?', 'Edvard Munch', 'Art', '2023-10-04 11:10:00'),
    ('What is the formula for calculating kinetic energy?', 'kinetic energy = 0.5 × mass × velocity²', 'Physics',
     '2023-10-11 16:30:00'),
    ('What is the longest river in South America?', 'Amazon River', 'Geography', '2023-10-18 10:45:00'),
    ('Who discovered the theory of evolution by natural selection?', 'Charles Darwin', 'Science', '2023-10-25 15:10:00'),
    ('What is the capital of South Africa?', 'Pretoria', 'Geography', '2023-11-01 11:25:00'),
    ('Who painted "Guernica"?', 'Pablo Picasso', 'Art', '2023-11-08 16:45:00'),
    ('What is the boiling point of water in Kelvin?', '273.15 Kelvin', 'Science', '2023-11-15 10:35:00'),
    ('Who is the current Prime Minister of India?', 'Narendra Modi', 'Politics', '2023-11-22 15:55:00'),
    ('Who wrote the novel "The Lord of the Rings"?', 'J.R.R. Tolkien', 'Literature', '2023-11-29 11:10:00'),
    ('What is the formula for calculating electric current?', 'current = charge/time', 'Physics', '2023-12-06 16:30:00'),
    ('What is the highest waterfall in the United States?', 'Yosemite Falls', 'Geography', '2023-12-13 10:45:00'),
    ('Who discovered the laws of gravitation?', 'Isaac Newton', 'Science', '2023-12-20 15:10:00'),
    ('What is the capital of Egypt?', 'Cairo', 'Geography', '2023-12-27 11:25:00'),
    ('Who painted "The Persistence of Memory"?', 'Salvador Dalí', 'Art', '2024-01-03 16:45:00'),
    ('What is the value of the mathematical constant "π"?', 'approximately 3.14159', 'Mathematics','2024-01-10 10:35:00'),
    ('Who is the author of "The Odyssey"?', 'Homer', 'Literature', '2024-01-17 15:55:00'),
    ('What is the longest river in Europe?', 'Volga River', 'Geography', '2024-01-24 11:10:00'),
    ('Who discovered the theory of relativity?', 'Albert Einstein', 'Science', '2024-01-31 16:30:00'),
    ('What is the capital of Mexico?', 'Mexico City', 'Geography', '2024-02-07 10:45:00'),
    ('Who painted "The Starry Night"?', 'Vincent van Gogh', 'Art', '2024-02-14 15:10:00'),
    ('What is the freezing point of water in Kelvin?', '273.15 Kelvin', 'Science', '2024-02-21 11:25:00'),
    ('Who is the current Prime Minister of Japan?', 'Yoshihide Suga', 'Politics', '2024-02-28 16:45:00'),
    ('Who wrote the play "Macbeth"?', 'William Shakespeare', 'Literature', '2024-03-06 10:35:00'),
    ('What is the formula for calculating potential energy?', 'potential energy = mass × gravity × height', 'Physics',
     '2024-03-13 15:55:00'),
    ('What is the largest lake in North America?', 'Lake Superior', 'Geography', '2024-03-20 11:10:00'),
    ('Who discovered the laws of motion?', 'Isaac Newton', 'Science', '2024-03-27 16:30:00'),
    ('What is the capital of Argentina?', 'Buenos Aires', 'Geography', '2024-04-03 10:45:00'),
    ('Who painted "The Last Supper"?', 'Leonardo da Vinci', 'Art', '2024-04-10 15:10:00'),
    ('What is the boiling point of water in Fahrenheit?', '212 degrees', 'Science', '2024-04-17 11:25:00'),
    ('Who is the current President of the United States?', 'Joe Biden', 'Politics', '2024-04-24 16:45:00')

]
cursor.executemany('INSERT INTO questions (question, answer, category, last_used) VALUES (?, ?, ?, ?)', initial_data)

conn.commit()

conn.close()
