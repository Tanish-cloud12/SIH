from flask import Flask, request, jsonify, render_template, session
import random
import copy

app = Flask(__name__)
# A secret key is required for Flask session management
app.secret_key = 'a-very-secret-key-for-anuvad-chatbot'

# =================================================================
# ALL DATA IS NOW STORED ON THE BACKEND
# =================================================================

# teachers
all_teachers = [
    "VIJEYA SINGH", "NAVEEN JAGLAN", "NEERAJ KUMAR", "RITU SIBAL", "VINEET KUMAR", "HARSH YADAV", "T N SHUKLA",
    "MANISHA MALIK", "SUBHODIP SAHA", "AMIT SANGER", "RICHA", "PRAVEEN SAROHA", "ROHIT KUMAR RAI", "ALOK PRAKASH MITTAL",
    "RATNESHWAR KUMAR RATNESH", "PURRNIMA SINGH", "MANISHA", "SANDEEP SINGH CHAUHAN", "SACHIN SHARMA", "VINAMRITA SINGH",
    "SEEMA THANEY", "RAHUL KUMAR", "SHIKHA BANSAL", "SARIKA", "JYOTI YADAV", "PIYUSH KUMAR YADAV", "ANIMESH MALVIYA",
    "NEETU RAJ BHARTI", "ANURAG GAUR", "ISHA PANDEY", "DEEPAK CHAND", "RASHMI RANI", "HARSHALI VERMA", "MANJU KUMARI",
    "NIKITA", "PRERNA SAHARIYA", "JEHOVA JIRE L. HMAR", "BHAVNESH KUMAR", "NAVNEETA VERMA", "GAURAV PANDEY",
    "ANJALI SINGH", "SATYA PRAKASH SINGH", "NIDHI AGRAWAL", "NAVEEN", "HARSHMANI YADAV", "ALOK AGRAWAL", "SHIVANI ANAND",
    "UMER ASHRAF", "SWATI ARUN SABBANWAR", "PRIYA BISHT", "JAINENDER KUMAR SINGH", "ANMOL AWASTHI", "SHEELA RANI",
    "SAMIKSHA DABAS", "SONAL AGGARWAL", "SHRUTI", "SEEMA SINGH", "ARVIND MEENA", "SWETA GUPTA", "SANDEEP KUMAR",
    "RISHABH VATS", "GURBAKSH", "JITENDER", "RAJANISH KUMAR RAI", "SAPNA VERMA", "MANYA", "SUMITA DAHIYA",
    "TANUSHREE CHOUDHARY", "ABDUL BASIT KHAN", "NANCY GUPTA", "SANJAY GUPTA", "NAVEEN GUPTA", "JUGAL BORI",
    "SUMAN BHAGCHANDANI", "RAKESH KUMAR", "ABHISHEK TEVATIA", "PRADEEP KUMAR CHASWAL", "MANOJ SOOD",
    "SWAPNIL LAXMAN SONAWANE", "SRISHTI GUPTA", "ANJANA SARKAR", "SUSHMITA", "SOMYA CHARAN PAHADI", "LEENA AGGARWAL",
    "SATADRU CHATTERJEE", "POOJA BHARDWAJ", "SANJEEVE THAKUR", "RAJVEER SINGH YADUVANSHI", "KUNWAR SINGH", "PURNIMA JAIN",
    "DEEPAK KUMAR GUPTA"
]

# Subject
subjects_year_2 = [
    "Biochemistry", "Numerical Methods and Computation", "Engineering Mathematics", "Operating Systems",
    "Software Engineering", "Mathematics For Communication & Signal Processing", "Optimization Principles and Techniques",
    "Mathematics For Machine Learning", "Data Structures & Algorithms", "Structural Analysis", "Database Management System",
    "Signals and Systems For Geo-Informatics", "Signals and Systems", "Manufacturing Processes-l", "Cell Biology",
    "Geographical Information System", "Design and Analysis of Algorithms", "Applied Linear Algebra",
    "Probability Theory and Random Process", "Electrical Circuit Theory and Analysis", "Power Apparatus",
    "Probability and Stochastic Processes", "Strength of Materials", "Chemical Engineering Principles",
    "Advanced Surveying", "Digital Logic Design", "Computer Architecture & Organization", "Electrical Machines-l",
    "Electronic Instrumentation", "Computer System Organization", "Thermal Engineering-I", "Thermal Engineering-II",
    "Microelectronics Circuits and Applications", "Microbiology", "Engineering Geology and Geomorphology",
    "Probability & Statistics", "Microprocessor and Microcontrollers", "Digital Circuits and Systems",
    "Computational Methods In Electrical Engineering", "Advance Programming", "Fluid Mechanics & Machines",
    "Building Materials and Construction", "Fundamentals of Electrical Engineering"
]

subjects_year_3 = [
    "Cloud Computing", "CMOS Digital Integrated Circuits", "Composite Materials", "Condition Assessment of Structures",
    "Cryptography and Computer Security", "Data Handeling Visualization and Tools", "Data Science",
    "Database Management System", "Design for Manufacture", "Digital Image Processing", "Discrete Time Systems",
    "Environmental Impact Assessment", "Fundamental of Robotics", "Industrial IoT", "Materials Science and Metallurgy",
    "Object Oriented Databases", "Operations Research", "Opto Electronics and Optical Communication",
    "Programming Data Structures and Algorithms Using Python", "Smart Sensors", "Virus: An Invisible Enemy",
    "Advanced Machining Processes", "Data Warehouse and Data mining", "Digital System Design using Verilog",
    "Environmental Biotechnology", "Biomedical Instrumentation", "Environmental Engineering", "Industrial Control Systems",
    "Information Theory and Secrecy Analysis", "Internal Combustion Engines", "Multimodal Transportation Infrastructure",
    "Open Channel Flow", "Optical Fiber Communication", "Probability and Statistics", "Product Design and Development",
    "Renewable Energy Sources", "Smart Sensor Technologies for IoT Applications", "Analog Integrated Circuits",
    "Automobile Engineering", "Basics of Electrical Vehicles", "Bioinformatics", "CAD & Product Design",
    "Computer Networks", "Data Mining", "DSP Algorithms and Architecture", "Embedded Systems", "Environmental Engineering",
    "Digital Signal Processing", "Distributed Computing", "Geoinformatics for Natural Disasters",
    "Industrial Systems and Automation", "Microprocessor based System Design", "Modern Control Theory",
    "RF and Microwave Engineering", "Theory of Computation", "Wireless and Mobile Communication",
    "Advance Computer Networks", "Digital Communication", "Concrete Technology",
    "Fundamentals & Operations of Electric Vehicles", "Global Navigation Satellite Systems", "IoT System Architecture",
    "Mechanical Design", "Number Theory and Cryptography", "Operating Systems", "Power System Analysis",
    "Principle of Compiler Construction", "Process Dynamics and Control", "Recombinant DNA Technology",
    "Sensors and Communication Systems", "Software Engineering", "Antenna Design for IoT Applications",
    "Artificial Intelligence", "Artificial Intelligence and Machine Learning", "Communication and Optical Instrumentation",
    "Control Systems", "Electrochemical Processes and Energy Systems", "Enzyme Technology",
    "Game Theory and Applications", "Geoinformatics for Natural Dissasters", "Geotechnical and Foundation Engineering",
    "Industrial Engineering", "Soft Computing", "VLSI Design", "Biochemical Engineering", "Cloud Computing",

    "Computer Vision", "Electric and Hybrid Vehicle Technology", "Electric Drives", "Embedded System Design",
    "Financial Engineering", "Information and Data Security", "Mobile Computing",
    "Principles of Sensors and Data Acquisition", "Quantity Survey and Cost Estimation", "Robotics",
    "Web mapping and Web-GIS", "Exploration of Classical Indian Philosophical Heritage"
]

subjects_year_4 = [
    "Epigenetics", "Intelligent Computing", "Multimedia Security and Forensics", "Multimedia Communication",
    "Underwater Communication", "ADVANCED ENERGY MANAGEMENT", "Optical Sensors", "Machine learning Applications in Robotics",
    "Stegnography and Digital Watermarking", "Pattern Analysis and Recommender Systems",
    "Alternative Fuels & Emission Control in Automotives", "Business Intelligence", "Idea To Business Model",
    "Mobile Computing", "Repair, Strengthening and Retrofitting of Structures", "Design for Manufacture",
    "Lifestyle Diseases", "Advanced Topics in Data Processing", "Graph theory and Algorithms",
    "Software Project Management", "Speech and Audio Signal Processing", "ENERGY STORAGE SYSTEMS", "Biomedical Imaging",
    "Cyber Laws", "Computational Data Science", "Reverse Engineering", "Health Informatics",
    "Electric Vehicle Charging Technology", "Web Technology", "Structural Dynamics", "Public Health Management",
    "Responsible Al", "Information Retrieval", "Service oriented architecture", "Cryptography",
    "Optical Wireless Communication", "Power System Operation & Control",
    "Machine Learning For Healthcare Deep and Reinforcement Networks", "Smart Materials in Robotics", "Internet of Things",
    "Computer Networks", "Unsaturated Soil Mechanics", "Smart Sensor Technologies for IoT Applications",
    "Biological Waste Treatment", "Current Trends in Software Development", "Knowledge Based System",
    "Video Signal Processing and Applications", "Multivariable Control Theory And Applications", "Green Computing",
    "Laser Materials Processing", "Computer Vision", "Big Data Analytics", "Models for Air and Water Quality",
    "Biosafety and Hazard Management", "Low-Voltage and Low-power VLSI Design", "Classical Optimization Techniques",
    "Software Re-use and Re-engineering", "Biometrics"
]

timetable = {
    "1": {  # Year 1
        "CSE-1": {
            "Monday": [
                {"time": "8:00-10:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "11:00-12:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVEEN JAGLAN"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "4:00-6:00", "subject": "Fundamentals of Electrical Engineering (PRACTICAL)", "teacher": "VINEET KUMAR"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Quantum Physics", "teacher": "HARSH YADAV"},
                {"time": "1:00-2:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "T N SHUKLA"},
                {"time": "4:00-6:00", "subject": "Computer Programming (PRACTICAL)", "teacher": "RITU SIBAL"}
            ],
            "Wednesday": [
                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVEEN JAGLAN"},
                {"time": "2:00-3:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "T N SHUKLA"},
                {"time": "3:00-4:00", "subject": "Quantum Physics", "teacher": "HARSH YADAV"}
            ],
            "Thursday": [
                {"time": "12:00-2:00", "subject": "Basics of Electronics & Communication Engineering (PRACTICAL)", "teacher": "NAVEEN JAGLAN"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "4:00-6:00", "subject": "Quantum Physics (PRACTICAL)", "teacher": "HARSH YADAV"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVEEN JAGLAN"},
                {"time": "2:00-3:00", "subject": "Quantum Physics", "teacher": "HARSH YADAV"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "T N SHUKLA"},
                {"time": "4:00-6:00", "subject": "Mathematics-I  (TUTORIAL)", "teacher": "NEERAJ KUMAR"}
            ]
        },
        "CSE-2": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "MANISHA MALIK"},
                {"time": "11:00-1:00", "subject": "Fundamentals of Electrical Engineering (PRACTICAL)", "teacher": "SUBHODIP SAHA"},
                {"time": "2:00-3:00", "subject": "Quantum Physics", "teacher": "AMIT SANGER"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": "RICHA"}

            ],
            "Tuesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "RICHA"},
                {"time": "11:00-12:00", "subject": "Quantum Physics", "teacher": "AMIT SANGER"},
                {"time": "12:00-2:00", "subject": "Basics of Electronics & Communication Engineering (PRACTICAL)", "teacher": "ROHIT KUMAR RAI"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK PRAKASH MITTAL"},
                {"time": "4:00-5:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "RATNESHWAR KUMAR RATNESH"}
            ],
            "Wednesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "MANISHA MALIK"},
                {"time": "2:00-4:00", "subject": "Quantum Physics (PRACTICAL)", "teacher": "AMIT SANGER"},
                {"time": "4:00-6:00", "subject": "Mathematics-I (TUTORIAL)", "teacher": "MANISHA MALIK"}
            ],
            "Thursday": [
                {"time": "10:00-11:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK PRAKASH MITTAL"},
                {"time": "11:00-12:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "RATNESHWAR KUMAR RATNESH"},
                {"time": "12:00-1:00", "subject": "Computer Programming", "teacher": "RICHA"},
                {"time": "1:00-2:00", "subject": "Quantum Physics", "teacher": "AMIT SANGER"}
            ],
            "Friday": [

                {"time": "10:00-11:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "ALOK PRAKASH MITTAL"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK PRAKASH MITTAL"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "MANISHA MALIK"},
                {"time": "2:00-4:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "PURRNIMA SINGH"}
            ]
        },
        "CSAI-1": {
            "Monday": [
                {"time": "8:00-10:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "MANISHA"},
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": " SANDEEP SINGH CHAUHAN"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "SACHIN SHARMA"},
                {"time": "4:00-6:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": " VINAMRITA SINGH"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "1:00-2:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"}

            ],
            "Wednesday": [
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "SACHIN SHARMA"},
                {"time": "11:00-12:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": " SANDEEP SINGH CHAUHAN"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "MANISHA"},
                {"time": "2:00-3:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SACHIN SHARMA"}
            ],
            "Thursday": [
                {"time": "12:00-2:00", "subject": "Fundamentals of Electrical Engineering (PRACTICAL)", "teacher": "MANISHA"},
                {"time": "2:00-3:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": " SANDEEP SINGH CHAUHAN"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "SACHIN SHARMA"},
                {"time": "4:00-6:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "RITU SIBAL"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "MANISHA"},
                {"time": "2:00-3:00", "subject": "Computer Programming", "teacher": "RITU SIBAL"},
                {"time": "3:00-4:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"},
                {"time": "4:00-6:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": " SANDEEP SINGH CHAUHAN"}
            ]
        },
        "CSAI-2": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"},
                {"time": "11:00-1:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": "RAHUL KUMAR"},
                {"time": "2:00-3:00", "subject": "Computer Programming", "teacher": "SHIKHA BANSAL"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "SARIKA"}

            ],
            "Tuesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "SARIKA"},
                {"time": "11:00-12:00", "subject": "Computer Programming", "teacher": "SHIKHA BANSAL"},
                {"time": "12:00-2:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "JYOTI YADAV"},
                {"time": "3:00-4:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"},
                {"time": "4:00-5:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PIYUSH KUMAR YADAV"}
            ],
            "Wednesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "1:00-2:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"},
                {"time": "2:00-4:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "ANIMESH MALVIYA"},
                {"time": "4:00-6:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": " NEETU RAJ BHARTI"}
            ],
            "Thursday": [
                {"time": "10:00-11:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PIYUSH KUMAR YADAV"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "SARIKA"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": "SHIKHA BANSAL"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SARIKA"}
            ],
            "Friday": [

                {"time": "10:00-11:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PIYUSH KUMAR YADAV"},
                {"time": "11:00-12:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"},
                {"time": "1:00-2:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"}
            ]
        },
        "IT-1": {
            "Monday": [
                {"time": "8:00-10:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "11:00-12:00", "subject": "Quantum Physics", "teacher": "ANURAG GAUR"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "JYOTI YADAV"},
                {"time": "1:00-2:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "ISHA PANDEY"},
                {"time": "4:00-6:00", "subject": "Computer Programming (PRACTICAL)", "teacher": " DEEPAK CHAND"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": " RASHMI RANI"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": " DEEPAK CHAND"},
                {"time": "4:00-6:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": "NEETU RAJ BHARTI"}
            ],
            "Wednesday": [
                {"time": "10:00-11:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "ISHA PANDEY"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "JYOTI YADAV"},
                {"time": "12:00-1:00", "subject": "Quantum Physics", "teacher": "ANURAG GAUR"},
                {"time": "2:00-3:00", "subject": "Computer Programming", "teacher": " DEEPAK CHAND"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": " RASHMI RANI"}
            ],
            "Thursday": [
                {"time": "12:00-2:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": "RAHUL KUMAR"},
                {"time": "2:00-3:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "JYOTI YADAV"},
                {"time": "3:00-4:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "ISHA PANDEY"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": " RASHMI RANI"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Quantum Physics", "teacher": "ANURAG GAUR"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": " RASHMI RANI"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": " DEEPAK CHAND"},
                {"time": "4:00-6:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "HARSHALI VERMA"}
            ]
        },
        "IT-2": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "VINEET KUMAR"},
                {"time": "11:00-1:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "DEEPAK CHAND"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": "SARIKA"},
                {"time": "3:00-4:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"}

            ],
            "Tuesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "10:00-11:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "SARIKA"},
                {"time": "12:00-2:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": " MANJU KUMARI"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": "DEEPAK CHAND"},
                {"time": "4:00-5:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"}
            ],
            "Wednesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "1:00-2:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "VINEET KUMAR"},
                {"time": "2:00-4:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "DEEPAK CHAND"},
                {"time": "4:00-6:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": " NIKITA"}
            ],
            "Thursday": [
                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "DEEPAK CHAND"},
                {"time": "11:00-12:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"},
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "SEEMA THANEY"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "SARIKA"}
            ],
            "Friday": [

                {"time": "10:00-11:00", "subject": "Quantum Physics", "teacher": " VINAMRITA SINGH"},
                {"time": "11:00-12:00", "subject": "Computer Programming", "teacher": "DEEPAK CHAND"},
                {"time": "1:00-2:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "VINEET KUMAR"},
                {"time": "2:00-4:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": "PRERNA SAHARIYA"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SARIKA"}
            ]
        },
        "CSDS": {
            "Monday": [
                {"time": "8:00-10:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "11:00-12:00", "subject": "Computer Programming", "teacher": " RICHA"},
                {"time": "12:00-1:00", "subject": "Quantum Physics", "teacher": "JEHOVA JIRE L. HMAR"},
                {"time": "1:00-2:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "BHAVNESH KUMAR"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": " SACHIN SHARMA"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVNEETA VERMA"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": " SACHIN SHARMA"},
                {"time": "4:00-6:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "GAURAV PANDEY"}
            ],
            "Wednesday": [
                {"time": "10:00-11:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "BHAVNESH KUMAR"},
                {"time": "11:00-12:00", "subject": "Quantum Physics", "teacher": "JEHOVA JIRE L. HMAR"},
                {"time": "12:00-1:00", "subject": "Computer Programming", "teacher": " RICHA"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": " SACHIN SHARMA"},
                {"time": "3:00-4:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVNEETA VERMA"}
            ],
            "Thursday": [
                {"time": "12:00-2:00", "subject": "Computer Programming(PRACTICAL)", "teacher": " ANJALI SINGH"},
                {"time": "2:00-3:00", "subject": "Quantum Physics", "teacher": "JEHOVA JIRE L. HMAR"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "BHAVNESH KUMAR"},
                {"time": "4:00-6:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": "SATYA PRAKASH SINGH"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Computer Programming", "teacher": " RICHA"},
                {"time": "2:00-3:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "NAVNEETA VERMA"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": " SACHIN SHARMA"},
                {"time": "4:00-6:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": "JEHOVA JIRE L. HMAR"}
            ]
        },
        "ITNS": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Quantum Physics", "teacher": "NIDHI AGRAWAL"},
                {"time": "11:00-1:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "NAVEEN"},
                {"time": "2:00-3:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK AGRAWAL"}

            ],
            "Tuesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "10:00-11:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK AGRAWAL"},
                {"time": "11:00-12:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "12:00-2:00", "subject": "Computer Programming", "teacher": "SHIKHA BANSAL"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "4:00-5:00", "subject": "Computer Programming", "teacher": "SHIVANI ANAND"}
            ],
            "Wednesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "1:00-2:00", "subject": "Quantum Physics", "teacher": "NIDHI AGRAWAL"},
                {"time": "2:00-4:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": " UMER ASHRAF"},
                {"time": "4:00-6:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": "NIDHI AGRAWAL"}
            ],
            "Thursday": [
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "11:00-12:00", "subject": "Computer Programming", "teacher": "SHIVANI ANAND"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "ALOK AGRAWAL"},
                {"time": "1:00-2:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "NAVEEN"}
            ],
            "Friday": [

                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "SHIVANI ANAND"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "1:00-2:00", "subject": "Quantum Physics", "teacher": "NIDHI AGRAWAL"},
                {"time": "2:00-4:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "SWATI ARUN SABBANWAR"}
            ]
        },
        "MAC": {
            "Monday": [
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": "ANMOL AWASTHI"},
                {"time": "4:00-6:00", "subject": "Basics of Electronics & Communication Engineering(PRACTICAL)", "teacher": "SHEELA RANI"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "PRIYA BISHT"},
                {"time": "12:00-1:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"},
                {"time": "2:00-4:00", "subject": "Quantum Physics (PRACTICAL)", "teacher": "SAMIKSHA DABAS"}
            ],
            "Wednesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "ANMOL AWASTHI"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"},
                {"time": "2:00-3:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "3:00-4:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"}
            ],
            "Thursday": [
                {"time": "10:00-12:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "3:00-4:00", "subject": "Computer Programming", "teacher": "ANMOL AWASTHI"}
            ],
            "Friday": [
                {"time": "10:00-12:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "ANMOL AWASTHI"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"},
                {"time": "2:00-3:00", "subject": "Quantum Physics", "teacher": "RAHUL KUMAR"},
                {"time": "3:00-4:00", "subject": "Basics of Electronics & Communication Engineering", "teacher": "HARSHMANI YADAV"},
                {"time": "4:00-6:00", "subject": "Mathematics-I  (TUTORIAL)", "teacher": "SONAL AGGARWAL"}
            ]
        },
        "ECE-1": {
            "Monday": [
                {"time": "8:00-10:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "12:00-1:00", "subject": "Computer Programming", "teacher": "SEEMA SINGH"},
                {"time": "1:00-2:00", "subject": "WAVE AND OPTICS", "teacher": "SAMIKSHA DABAS"},
                {"time": "4:00-6:00", "subject": "Engineering Graphics & CAD(PRACTICAL)", "teacher": "ARVIND MEENA"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-1", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "1:00-2:00", "subject": "Engineering Graphics & CAD", "teacher": "SANDEEP KUMAR"},
                {"time": "4:00-6:00", "subject": "WAVE AND OPTICS(PRACTICAL)", "teacher": "RAHUL KUMAR"}
            ],
            "Wednesday": [
                {"time": "10:00-11:00", "subject": "WAVE AND OPTICS", "teacher": "SAMIKSHA DABAS"},
                {"time": "11:00-12:00", "subject": "Computer Programming", "teacher": "SEEMA SINGH"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "2:00-3:00", "subject": "Engineering Graphics & CAD", "teacher": "SANDEEP KUMAR"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SHRUTI"}
            ],
            "Thursday": [
                {"time": "12:00-2:00", "subject": "Quantum Physics(PRACTICAL)", "teacher": "RAHUL KUMAR"},
                {"time": "2:00-3:00", "subject": "Computer Programming", "teacher": "SEEMA SINGH"},
                {"time": "3:00-4:00", "subject": "WAVE AND OPTICS", "teacher": "SAMIKSHA DABAS"},
                {"time": "4:00-6:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "ALOK AGRAWAL"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "2:00-3:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "3:00-4:00", "subject": "Engineering Graphics & CAD", "teacher": "SANDEEP KUMAR"},
                {"time": "4:00-6:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "RISHABH VATS"}
            ]
        },
        "ECE-2": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Computer Programming", "teacher": "GURBAKSH"},
                {"time": "11:00-1:00", "subject": "Engineering Graphics & CAD(PRACTICAL)", "teacher": "JITENDER"},
                {"time": "2:00-3:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"},
                {"time": "3:00-4:00", "subject": "WAVE AND OPTICS", "teacher": "MANJU KUMARI"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "RAJANISH KUMAR RAI"}

            ],
            "Tuesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "10:00-11:00", "subject": "WAVE AND OPTICS", "teacher": "MANJU KUMARI"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"},
                {"time": "3:00-4:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"},
                {"time": "4:00-5:00", "subject": "Mathematics-I", "teacher": "RAJANISH KUMAR RAI"}
            ],
            "Wednesday": [
                {"time": "10:00-12:00", "subject": "VA Batch-3", "teacher": "PRAVEEN SAROHA"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": "GURBAKSH"},
                {"time": "2:00-4:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "SAPNA VERMA"},
                {"time": "4:00-6:00", "subject": "Computer Programming(PRACTICAL)", "teacher": "MANYA"}
            ],
            "Thursday": [
                {"time": "10:00-11:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "RAJANISH KUMAR RAI"},
                {"time": "12:00-1:00", "subject": "WAVE AND OPTICS", "teacher": "MANJU KUMARI"},
                {"time": "1:00-2:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "PRIYA BISHT"}
            ],
            "Friday": [

                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "RAJANISH KUMAR RAI"},
                {"time": "11:00-12:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"},
                {"time": "1:00-2:00", "subject": "Computer Programming", "teacher": "GURBAKSH"},
                {"time": "2:00-4:00", "subject": "WAVE AND OPTICS(PRACTICAL)", "teacher": "MANJU KUMARI"}
            ]
        },
        "ICE-1": { # Renamed from 1CE-1 to match getReplies
            "Monday": [
                {"time": "11:00-12:00", "subject": "Basics of Mechanical Engineering", "teacher": "SANJAY GUPTA"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "SUMITA DAHIYA"},
                {"time": "1:00-2:00", "subject": "English", "teacher": "TANUSHREE CHOUDHARY"},
                {"time": "4:00-6:00", "subject": "Basic Civil Engineering(TUTORIAL)", "teacher": "ABDUL BASIT KHAN"}
            ],
            "Tuesday": [
                {"time": "12:00-1:00", "subject": "Environment Science and Green Chemistry", "teacher": "NANCY GUPTA"},
                {"time": "1:00-2:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "4:00-6:00", "subject": "English(PRACTICAL)", "teacher": "TANUSHREE CHOUDHARY"}
            ],
            "Wednesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "English", "teacher": "TANUSHREE CHOUDHARY"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "SUMITA DAHIYA"},
                {"time": "12:00-1:00", "subject": "Basics of Mechanical Engineering", "teacher": "SANJAY GUPTA"},
                {"time": "2:00-3:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "3:00-4:00", "subject": "Environment Science and Green Chemistry", "teacher": "NANCY GUPTA"}
            ],
            "Thursday": [
                {"time": "10:00-12:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-2:00", "subject": "Basics of Mechanical Engineering(PRACTICAL)", "teacher": "SANJAY GUPTA"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": "SUMITA DAHIYA"},
                {"time": "3:00-4:00", "subject": "English", "teacher": "TANUSHREE CHOUDHARY"},
                {"time": "4:00-6:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "NANCY GUPTA"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Basics of Mechanical Engineering", "teacher": "SANJAY GUPTA"},
                {"time": "2:00-3:00", "subject": "Environment Science and Green Chemistry", "teacher": "NANCY GUPTA"},
                {"time": "3:00-4:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "4:00-6:00", "subject": "Mathematics-I  (TUTORIAL)", "teacher": "SUMITA DAHIYA"}
            ]
        },
        "ICE-2": { # Renamed from 1CE-2 to match getReplies
            "Monday": [
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"},
                {"time": "11:00-1:00", "subject": "Basic Civil Engineering(PRACTICAL)", "teacher": "ABDUL BASIT KHAN"},
                {"time": "2:00-3:00", "subject": "Environment Science and Green Chemistry", "teacher": "JUGAL BORI"},
                {"time": "3:00-4:00", "subject": "English", "teacher": "SUMAN BHAGCHANDANI"}
            ],
            "Tuesday": [
                {"time": "10:00-11:00", "subject": "English", "teacher": "SUMAN BHAGCHANDANI"},
                {"time": "11:00-12:00", "subject": "Environment Science and Green Chemistry", "teacher": "JUGAL BORI"},
                {"time": "2:00-3:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "3:00-4:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"}
            ],
            "Wednesday": [
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"},
                {"time": "2:00-4:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "JUGAL BORI"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "NAVEEN GUPTA"}
            ],
            "Thursday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "11:00-12:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "12:00-1:00", "subject": "English", "teacher": "SUMAN BHAGCHANDANI"},
                {"time": "1:00-2:00", "subject": "Environment Science and Green Chemistry", "teacher": "JUGAL BORI"},
                {"time": "4:00-6:00", "subject": "Basics of Mechanical Engineering(TUTORIAL)", "teacher": "ABHISHEK TEVATIA"}

            ],
            "Friday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "11:00-12:00", "subject": "Basic Civil Engineering ", "teacher": "ABDUL BASIT KHAN"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"},
                {"time": "2:00-4:00", "subject": "English(PRACTICAL)", "teacher": "PRADEEP KUMAR CHASWAL"}
            ]
        },
        "EE-1": {
            "Monday": [
                {"time": "11:00-12:00", "subject": "Basic Civil Engineering", "teacher": "MANOJ SOOD"},
                {"time": "12:00-1:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "SUMITA DAHIYA"},
                {"time": "4:00-6:00", "subject": "Environment Science and Green Chemistry", "teacher": "SWAPNIL LAXMAN SONAWANE"}
            ],
            "Tuesday": [
                {"time": "12:00-1:00", "subject": "English", "teacher": "SRISHTI GUPTA"},
                {"time": "1:00-2:00", "subject": "Environment Science and Green Chemistry", "teacher": "SWAPNIL LAXMAN SONAWANE"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SUMITA DAHIYA"}
            ],
            "Wednesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "SUMITA DAHIya"},
                {"time": "11:00-12:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "12:00-1:00", "subject": "Basic Civil Engineering ", "teacher": "MANOJ SOOD"},
                {"time": "2:00-3:00", "subject": "Environment Science and Green Chemistry", "teacher": "SWAPNIL LAXMAN SONAWANE"},
                {"time": "3:00-4:00", "subject": "English", "teacher": "SRISHTI GUPTA"}
            ],
            "Thursday": [
                {"time": "10:00-12:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-2:00", "subject": "Basic Civil Engineering(PRACTICAL)", "teacher": "MANOJ SOOD"},
                {"time": "2:00-3:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "3:00-4:00", "subject": "Mathematics-I  (TUTORIAL)", "teacher": "SUMITA DAHIYA"},
                {"time": "4:00-6:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "ANJANA SARKAR"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Basic Civil Engineering ", "teacher": "MANOJ SOOD"},
                {"time": "2:00-3:00", "subject": "English", "teacher": "SRISHTI GUPTA"},
                {"time": "3:00-4:00", "subject": "Environment Science and Green Chemistry", "teacher": "SWAPNIL LAXMAN SONAWANE"},
                {"time": "4:00-6:00", "subject": "Basics of Mechanical Engineering(TUTORIAL)", "teacher": "RAKESH KUMAR"}
            ]
        },
        "EE-2": {
            "Monday": [
                {"time": "10:00-11:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "11:00-1:00", "subject": "Environment Science and Green Chemistry", "teacher": "SUSHMITA"},
                {"time": "2:00-3:00", "subject": "English", "teacher": "SOMYA CHARAN PAHADI"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "4:00-6:00", "subject": "Basic Civil Engineering(PRACTICAL)", "teacher": "MANOJ SOOD"}
            ],
            "Tuesday": [
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "11:00-12:00", "subject": "English", "teacher": "SOMYA CHARAN PAHADI"},
                {"time": "2:00-3:00", "subject": "Environment Science and Green Chemistry", "teacher": "SUSHMITA"},
                {"time": "3:00-4:00", "subject": "Basic Civil Engineering(PRACTICAL)", "teacher": "MANOJ SOOD"}
            ],
            "Wednesday": [
                {"time": "1:00-2:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"},
                {"time": "2:00-4:00", "subject": "English(PRACTICAL)", "teacher": "SOMYA CHARAN PAHADI"},
                {"time": "4:00-6:00", "subject": "Basics of Mechanical Engineering(TUTORIAL)", "teacher": "RAKESH KUMAR"}
            ],
            "Thursday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Environment Science and Green Chemistry", "teacher": "SUSHMITA"},
                {"time": "11:00-12:00", "subject": "Basic Civil Engineering", "teacher": "MANOJ SOOD"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "JAINENDER KUMAR SINGH"},
                {"time": "1:00-2:00", "subject": "English", "teacher": "SOMYA CHARAN PAHADI"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "JAINENDER KUMAR SINGH"}

            ],
            "Friday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Basic Civil Engineering", "teacher": "MANOJ SOOD"},
                {"time": "11:00-12:00", "subject": "Environment Science and Green Chemistry", "teacher": "SUSHMITA"},
                {"time": "1:00-2:00", "subject": "Basics of Mechanical Engineering", "teacher": "RAKESH KUMAR"}
            ]
        },
        "EVDT": {
            "Monday": [
                {"time": "11:00-12:00", "subject": "Environment Science and Green Chemistry", "teacher": "LEENA AGGARWAL"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "1:00-2:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"},
                {"time": "4:00-6:00", "subject": "English(PRACTICAL)", "teacher": "SATADRU CHATTERJEE"}
            ],
            "Tuesday": [
                {"time": "10:00-12:00", "subject": "Engineering Graphics & CAD(PRACTICAL)", "teacher": "ARVIND MEENA"},
                {"time": "12:00-1:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "2:00-3:00", "subject": "English", "teacher": "SATADRU CHATTERJEE"}
            ],
            "Wednesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"},
                {"time": "11:00-12:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "12:00-1:00", "subject": "Environment Science and Green Chemistry", "teacher": "LEENA AGGARWAL"},
                {"time": "2:00-3:00", "subject": "English", "teacher": "SATADRU CHATTERJEE"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"}
            ],
            "Thursday": [
                {"time": "10:00-12:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-2:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "LEENA AGGARWAL"},
                {"time": "2:00-4:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "SWETA GUPTA"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "NEERAJ KUMAR"}
            ],
            "Friday": [
                {"time": "12:00-1:00", "subject": "Environment Science and Green Chemistry", "teacher": "LEENA AGGARWAL"},
                {"time": "2:00-3:00", "subject": "Mathematics-I", "teacher": "NEERAJ KUMAR"},
                {"time": "3:00-4:00", "subject": "English", "teacher": "SATADRU CHATTERJEE"},
                {"time": "4:00-5:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "SWETA GUPTA"},
                {"time": "5:00-6:00", "subject": "Engineering Graphics & CAD", "teacher": "ARVIND MEENA"}
            ]
        },
        "ME-1": {
            "Monday": [
                {"time": "11:00-12:00", "subject": "English", "teacher": "POOJA BHARDWAJ"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": " ALOK PRAKASH MITTAL"},
                {"time": "1:00-2:00", "subject": "Environment Science and Green Chemistry", "teacher": "SANJEEVE THAKUR"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "SHRUTI"}
            ],
            "Tuesday": [
                {"time": "12:00-1:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "RAJVEER SINGH YADUVANSHI"},
                {"time": "1:00-2:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "4:00-5:00", "subject": "Environment Science and Green Chemistry", "teacher": "SANJEEVE THAKUR"},
                {"time": "5:00-6:00", "subject": "Fundamentals of Electrical Engineering", "teacher": " ALOK PRAKASH MITTAL"}
            ],
            "Wednesday": [
                {"time": "8:00-10:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-12:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": " ALOK PRAKASH MITTAL"},
                {"time": "12:00-1:00", "subject": "English", "teacher": "POOJA BHARDWAJ"}
            ],
            "Thursday": [
                {"time": "10:00-12:00", "subject": "VA Batch-2", "teacher": "VIJEYA SINGH"},
                {"time": "12:00-2:00", "subject": "English(PRACTICAL)", "teacher": "POOJA BHARDWAJ"},
                {"time": "2:00-3:00", "subject": "Environment Science and Green Chemistry", "teacher": "SANJEEVE THAKUR"},
                {"time": "3:00-4:00", "subject": "Fundamentals of Electrical Engineering", "teacher": " ALOK PRAKASH MITTAL"},
                {"time": "4:00-5:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "5:00-6:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "RAJVEER SINGH YADUVANSHI"}
            ],
            "Friday": [
                {"time": "10:00-12:00", "subject": "Basics of Analog & Digital Electronics(PRACTICAL)", "teacher": "RAJVEER SINGH YADUVANSHI"},
                {"time": "12:00-1:00", "subject": "English", "teacher": "POOJA BHARDWAJ"},
                {"time": "2:00-3:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "RAJVEER SINGH YADUVANSHI"},
                {"time": "2:00-4:00", "subject": "Mathematics-I", "teacher": "SHRUTI"},
                {"time": "4:00-6:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "SANJEEVE THAKUR"}
            ]
        },
        "ME-2": {
            "Monday": [
                {"time": "9:00-10:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "KUNWAR SINGH"},
                {"time": "10:00-11:00", "subject": "Environment Science and Green Chemistry", "teacher": "PURNIMA JAIN"},
                {"time": "11:00-1:00", "subject": "English(PRACTICAL)", "teacher": "ANJALI SINGH"},
                {"time": "2:00-4:00", "subject": "Fundamentals of Electrical Engineering(PRACTICAL)", "teacher": "DEEPAK KUMAR GUPTA"}
            ],
            "Tuesday": [
                {"time": "9:00-10:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "DEEPAK KUMAR GUPTA"},
                {"time": "10:00-12:00", "subject": "Basics of Analog & Digital Electronics(PRACTICAL)", "teacher": "KUNWAR SINGH"},
                {"time": "2:00-3:00", "subject": "English", "teacher": "ANJALI SINGH"},
                {"time": "3:00-4:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"}
            ],
            "Wednesday": [
                {"time": "1:00-2:00", "subject": "Environment Science and Green Chemistry", "teacher": "PURNIMA JAIN"},
                {"time": "2:00-3:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "DEEPAK KUMAR GUPTA"},
                {"time": "3:00-4:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "KUNWAR SINGH"},
                {"time": "4:00-6:00", "subject": "Environment Science and Green Chemistry(PRACTICAL)", "teacher": "PURNIMA JAIN"}
            ],
            "Thursday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "English", "teacher": "ANJALI SINGH"},
                {"time": "11:00-12:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"},
                {"time": "12:00-1:00", "subject": "Fundamentals of Electrical Engineering", "teacher": "DEEPAK KUMAR GUPTA"},
                {"time": "1:00-2:00", "subject": "Basics of Analog & Digital Electronics", "teacher": "KUNWAR SINGH"}
            ],
            "Friday": [
                {"time": "8:00-10:00", "subject": "VA Batch-4", "teacher": "VIJEYA SINGH"},
                {"time": "10:00-11:00", "subject": "Mathematics-I", "teacher": "NAVEEN GUPTA"},
                {"time": "11:00-12:00", "subject": "English", "teacher": "ANJALI SINGH"},
                {"time": "1:00-2:00", "subject": "Environment Science and Green Chemistry", "teacher": "PURNIMA JAIN"},
                {"time": "4:00-6:00", "subject": "Mathematics-I(TUTORIAL)", "teacher": "NAVEEN GUPTA"}
            ]
        }
    },
    "2": {}, "3": {}, "4": {}
}

# CONVERSATIONAL FLOWS
flows = {
    'en': {
        'TIMETABLE': {
            'start': {
                'message': "Let's find your timetable. First, please select your year.",
                'replies': [
                    {'text': '1st Year', 'icon': '1️⃣', 'payload': 'TIMETABLE_SET_YEAR_1'},
                    {'text': '2nd Year', 'icon': '2️⃣', 'payload': 'TIMETABLE_SET_YEAR_2'},
                    {'text': '3rd Year', 'icon': '3️⃣', 'payload': 'TIMETABLE_SET_YEAR_3'},
                    {'text': '4th Year', 'icon': '4️⃣', 'payload': 'TIMETABLE_SET_YEAR_4'}
                ],
                'nextStep': 'ask_branch'
            },
            'ask_branch': {
                'message': "Great! Now, please select your branch.",
                'getReplies': lambda: [
                    {'text': branch, 'icon': '📚', 'payload': f"TIMETABLE_SET_BRANCH_{branch.replace(' ', '')}"}
                    for branch in ["CSE-1", "CSE-2", "CSAI-1", "CSAI-2", "IT-1", "IT-2", "CSDS", "ITNS", "MAC", "ECE-1", "ECE-2", "ICE-1", "ICE-2", "EE-1", "EE-2", "EVDT", "ME-1", "ME-2"]
                ],
                'nextStep': 'finish'
            },
            'finish': {}
        }
    },
    'hi': {
        'TIMETABLE': {
            'start': {
                'message': "आइए आपका टाइमटेबल ढूंढते हैं। पहले, कृपया अपना वर्ष चुनें।",
                'replies': [
                    {'text': 'पहला साल', 'icon': '1️⃣', 'payload': 'TIMETABLE_SET_YEAR_1'},
                    {'text': 'दूसरा साल', 'icon': '2️⃣', 'payload': 'TIMETABLE_SET_YEAR_2'},
                    {'text': 'तीसरा साल', 'icon': '3️⃣', 'payload': 'TIMETABLE_SET_YEAR_3'},
                    {'text': 'चौथा साल', 'icon': '4️⃣', 'payload': 'TIMETABLE_SET_YEAR_4'}
                ],
                'nextStep': 'ask_branch'
            },
            'ask_branch': {
                'message': "बहुत बढ़िया! अब, कृपया अपनी शाखा चुनें।",
                'getReplies': lambda: [
                    {'text': branch, 'icon': '📚', 'payload': f"TIMETABLE_SET_BRANCH_{branch.replace(' ', '')}"}
                    for branch in ["CSE-1", "CSE-2", "CSAI-1", "CSAI-2", "IT-1", "IT-2", "CSDS", "ITNS", "MAC", "ECE-1", "ECE-2", "ICE-1", "ICE-2", "EE-1", "EE-2", "EVDT", "ME-1", "ME-2"]
                ],
                'nextStep': 'finish'
            },
            'finish': {}
        }
    },
    'ta': {
        'TIMETABLE': {
            'start': {
                'message': "உங்கள் கால அட்டவணையைக் கண்டுபிடிப்போம். முதலில், உங்கள் ஆண்டைத் தேர்ந்தெடுக்கவும்.",
                'replies': [
                    {'text': 'முதலாம் ஆண்டு', 'icon': '1️⃣', 'payload': 'TIMETABLE_SET_YEAR_1'},
                    {'text': 'இரண்டாம் ஆண்டு', 'icon': '2️⃣', 'payload': 'TIMETABLE_SET_YEAR_2'},
                    {'text': 'மூன்றாம் ஆண்டு', 'icon': '3️⃣', 'payload': 'TIMETABLE_SET_YEAR_3'},
                    {'text': 'நான்காம் ஆண்டு', 'icon': '4️⃣', 'payload': 'TIMETABLE_SET_YEAR_4'}
                ],
                'nextStep': 'ask_branch'
            },
            'ask_branch': {
                'message': "அருமை! இப்போது, உங்கள் துறையைத் தேர்ந்தெடுக்கவும்.",
                'getReplies': lambda: [
                    {'text': branch, 'icon': '📚', 'payload': f"TIMETABLE_SET_BRANCH_{branch.replace(' ', '')}"}
                    for branch in ["CSE-1", "CSE-2", "CSAI-1", "CSAI-2", "IT-1", "IT-2", "CSDS", "ITNS", "MAC", "ECE-1", "ECE-2", "ICE-1", "ICE-2", "EE-1", "EE-2", "EVDT", "ME-1", "ME-2"]
                ],
                'nextStep': 'finish'
            },
            'finish': {}
        }
    },
    'pa': {
        'TIMETABLE': {
            'start': {
                'message': "ਆਓ ਤੁਹਾਡਾ ਟਾਈਮਟੇਬਲ ਲੱਭੀਏ। ਪਹਿਲਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ ਸਾਲ ਚੁਣੋ।",
                'replies': [
                    {'text': 'ਪਹਿਲਾ ਸਾਲ', 'icon': '1️⃣', 'payload': 'TIMETABLE_SET_YEAR_1'},
                    {'text': 'ਦੂਜਾ ਸਾਲ', 'icon': '2️⃣', 'payload': 'TIMETABLE_SET_YEAR_2'},
                    {'text': 'ਤੀਜਾ ਸਾਲ', 'icon': '3️⃣', 'payload': 'TIMETABLE_SET_YEAR_3'},
                    {'text': 'ਚੌਥਾ ਸਾਲ', 'icon': '4️⃣', 'payload': 'TIMETABLE_SET_YEAR_4'}
                ],
                'nextStep': 'ask_branch'
            },
            'ask_branch': {
                'message': "ਬਹੁਤ ਵਧੀਆ! ਹੁਣ, ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਸ਼ਾਖਾ ਚੁਣੋ।",
                'getReplies': lambda: [
                    {'text': branch, 'icon': '📚', 'payload': f"TIMETABLE_SET_BRANCH_{branch.replace(' ', '')}"}
                    for branch in ["CSE-1", "CSE-2", "CSAI-1", "CSAI-2", "IT-1", "IT-2", "CSDS", "ITNS", "MAC", "ECE-1", "ECE-2", "ICE-1", "ICE-2", "EE-1", "EE-2", "EVDT", "ME-1", "ME-2"]
                ],
                'nextStep': 'finish'
            },
            'finish': {}
        }
    }
}

# KNOWLEDGE BASE
knowledge_base = {
    'en': {
        'welcome': "Hi there! I'm Anuvad, the NSUT student assistant. How can I help you today?",
        'farewellMessage': "Later, dude! Have a great one! Feel free to hit me up if you need anything else.",
        'undefinedExplanation': "In simple terms, **'undefined'** means a variable has been declared but not assigned a value. For example, if you say `let x;` but don't give it a value, `x` is `undefined`. It's like an empty box waiting for something to be put inside. In programming, trying to use an `undefined` value can often lead to errors.",
        'greetings': ["hi", "hello", "hey", "hw r u", "heyy"],
        'farewells': ["bye", "goodbye", "cya", "see you", "by"],
        'slang': {
            "hw r u": "I'm good! How can I help you today regarding NSUT?",
            "wyd": "I'm just chilling, waiting for your queries about NSUT. Ask me anything!",
            "whats up": "What's up, my friend! I'm here to help with all things NSUT.",
            "wbu": "I'm doing well, thanks! What about you? What can I do for ya?",
            "hows it going": "It's going great! How can I help you navigate NSUT today?",
            "sup": "Sup! I'm ready to roll. What's on your mind?"
        },
        'mainMenuPrompt': "You can select one of these main topics, or type a question below.",
        'changeLanguagePrompt': "Please select a new language.",
        'mainMenu': [
            {'text': 'About NSUT', 'icon': '🏫', 'payload': 'ABOUT_NSUT', 'keywords': ['nsut', 'about', 'college', 'university']},
            {'text': 'Placements', 'icon': '💼', 'payload': 'PLACEMENTS', 'keywords': ['placement', 'job', 'company', 'recruitment']},
            {'text': 'Scholarships', 'icon': '💰', 'payload': 'SCHOLARSHIPS', 'keywords': ['scholarship', 'grant', 'aid']},
            {'text': 'Fee Deadlines', 'icon': '⏰', 'payload': 'FEES', 'keywords': ['fee', 'deadline', 'payment', 'due']},
            {'text': 'Timetable', 'icon': '🗓️', 'payload': 'TIMETABLE', 'keywords': ['timetable', 'schedule', 'class']},
            {'text': 'More Options...', 'icon': '⚙️', 'payload': 'MORE_OPTIONS', 'keywords': []}
        ],
        'moreOptionsMenu': [
            {'text': 'Exam Info', 'icon': '📝', 'payload': 'EXAMS', 'keywords': ['exam', 'test', 'assessment']},
            {'text': 'Contact Info', 'icon': '📞', 'payload': 'CONTACT', 'keywords': ['contact', 'phone', 'email', 'helpdesk']},
            {'text': 'Campus Events', 'icon': '🎉', 'payload': 'EVENTS', 'keywords': ['event', 'fest', 'workshop']},
            {'text': 'Facilities', 'icon': '🏢', 'payload': 'FACILITIES', 'keywords': ['library', 'gym', 'hostel']},
            {'text': 'Change Language', 'icon': '🌐', 'payload': 'CHANGE_LANGUAGE', 'keywords': ['language', 'switch']},
            {'text': '← Back to Menu', 'icon': '⬅️', 'payload': 'MAIN_MENU', 'keywords': ['back', 'menu']}
        ],
        'responses': {
            'ABOUT_NSUT': {'type': 'text', 'content': "Netaji Subhas University of Technology (NSUT), formerly known as Netaji Subhas Institute of Technology (NSIT), is a premier engineering college in Delhi, India. It was upgraded to a university in 2018. NSUT is known for its strong curriculum, excellent faculty, and high placement rates, especially in the IT and CSE branches. It's often ranked among the top engineering colleges in India."},
            'PLACEMENTS': {'intro': "Here's the latest information from the NSUT Training & Placement Cell:", 'type': 'cards', 'content': [{'title': "Upcoming Placement Drive", 'details': {"Dates": "Oct 05 - Oct 20, 2025", "Eligibility": "Final year B.Tech/M.Tech", "Status": "Registration Open"}, 'linkText': "Register on Portal", 'link': "https://www.tnpnsut.in/"}, {'title': "Pre-Placement Talks Schedule", 'details': {"Companies": "Google, Microsoft, Amazon", "Dates": "Sep 25 - Sep 30, 2025", "Venue": "Main Auditorium"}, 'linkText': "View Full Schedule", 'link': "https://www.tnpnsut.in/"}, {'title': "Placement Cell Contact", 'details': {"In-charge": "Dr. M.P.S. Bhatia", "Mobile no": "+91-9968604104"}, 'linkText': "Visit T&P Website", 'link': "https://www.tnpnsut.in/"}]},
            'SCHOLARSHIPS': {'intro': "Here are the currently available scholarships:", 'type': 'cards', 'content': [{'title': "Merit-cum-Means Scholarship", 'details': {"Eligibility": "Top 10% of branch", "Amount": "₹50,000 / year", "Deadline": "Nov 30, 2025"}, 'linkText': "View & Apply", 'link': "https://incentives.nsut.ac.in/"}, {'title': "NSUT Alumni Scholarship", 'details': {"Eligibility": "Outstanding contribution", "Amount": "100% tuition waiver", "Deadline": "Oct 15, 2025"}, 'linkText': "View & Apply", 'link': "https://incentives.nsut.ac.in/"}]},
            'FEES': {'intro': "Here are the upcoming fee deadlines:", 'type': 'cards', 'content': [{'title': "Tuition Fee - Autumn Sem", 'details': {"Amount": "₹1,25,000", "Deadline": "Sep 30, 2025", "Late Fee": "₹1000 after deadline"}, 'linkText': "More Info", 'link': "https://nsut.ac.in/en/home"}, {'title': "Hostel Fee - Autumn Term", 'details': {"Amount": "₹65,000", "Deadline": "Oct 10, 2025", "Late Fee": "₹500 after deadline"}, 'linkText': "More Info", 'link': "https://nsut.ac.in/en/home"}]},
            'TIMETABLE': {'type': 'start_flow', 'flow': 'TIMETABLE'},
            'EXAMS': {'intro': "Here is the upcoming mid-semester examination schedule:", 'type': 'cards', 'content': [{'title': "Theory Exams", 'details': {"Dates": "Oct 20 - Oct 28, 2025", "Time": "10:00 AM - 1:00 PM", "Seating Plan": "Available Oct 15"}, 'linkText': "View Notifications", 'link': "https://www.imsnsit.org/imsnsit/notifications.php"}, {'title': "Practical Exams", 'details': {"Dates": "Oct 29 - Nov 05, 2025", "Time": "Varies by department", "Notice": "Check with your HOD"}, 'linkText': "View Notifications", 'link': "https://www.imsnsit.org/imsnsit/notifications.php"}]},
            'CONTACT': {'intro': "Here are some important contacts:", 'type': 'cards', 'content': [{'title': "Admissions Office", 'details': {"Phone": "+91-11-25099050", "Email": "admissions@nsut.ac.in", "Hours": "Mon-Fri, 9AM-5PM"}, 'linkText': "Visit Website", 'link': "https://nsut.ac.in/en/home"}, {'title': "IT Helpdesk", 'details': {"Phone": "+91-11-25000132", "Email": "helpdesk@nsut.ac.in", "Hours": "24/7 for critical issues"}, 'linkText': "Visit Website", 'link': "https://nsut.ac.in/en/home"}]},
            'EVENTS': {'intro': "We have some exciting events coming up!", 'type': 'cards', 'content': [{'title': "Moksha-Innovision '25", 'details': {"Dates": "Oct 10 - Oct 12, 2025", "Venue": "Main Campus Grounds", "Highlights": "Concerts, Tech Expo"}, 'linkText': "View Notifications", 'link': "https://www.imsnsit.org/imsnsit/notifications.php"}]},
            'FACILITIES': {'intro': "Information on campus facilities:", 'type': 'cards', 'content': [{'title': "Central Library", 'details': {"Weekdays": "8:00 AM - 10:00 PM", "Weekends": "10:00 AM - 6:00 PM", "Exam Period": "Open 24/7"}, 'linkText': "More Info", 'link': "https://nsut.ac.in/en/home"}, {'title': "Hostel Application", 'details': {"For": "New admissions", "Deadline": "Sep 20, 2025", "Process": "Apply via student portal"}, 'linkText': "More Info", 'link': "https://nsut.ac.in/en/home"}]},
            'PLACEMENT_STATS': {'intro': "Here's a summary of the NSUT placement stats for the 2024 batch:", 'type': 'text', 'content': """
<div class="p-3">
    <p class="font-bold text-white mb-2">Key Placement Highlights for 2024:</p>
    <ul class="list-disc list-inside text-sm mb-4">
        <li><strong>Overall Average Package:</strong> Approx. ₹17.75 LPA</li>
        <li><strong>Highest Package:</strong> ₹1 Crore per annum (International)</li>
        <li><strong>Companies Visited:</strong> Over 320</li>
    </ul>
    <p class="font-bold text-white mb-2">Branch-wise Placement Breakdown:</p>
    <div class="w-full text-left text-sm rounded-lg overflow-hidden bg-white/10 shadow-md">
        <table class="w-full">
            <thead class="bg-white/20">
                <tr>
                    <th class="p-2 font-semibold">Branch</th>
                    <th class="p-2 font-semibold">Highest (LPA)</th>
                    <th class="p-2 font-semibold">Average (LPA)</th>
                </tr>
            </thead>
            <tbody>
                <tr class="border-b border-white/20"><td class="p-2">CSE</td><td class="p-2">₹100</td><td class="p-2">₹25</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">IT</td><td class="p-2">₹90</td><td class="p-2">₹20</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">ECE</td><td class="p-2">₹80</td><td class="p-2">₹15+</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">EE</td><td class="p-2">₹60</td><td class="p-2">₹12</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">ICE</td><td class="p-2">₹50</td><td class="p-2">₹10</td></tr>
                <tr><td class="p-2">ME</td><td class="p-2">₹40</td><td class="p-2">₹8</td></tr>
            </tbody>
        </table>
    </div>
    <p class="text-xs italic mt-3">*Note: Data is approximate and compiled from public sources.</p>
</div>
"""},
            'FALLBACK': {'type': 'text', 'content': "I'm not sure what you're asking. I can help with topics like Placements, Scholarships, or Campus Events. What would you like to know about?"}
        }
    },
    'hi': {
        'welcome': "नमस्ते! मैं अनुवाद हूँ, एनएसयूटी का छात्र सहायक। मैं आज आपकी कैसे मदद कर सकता हूँ?",
        'farewellMessage': "फिर मिलेंगे! आपका दिन शुभ हो! अगर कुछ और जानना हो तो पूछ लेना।",
        'undefinedExplanation': "आसान शब्दों में, **'undefined'** का मतलब है कि एक वेरिएबल घोषित तो कर दिया गया है, लेकिन उसे कोई मान (value) नहीं दी गई है। उदाहरण के लिए, यदि आप `let x;` लिखते हैं, तो `x` की मान `undefined` होती है। यह एक खाली बॉक्स की तरह है जिसमें कुछ भी रखना बाकी है। प्रोग्रामिंग में, `undefined` मान का उपयोग करने से अक्सर त्रुटियाँ हो सकती हैं।",
        'greetings': ["नमस्ते", "हेलो", "कैसा है", "कैसे हो", "ठीक हो"],
        'farewells': ["बाय", "अलविदा", "फिर मिलेंगे"],
        'slang': {
            "कैसा है": "मैं एकदम बढ़िया हूँ! एनएसयूटी के बारे में आपकी क्या मदद कर सकता हूँ?",
            "क्या कर रहा है": "मैं बस तुम्हारे सवालों का इंतजार कर रहा हूँ। पूछो!",
            "kya chal rha hai": "कुछ नहीं यार, बस तुम्हारे सवालों का इंतजार कर रहा हूँ। NSUT से जुड़ी कोई भी जानकारी चाहिए तो पूछो।",
            "sab badhiya": "हाँ यार, सब ठीक है! बताओ NSUT के बारे में क्या जानना चाहते हो?",
            "kya haal hai": "एकदम मस्त! NSUT के बारे में कुछ जानना है क्या?"
        },
        'mainMenuPrompt': "आप इनमें से कोई एक मुख्य विषय चुन सकते हैं, या नीचे अपना प्रश्न टाइप कर सकते हैं।",
        'changeLanguagePrompt': "कृपया एक नई भाषा चुनें।",
        'mainMenu': [
            {'text': 'एनएसयूटी के बारे में', 'icon': '🏫', 'payload': 'ABOUT_NSUT', 'keywords': ['nsut', 'एनएसयूटी', 'कॉलेज', 'विश्वविद्यालय']},
            {'text': 'प्लेसमेंट', 'icon': '💼', 'payload': 'PLACEMENTS', 'keywords': ['प्लेसमेंट', 'नौकरी']},
            {'text': 'छात्रवृत्ति', 'icon': '💰', 'payload': 'SCHOLARSHIPS', 'keywords': ['छात्रवृत्ति', 'स्कॉलरशिप']},
            {'text': 'फीस की अंतिम तिथि', 'icon': '⏰', 'payload': 'FEES', 'keywords': ['फीस', 'अंतिम तिथि']},
            {'text': 'टाइमटेबल', 'icon': '🗓️', 'payload': 'TIMETABLE', 'keywords': ['टाइमटेबल', 'शेड्यूल']},
            {'text': 'और विकल्प...', 'icon': '⚙️', 'payload': 'MORE_OPTIONS', 'keywords': []}
        ],
        'moreOptionsMenu': [
            {'text': 'परीक्षा जानकारी', 'icon': '📝', 'payload': 'EXAMS', 'keywords': ['परीक्षा', 'टेस्ट']},
            {'text': 'संपर्क जानकारी', 'icon': '📞', 'payload': 'CONTACT', 'keywords': ['संपर्क', 'फोन']},
            {'text': 'कैंपस इवेंट्स', 'icon': '🎉', 'payload': 'EVENTS', 'keywords': ['इवेंट', 'फेस्ट']},
            {'text': 'सुविधाएं', 'icon': '🏢', 'payload': 'FACILITIES', 'keywords': ['लाइब्रेरी', 'जिम', 'हॉस्टल']},
            {'text': 'भाषा बदलें', 'icon': '🌐', 'payload': 'CHANGE_LANGUAGE', 'keywords': ['भाषा']},
            {'text': '← वापस मेनू पर', 'icon': '⬅️', 'payload': 'MAIN_MENU', 'keywords': ['वापस', 'मेनू']}
        ],
        'responses': {
            'ABOUT_NSUT': {'type': 'text', 'content': "नेताजी सुभाष प्रौद्योगिकी विश्वविद्यालय (एनएसयूटी), जिसे पहले नेताजी सुभाष प्रौद्योगिकी संस्थान (एनएसआईटी) के नाम से जाना जाता था, दिल्ली का एक प्रमुख इंजीनियरिंग कॉलेज है। इसे 2018 में विश्वविद्यालय का दर्जा दिया गया था। एनएसयूटी अपने मजबूत पाठ्यक्रम, उत्कृष्ट संकाय और उच्च प्लेसमेंट दरों के लिए जाना जाता है, खासकर आईटी और सीएसई शाखाओं में। इसे अक्सर भारत के शीर्ष इंजीनियरिंग कॉलेजों में गिना जाता है।"},
            'PLACEMENTS': {'intro': "एनएसयूटी ट्रेनिंग एंड प्लेसमेंट सेल से नवीनतम जानकारी यहाँ दी गई है:", 'type': 'cards', 'content': [{'title': "आगामी प्लेसमेंट ड्राइव", 'details': {"तिथियाँ": "अक्टूबर 05 - अक्टूबर 20, 2025", "पात्रता": "अंतिम वर्ष बी.टेक/एम.टेक", "स्थिति": "पंजीकरण खुला है"}, 'linkText': "पोर्टल पर रजिस्टर करें", 'link': "https://www.tnpnsut.in/"}, {'title': "प्री-प्लेसमेंट वार्ता शेड्यूल", 'details': {"कंपनियाँ": "गूगल, माइक्रोसॉफ्ट, अमेज़ॅन", "तिथियाँ": "सितम्बर 25 - सितम्बर 30, 2025", "स्थान": "मुख्य सभागार"}, 'linkText': "पूरा शेड्यूल देखें", 'link': "https://www.tnpnsut.in/"}, {'title': "प्लेसमेंट सेल संपर्क", 'details': {"प्रभारी": "डॉ. एम.पी.एस. भाटिया", "मोबाइल नंबर": "+91-9968604104"}, 'linkText': "T&P वेबसाइट पर जाएं", 'link': "https://www.tnpnsut.in/"}]},
            'SCHOLARSHIPS': {'intro': "वर्तमान में उपलब्ध छात्रवृत्तियाँ यहाँ दी गई हैं:", 'type': 'cards', 'content': [{'title': "मेरिट-कम-मीन्स छात्रवृत्ति", 'details': {"पात्रता": "शाखा के शीर्ष 10%", "राशि": "₹50,000 / वर्ष", "अंतिम तिथि": "नवंबर 30, 2025"}, 'linkText': "देखें और आवेदन करें", 'link': "https://incentives.nsut.ac.in/"}, {'title': "एनएसयूटी एलुमनाई छात्रवृत्ति", 'details': {"पात्रता": "उत्कृष्ट योगदान", "राशि": "100% ट्यूशन शुल्क छूट", "अंतिम तिथि": "अक्टूबर 15, 2025"}, 'linkText': "देखें और आवेदन करें", 'link': "https://incentives.nsut.ac.in/"}]},
            'FEES': {'intro': "आगामी फीस की अंतिम तिथियाँ यहाँ दी गई हैं:", 'type': 'cards', 'content': [{'title': "ट्यूशन फीस - शरद सेमेस्टर", 'details': {"राशि": "₹1,25,000", "अंतिम तिथि": "सितम्बर 30, 2025", "विलंब शुल्क": "अंतिम तिथि के बाद ₹1000"}, 'linkText': "और जानकारी", 'link': "https://nsut.ac.in/en/home"}, {'title': "हॉस्टल फीस - शरद सत्र", 'details': {"राशि": "₹65,000", "अंतिम तिथि": "अक्टूबर 10, 2025", "विलंब शुल्क": "अंतिम तिथि के बाद ₹500"}, 'linkText': "और जानकारी", 'link': "https://nsut.ac.in/en/home"}]},
            'TIMETABLE': {'type': 'start_flow', 'flow': 'TIMETABLE'},
            'PLACEMENT_STATS': {'intro': "2024 बैच के लिए एनएसयूटी प्लेसमेंट आंकड़ों का सारांश यहां दिया गया है:", 'type': 'text', 'content': """
<div class="p-3">
    <p class="font-bold text-white mb-2">2024 के लिए मुख्य प्लेसमेंट हाइलाइट्स:</p>
    <ul class="list-disc list-inside text-sm mb-4">
        <li><strong>कुल औसत पैकेज:</strong> लगभग ₹17.75 LPA</li>
        <li><strong>उच्चतम पैकेज:</strong> ₹1 करोड़ प्रति वर्ष (अंतर्राष्ट्रीय)</li>
        <li><strong>कंपनियां आईं:</strong> 320 से अधिक</li>
    </ul>
    <p class="font-bold text-white mb-2">शाखा-वार प्लेसमेंट का विवरण:</p>
    <div class="w-full text-left text-sm rounded-lg overflow-hidden bg-white/10 shadow-md">
        <table class="w-full">
            <thead class="bg-white/20">
                <tr>
                    <th class="p-2 font-semibold">शाखा</th>
                    <th class="p-2 font-semibold">उच्चतम (LPA)</th>
                    <th class="p-2 font-semibold">औसत (LPA)</th>
                </tr>
            </thead>
            <tbody>
                <tr class="border-b border-white/20"><td class="p-2">सीएसई</td><td class="p-2">₹100</td><td class="p-2">₹25</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">आईटी</td><td class="p-2">₹90</td><td class="p-2">₹20</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">ईसीई</td><td class="p-2">₹80</td><td class="p-2">₹15+</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">ईई</td><td class="p-2">₹60</td><td class="p-2">₹12</td></tr>
                <tr class="border-b border-white/20"><td class="p-2">आईसीई</td><td class="p-2">₹50</td><td class="p-2">₹10</td></tr>
                <tr><td class="p-2">एमई</td><td class="p-2">₹40</td><td class="p-2">₹8</td></tr>
            </tbody>
        </table>
    </div>
    <p class="text-xs italic mt-3">*नोट: डेटा अनुमानित है और सार्वजनिक स्रोतों से संकलित है।</p>
</div>
"""},
            'FALLBACK': {'type': 'text', 'content': "मुझे यकीन नहीं है कि मैं इसमें कैसे मदद कर सकता हूँ। आप प्लेसमेंट, छात्रवृत्ति, या कैंपस इवेंट्स जैसे विषयों के बारे में पूछ सकते हैं। क्या आप इनमें से कुछ जानना चाहेंगे?"}
        }
    },
    'ta': {
        'welcome': "வணக்கம்! நான் அனுவாத், NSUT மாணவர் உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
        'farewellMessage': "அப்புறம் பார்க்கலாம்! உங்களுக்கு நல்ல நாள் அமையட்டும்! வேற ஏதாவது தேவைப்பட்டால் கேளுங்கள்.",
        'undefinedExplanation': "எளிய வார்த்தைகளில், **'undefined'** என்றால் ஒரு மாறி அறிவிக்கப்பட்டுவிட்டது ஆனால் அதற்கு மதிப்பு எதுவும் ஒதுக்கப்படவில்லை என்று அர்த்தம். எடுத்துக்காட்டாக, நீங்கள் `let x;` என்று சொன்னால், அதற்கு மதிப்பு கொடுக்காததால், `x` என்பது `undefined` ஆகும். இது உள்ளே எதுவும் இல்லாத ஒரு காலி பெட்டிக்கு ஒத்தது. புரோகிராமிங்கில், `undefined` மதிப்பைப் பயன்படுத்த முயற்சிப்பது பெரும்பாலும் பிழைகளுக்கு வழிவகுக்கும்.",
        'greetings': ["வணக்கம்", "ஹாய்", "ஹேய்", "எப்படி இருக்கிறீர்கள்"],
        'farewells': ["டாடா", "போய் வருகிறேன்", "மீண்டும் சந்திப்போம்"],
        'slang': {
            "எப்படி இருக்கிறீர்கள்": "நான் நன்றாக இருக்கிறேன்! NSUT பற்றி உங்களுக்கு என்ன உதவி வேண்டும்?",
            "என்ன செய்கிறீர்கள்": "நான் சும்மா இருக்கிறேன், உங்கள் கேள்விகளுக்காக காத்திருக்கிறேன். கேளுங்கள்!",
            "enna vishesham": "அப்படி ஒன்னும் இல்ல, உங்க கேள்விக்கு காத்துட்டு இருக்கேன்! NSUT பத்தி ஏதாவது உதவி வேணுமா?"
        },
        'mainMenuPrompt': "நீங்கள் இந்த முக்கிய தலைப்புகளில் ஒன்றைத் தேர்ந்தெடுக்கலாம் அல்லது கீழே ஒரு கேள்வியைத் தட்டச்சு செய்யலாம்.",
        'changeLanguagePrompt': "புதிய மொழியைத் தேர்ந்தெடுக்கவும்.",
        'mainMenu': [
            {'text': 'NSUT பற்றி', 'icon': '🏫', 'payload': 'ABOUT_NSUT', 'keywords': ['nsut', 'பற்றி', 'கல்லூரி', 'பல்கலைக்கழகம்']},
            {'text': 'வேலைவாய்ப்புகள்', 'icon': '💼', 'payload': 'PLACEMENTS', 'keywords': ['வேலை', 'வேலைவாய்ப்பு']},
            {'text': 'கல்வி உதவித்தொகை', 'icon': '💰', 'payload': 'SCHOLARSHIPS', 'keywords': ['உதவித்தொகை', 'ஸ்காலர்ஷிப்']},
            {'text': 'கட்டணக் கடைசி தேதிகள்', 'icon': '⏰', 'payload': 'FEES', 'keywords': ['கட்டணம்', 'கடைசி தேதி']},
            {'text': 'கால அட்டவணை', 'icon': '🗓️', 'payload': 'TIMETABLE', 'keywords': ['அட்டவணை', 'டைம்டேபிள்']},
            {'text': 'மேலும் விருப்பங்கள்...', 'icon': '⚙️', 'payload': 'MORE_OPTIONS', 'keywords': []}
        ],
        'moreOptionsMenu': [
            {'text': 'தேர்வு தகவல்', 'icon': '📝', 'payload': 'EXAMS', 'keywords': ['தேர்வு']},
            {'text': 'தொடர்பு தகவல்', 'icon': '📞', 'payload': 'CONTACT', 'keywords': ['தொடர்பு', 'போன்']},
            {'text': 'வளாக நிகழ்வுகள்', 'icon': '🎉', 'payload': 'EVENTS', 'keywords': ['நிகழ்வு', 'விழா']},
            {'text': 'வசதிகள்', 'icon': '🏢', 'payload': 'FACILITIES', 'keywords': ['நூலகம்', 'ஜிம்', 'ஹாஸ்டல்']},
            {'text': 'மொழியை மாற்று', 'icon': '🌐', 'payload': 'CHANGE_LANGUAGE', 'keywords': ['மொழி']},
            {'text': '← மீண்டும் மெனுவுக்கு', 'icon': '⬅️', 'payload': 'MAIN_MENU', 'keywords': ['மீண்டும்', 'மெனு']}
        ],
        'responses': {
            'ABOUT_NSUT': {'type': 'text', 'content': "நேதாஜி சுபாஸ் தொழில்நுட்ப பல்கலைக்கழகம் (NSUT), முன்பு நேதாஜி சுபாஸ் தொழில்நுட்ப நிறுவனம் (NSIT) என்று அழைக்கப்பட்டது, டெல்லியில் உள்ள ஒரு முதன்மையான பொறியியல் கல்லூரி ஆகும். இது 2018 இல் பல்கலைக்கழகமாக மேம்படுத்தப்பட்டது. NSUT அதன் வலுவான பாடத்திட்டம், சிறந்த ஆசிரியர்கள் மற்றும் அதிக வேலைவாய்ப்பு விகிதங்களுக்கு, குறிப்பாக IT மற்றும் CSE துறைகளில், அறியப்படுகிறது. இது பெரும்பாலும் இந்தியாவின் சிறந்த பொறியியல் கல்லூரிகளில் ஒன்றாகக் கருதப்படுகிறது."},
            'PLACEMENT_STATS': {'intro': "2024 ஆம் ஆண்டுக்கான NSUT வேலைவாய்ப்பு புள்ளிவிவரங்களின் சுருக்கம் இங்கே.", 'type': 'text', 'content': "**2024 க்கான முக்கிய வேலைவாய்ப்பு சிறப்பம்சங்கள்:**\n- **மொத்த சராசரி தொகுப்பு:** தோராயமாக ₹17.75 LPA.\n- **அதிகபட்ச தொகுப்பு:** ₹1 கோடிக்கு சர்வதேச வேலைவாய்ப்பு (₹1 CPA).\n- **பணியமர்த்தும் நிறுவனங்கள்:** 320 க்கும் மேற்பட்ட நிறுவனங்கள் பங்கேற்றன.\n- **முக்கிய பணியமர்த்துபவர்கள்:** Adobe, Amazon, Google, Microsoft, மற்றும் Texas Instruments போன்ற முன்னணி நிறுவனங்கள் இதில் அடங்கும்.\n\n**துறை வாரியான வேலைவாய்ப்பு விவரங்கள் (2024 தரவு):**\n\n```\nதுறை               அதிகபட்ச தொகுப்பு (LPA) சராசரி தொகுப்பு (LPA) வேலைவாய்ப்பு % (2023)\n------------------- ----------------------- ------------------- --------------------\nB.Tech (மொத்தம்)     ₹100                    ₹17.75              85%\nCSE                 ₹100                    ₹25                 90%\nCSE (AI)            ₹100* வரை               ₹23-₹25* 91.47%\nIT                  ₹90                     ₹20                 92.31%\nECE                 ₹80                     ₹15+                81.72%\nECE (AIML)          ₹50                     ~₹14-₹17            குறிப்பிடப்படவில்லை\nEE                  ₹60                     ₹12                 41.06%\nICE                 ₹50                     ₹10                 72.16%\nME                  ₹40                     ₹8                  66.00%\nBiotech             ₹30                     ₹6                  54.05%\nManufacturing       கிடைக்கவில்லை          கிடைக்கவில்லை       75.73%\n```\n*குறிப்பு: அனைத்து துறைகளுக்கும் அதிகாரப்பூர்வ இடைநிலை தொகுப்பு தரவு பொதுவாக வெளியிடப்படுவதில்லை. 2023 ஆம் ஆண்டிற்கான ஒட்டுமொத்த B.Tech இடைநிலை தொகுப்பு ₹17 LPA ஆகும். சில துறைகளின் தரவு CSE புள்ளிவிவரங்களில் சேர்க்கப்பட்டுள்ளது."},
            'FALLBACK': {'type': 'text', 'content': "இதில் எப்படி உதவுவது என்று எனக்குத் தெரியவில்லை. நீங்கள் வேலைவாய்ப்பு, கல்வி உதவித்தொகை, அல்லது வளாக நிகழ்வுகள் போன்ற தலைப்புகளைப் பற்றி கேட்கலாம். இவற்றில் எதை நீங்கள் தெரிந்து கொள்ள விரும்புகிறீர்கள்?"}
        }
    },
    'pa': {
        'welcome': "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਅਨੁਵਾਦ ਹਾਂ, NSUT ਦਾ ਵਿਦਿਆਰਥੀ ਸਹਾਇਕ। ਮੈਂ ਅੱਜ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
        'farewellMessage': "ਚੰਗਾ, ਫੇਰ ਮਿਲਾਂਗੇ! ਤੁਹਾਡਾ ਦਿਨ ਵਧੀਆ ਰਹੇ! ਹੋਰ ਕੁਝ ਜਾਣਨਾ ਹੋਵੇ ਤਾਂ ਪੁੱਛ ਲਿਓ।",
        'undefinedExplanation': "ਸਧਾਰਨ ਸ਼ਬਦਾਂ ਵਿੱਚ, **'undefined'** ਦਾ ਮਤਲਬ ਹੈ ਕਿ ਇੱਕ ਵੇਰੀਏਬਲ ਨੂੰ ਘੋਸ਼ਿਤ ਕੀਤਾ ਗਿਆ ਹੈ ਪਰ ਉਸ ਨੂੰ ਕੋਈ ਮੁੱਲ ਨਹੀਂ ਦਿੱਤਾ ਗਿਆ ਹੈ। ਉਦਾਹਰਨ ਲਈ, ਜੇ ਤੁਸੀਂ `let x;` ਲਿਖਦੇ ਹੋ, ਤਾਂ `x` ਦਾ ਮੁੱਲ `undefined` ਹੁੰਦਾ ਹੈ। ਇਹ ਇੱਕ ਖਾਲੀ ਡੱਬੇ ਵਾਂਗ ਹੈ ਜਿਸ ਵਿੱਚ ਕੁਝ ਵੀ ਪਾਉਣਾ ਬਾਕੀ ਹੈ। ਪ੍ਰੋਗਰਾਮਿੰਗ ਵਿੱਚ, `undefined` ਮੁੱਲ ਦੀ ਵਰਤੋਂ ਕਰਨ ਨਾਲ ਅਕਸਰ ਗਲਤੀਆਂ ਹੋ ਸਕਦੀਆਂ ਹਨ।",
        'greetings': ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ਹੈਲੋ", "ਕਿਵੇਂ ਹੋ"],
        'farewells': ["ਅਲਵਿਦਾ", "ਫਿਰ ਮਿਲਾਂਗੇ"],
        'slang': {
            "ਕਿਵੇਂ ਹੋ": "ਮੈਂ ਬਿਲਕੁਲ ਠੀਕ ਹਾਂ! NSUT ਬਾਰੇ ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
            "ਕੀ ਕਰ ਰਹੇ ਹੋ": "ਮੈਂ ਬਸ ਤੁਹਾਡੇ ਸਵਾਲਾਂ ਦਾ ਇੰਤਜ਼ਾਰ ਕਰ ਰਿਹਾ ਹਾਂ। ਪੁੱਛੋ!",
            "ki haal aa": "ਮੈਂ ਤਾਂ ਵਧੀਆ, ਤੁਸੀਂ ਦੱਸੋ! NSUT ਬਾਰੇ ਕੀ ਪੁੱਛਣਾ ਚਾਹੁੰਦੇ ਹੋ?",
            "ki chal reha hai": "ਕੁਛ ਨਹੀਂ, ਬਸ ਤੁਹਾਡੇ ਸਵਾਲਾਂ ਦਾ ਇੰਤਜ਼ਾਰ ਕਰ ਰਿਹਾ ਹਾਂ। NSUT ਬਾਰੇ ਕੁਝ ਪੁੱਛਣਾ ਹੋਵੇ ਤਾਂ ਦੱਸੋ।",
            "vaddiya": "ਮੈਂ ਵਧੀਆ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ? NSUT ਬਾਰੇ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?"
        },
        'mainMenuPrompt': "ਤੁਸੀਂ ਇਹਨਾਂ ਮੁੱਖ ਵਿਸ਼ਿਆਂ ਵਿੱਚੋਂ ਇੱਕ ਚੁਣ ਸਕਦੇ ਹੋ, ਜਾਂ ਹੇਠਾਂ ਆਪਣਾ ਸਵਾਲ ਟਾਈਪ ਕਰ ਸਕਦੇ ਹੋ।",
        'changeLanguagePrompt': "ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਨਵੀਂ ਭਾਸ਼ਾ ਚੁਣੋ।",
        'mainMenu': [
            {'text': 'ਐਨ.ਐਸ.ਯੂ.ਟੀ. ਬਾਰੇ', 'icon': '🏫', 'payload': 'ABOUT_NSUT', 'keywords': ['nsut', 'ਐਨਐਸਯੂਟੀ', 'ਕਾਲਜ', 'ਯੂਨੀਵਰਸਿਟੀ']},
            {'text': 'ਪਲੇਸਮੈਂਟ', 'icon': '💼', 'payload': 'PLACEMENTS', 'keywords': ['ਪਲੇਸਮੈਂਟ', 'ਨੌਕਰੀ']},
            {'text': 'ਵਜ਼ੀਫੇ', 'icon': '💰', 'payload': 'SCHOLARSHIPS', 'keywords': ['ਵਜ਼ੀਫਾ', 'ਸਕਾਲਰਸ਼ਿਪ']},
            {'text': 'ਫ਼ੀਸ ਦੀ ਆਖਰੀ ਮਿਤੀ', 'icon': '⏰', 'payload': 'FEES', 'keywords': ['ਫ਼ੀਸ', 'ਆਖਰੀ ਮਿਤੀ']},
            {'text': 'ਟਾਈਮਟੇਬਲ', 'icon': '🗓️', 'payload': 'TIMETABLE', 'keywords': ['ਟਾਈਮਟੇਬਲ', 'ਸ਼ਡਿਊਲ']},
            {'text': 'ਹੋਰ ਵਿਕਲਪ...', 'icon': '⚙️', 'payload': 'MORE_OPTIONS', 'keywords': []}
        ],
        'moreOptionsMenu': [
            {'text': 'ਪ੍ਰੀਖਿਆ ਦੀ ਜਾਣਕਾਰੀ', 'icon': '📝', 'payload': 'EXAMS', 'keywords': ['ਪ੍ਰੀਖਿਆ', 'ਟੈਸਟ']},
            {'text': 'ਸੰਪਰਕ ਜਾਣਕਾਰੀ', 'icon': '📞', 'payload': 'CONTACT', 'keywords': ['ਸੰਪਰਕ', 'ਫੋਨ']},
            {'text': 'ਕੈਂਪਸ ਸਮਾਗਮ', 'icon': '🎉', 'payload': 'EVENTS', 'keywords': ['ਸਮਾਗਮ', 'ਫੈਸਟ']},
            {'text': 'ਸਹੂਲਤਾਂ', 'icon': '🏢', 'payload': 'FACILITIES', 'keywords': ['ਲਾਇਬ੍ਰੇਰੀ', 'ਜਿਮ', 'ਹੋਸਟਲ']},
            {'text': 'ਭਾਸ਼ਾ ਬਦਲੋ', 'icon': '🌐', 'payload': 'CHANGE_LANGUAGE', 'keywords': ['ਭਾਸ਼ਾ']},
            {'text': '← ਵਾਪਸ ਮੇਨੂ ਤੇ', 'icon': '⬅️', 'payload': 'MAIN_MENU', 'keywords': ['ਵਾਪਸ', 'ਮੇਨੂ']}
        ],
        'responses': {
            'ABOUT_NSUT': {'type': 'text', 'content': "ਨੇਤਾਜੀ ਸੁਭਾਸ ਯੂਨੀਵਰਸਿਟੀ ਆਫ ਟੈਕਨਾਲੋਜੀ (ਐਨ.ਐਸ.ਯੂ.ਟੀ.), ਜਿਸਨੂੰ ਪਹਿਲਾਂ ਨੇਤਾਜੀ ਸੁਭਾਸ ਇੰਸਟੀਚਿਊਟ ਆਫ ਟੈਕਨਾਲੋਜੀ (ਐਨ.ਐਸ.ਆਈ.ਟੀ.) ਕਿਹਾ ਜਾਂਦਾ ਸੀ, ਦਿੱਲੀ ਦਾ ਇੱਕ ਪ੍ਰਮੁੱਖ ਇੰਜੀਨੀਅਰਿੰਗ ਕਾਲਜ ਹੈ। ਇਸਨੂੰ 2018 ਵਿੱਚ ਯੂਨੀਵਰਸਿਟੀ ਦਾ ਦਰਜਾ ਦਿੱਤਾ ਗਿਆ ਸੀ। ਐਨ.ਐਸ.ਯੂ.ਟੀ. ਆਪਣੇ ਮਜ਼ਬੂਤ ​​ਪਾਠਕ੍ਰਮ, ਉੱਤਮ ਫੈਕਲਟੀ, ਅਤੇ ਉੱਚ ਪਲੇਸਮੈਂਟ ਦਰਾਂ ਲਈ ਜਾਣਿਆ ਜਾਂਦਾ ਹੈ, ਖਾਸ ਕਰਕੇ ਆਈ.ਟੀ. ਅਤੇ ਸੀ.ਐਸ.ਈ. ਸ਼ਾਖਾਵਾਂ ਵਿੱਚ। ਇਸਨੂੰ ਅਕਸਰ ਭਾਰਤ ਦੇ ਚੋਟੀ ਦੇ ਇੰਜੀਨੀਅਰਿੰਗ ਕਾਲਜਾਂ ਵਿੱਚ ਗਿਣਿਆ ਜਾਂਦਾ ਹੈ।"},
            'PLACEMENT_STATS': {'intro': "2024 ਬੈਚ ਲਈ NSUT ਪਲੇਸਮੈਂਟ ਅੰਕੜਿਆਂ ਦਾ ਸਾਰ ਇੱਥੇ ਹੈ।", 'type': 'text', 'content': "**2024 ਲਈ ਮੁੱਖ ਪਲੇਸਮੈਂਟ ਹਾਈਲਾਈਟਸ:**\n- **ਕੁੱਲ ਔਸਤ ਪੈਕੇਜ:** ਲਗਭਗ ₹17.75 LPA।\n- **ਸਭ ਤੋਂ ਵੱਧ ਪੈਕੇਜ:** ₹1 ਕਰੋੜ ਪ੍ਰਤੀ ਸਾਲ (₹1 CPA) ਦੀ ਇੱਕ ਅੰਤਰਰਾਸ਼ਟਰੀ ਪੇਸ਼ਕਸ਼।\n- **ਭਰਤੀ ਕਰਨ ਵਾਲੀਆਂ ਕੰਪਨੀਆਂ:** 320 ਤੋਂ ਵੱਧ ਕੰਪਨੀਆਂ ਨੇ ਹਿੱਸਾ ਲਿਆ।\n- **ਪ੍ਰਮੁੱਖ ਭਰਤੀ ਕਰਨ ਵਾਲੇ:** ਚੋਟੀ ਦੀਆਂ ਕੰਪਨੀਆਂ ਵਿੱਚ ਐਡੋਬ, ਐਮਾਜ਼ਾਨ, ਗੂਗਲ, ​​ਮਾਈਕ੍ਰੋਸਾਫਟ, ਅਤੇ ਟੈਕਸਾਸ ਇੰਸਟਰੂਮੈਂਟਸ ਸ਼ਾਮਲ ਸਨ।\n\n**ਸ਼ਾਖਾ-ਵਾਰ ਪਲੇਸਮੈਂਟ ਵੇਰਵੇ (2024 ਡੇਟਾ):**\n\n```\nਸ਼ਾਖਾ               ਸਭ ਤੋਂ ਵੱਧ ਪੈਕੇਜ (LPA) ਔਸਤ ਪੈਕੇਜ (LPA) ਪਲੇਸਮੈਂਟ % (2023)\n------------------- ----------------------- ------------------- --------------------\nਬੀ.ਟੈਕ (ਕੁੱਲ)        ₹100                    ₹17.75              85%\nਸੀਐਸਈ              ₹100                    ₹25                 90%\nਸੀਐਸਈ (ਏਆਈ)        ₹100* ਤੱਕ                ₹23-₹25* 91.47%\nਆਈਟੀ               ₹90                     ₹20                 92.31%\nਈਸੀਈ                ₹80                     ₹15+                81.72%\nਈਸੀਈ (ਏਆਈਐਮਐਲ)      ₹50                     ~₹14-₹17            ਦੱਸਿਆ ਨਹੀਂ ਗਿਆ\nਈਈ                 ₹60                     ₹12                 41.06%\nਆਈਸੀਈ              ₹50                     ₹10                 72.16%\nਐਮਈ                 ₹40                     ₹8                  66.00%\nਬਾਇਓਟੈਕ            ₹30                     ₹6                  54.05%\nਮੈਨੂਫੈਕਚਰਿੰਗ        ਉਪਲਬਧ ਨਹੀਂ            ਉਪਲਬਧ ਨਹੀਂ         75.73%\n```\n*ਨੋਟ: ਸਾਰੀਆਂ ਸ਼ਾਖਾਵਾਂ ਲਈ ਅਧਿਕਾਰਤ ਮੱਧਮਾਨ ਪੈਕੇਜ ਡੇਟਾ ਜਨਤਕ ਤੌਰ 'ਤੇ ਉਪਲਬਧ ਨਹੀਂ ਹੈ। 2023 ਲਈ ਕੁੱਲ ਬੀ.ਟੈਕ ਮੱਧਮਾਨ ₹17 LPA ਸੀ। ਕੁਝ ਸ਼ਾਖਾਵਾਂ ਦਾ ਡੇਟਾ ਸੀਐਸਈ ਅੰਕੜਿਆਂ ਵਿੱਚ ਸ਼ਾਮਲ ਹੈ।"},
            'FALLBACK': {'type': 'text', 'content': "ਮੈਨੂੰ ਯਕੀਨ ਨਹੀਂ ਹੈ ਕਿ ਮੈਂ ਇਸ ਵਿੱਚ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ। ਤੁਸੀਂ ਪਲੇਸਮੈਂਟ, ਵਜ਼ੀਫੇ, ਜਾਂ ਕੈਂਪਸ ਸਮਾਗਮਾਂ ਵਰਗੇ ਵਿਸ਼ਿਆਂ ਬਾਰੇ ਪੁੱਛ ਸਕਦੇ ਹੋ। ਕੀ ਤੁਸੀਂ ਇਹਨਾਂ ਵਿੱਚੋਂ ਕੁਝ ਜਾਣਨਾ ਚਾਹੋਗੇ?"}
        }
    }
}


def generate_year_data(original_year_data, subject_list):
    new_year_data = copy.deepcopy(original_year_data)
    for branch, days in new_year_data.items():
        for day, slots in days.items():
            for slot in slots:
                if "VA Batch" not in slot['subject']:
                    original_subject_name = slot['subject']
                    new_subject_base = random.choice(subject_list)

                    suffix = ""
                    if "(PRACTICAL)" in original_subject_name:
                        suffix = " (PRACTICAL)"
                    elif "(TUTORIAL)" in original_subject_name:
                        suffix = " (TUTORIAL)"

                    new_subject_name = new_subject_base + suffix
                    slot['subject'] = new_subject_name
                    slot['teacher'] = random.choice(all_teachers)
    return new_year_data

timetable["2"] = generate_year_data(timetable["1"], subjects_year_2)
timetable["3"] = generate_year_data(timetable["1"], subjects_year_3)
timetable["4"] = generate_year_data(timetable["1"], subjects_year_4)

# =================================================================
# FLASK ROUTES
# =================================================================

@app.route('/')
def home():
    # Clear session on new visit to start fresh
    session.clear()
    return render_template("index.html")

@app.route('/get_timetable', methods=['GET'])
def get_timetable():
    year = request.args.get("year")
    branch = request.args.get("branch")
    day = request.args.get("day")

    if year in timetable and branch in timetable[year] and day in timetable[year][branch]:
        return jsonify(timetable[year][branch][day])
    else:
        return jsonify([])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    language = data.get('language', 'en')
    raw_message = data.get('message')
    message_text = (raw_message or '').lower().strip()
    payload = data.get('payload')
    
    # Initialize conversation state in session if not present
    if 'conversation_state' not in session:
        session['conversation_state'] = {}

    actions = []

    # --- Main Logic ---
    
    # Reset flow on any new text input
    if message_text:
        session['conversation_state'] = {}

    # 1. Handle Flow Advancement from Payload
    if session.get('conversation_state') and 'activeFlow' in session['conversation_state']:
        state = session['conversation_state']
        flow_name = state['activeFlow']
        current_step_name = state['step']
        flow = flows[language][flow_name]

        if payload and 'TIMETABLE_SET_YEAR_' in payload:
            state['data']['year'] = payload.split('_').pop()
        elif payload and 'TIMETABLE_SET_BRANCH_' in payload:
            state['data']['branch'] = payload.split('_').pop()
            
        next_step_name = flow[current_step_name].get('nextStep')
        if next_step_name:
            state['step'] = next_step_name
            next_step_info = flow[next_step_name]

            if next_step_name == 'finish':
                actions.append({'type': 'add_bot_message', 'html': '<p class="p-3">Fetching your timetable...</p>'})
                actions.append({'type': 'fetch_timetable', 'year': state['data']['year'], 'branch': state['data']['branch']})
                session['conversation_state'] = {} # End flow
            else:
                actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{next_step_info['message']}</p>"})
                replies = next_step_info['getReplies']() if 'getReplies' in next_step_info else next_step_info['replies']
                actions.append({'type': 'add_quick_replies', 'replies': replies})
        
        session.modified = True
        return jsonify({'actions': actions})


    # 2. Handle Direct Payloads (Menus, Language Change, etc.)
    if payload:
        if 'LANG_' in payload:
            lang_code = payload.split('_')[1]
            actions.append({'type': 'set_language', 'language': lang_code})
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{knowledge_base[lang_code]['welcome']}</p>"})
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{knowledge_base[lang_code]['mainMenuPrompt']}</p>"})
            actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[lang_code]['mainMenu']})
            actions.append({'type': 'toggle_input_area', 'show': True})
        elif payload == 'MAIN_MENU':
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{knowledge_base[language]['mainMenuPrompt']}</p>"})
            actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[language]['mainMenu']})
            actions.append({'type': 'toggle_input_area', 'show': True})
        elif payload == 'MORE_OPTIONS':
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>Here are some other things I can help with:</p>"})
            actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[language]['moreOptionsMenu']})
        elif payload == 'CHANGE_LANGUAGE':
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{knowledge_base[language]['changeLanguagePrompt']}</p>"})
            languages = [{'text': 'English', 'payload': 'LANG_en'}, {'text': 'हिन्दी', 'payload': 'LANG_hi'}, {'text': 'தமிழ்', 'payload': 'LANG_ta'}, {'text': 'ਪੰਜਾਬੀ', 'payload': 'LANG_pa'}]
            actions.append({'type': 'add_quick_replies', 'replies': [{'text': l['text'], 'icon': '🌐', 'payload': l['payload']} for l in languages]})
            actions.append({'type': 'toggle_input_area', 'show': False})
        else: # Handle all other knowledge base responses
            response = knowledge_base[language]['responses'].get(payload)
            if response:
                if response.get('type') == 'start_flow':
                    flow_name = response['flow']
                    session['conversation_state'] = {'activeFlow': flow_name, 'step': 'start', 'data': {}}
                    session.modified = True
                    start_step = flows[language][flow_name]['start']
                    actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{start_step['message']}</p>"})
                    actions.append({'type': 'add_quick_replies', 'replies': start_step['replies']})
                    actions.append({'type': 'toggle_input_area', 'show': False})
                else:
                    if 'intro' in response:
                        actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{response['intro']}</p>"})
                    if response.get('type') == 'cards':
                        for card in response['content']:
                            actions.append({'type': 'add_link_card', 'cardData': card})
                        if payload == 'PLACEMENTS':
                            actions.append({'type': 'add_quick_replies', 'replies': [{'text': 'View Placement Stats', 'icon': '📊', 'payload': 'PLACEMENT_STATS'}, {'text': '← Back to Menu', 'icon': '⬅️', 'payload': 'MAIN_MENU'}]})
                    elif response.get('type') == 'text':
                         actions.append({'type': 'add_bot_message', 'html': f"<div class='p-3'>{response['content']}</div>"})
                         if payload != 'FALLBACK': # Add main menu after a standard text response
                             actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[language]['mainMenu']})
                             actions.append({'type': 'toggle_input_area', 'show': True})
        return jsonify({'actions': actions})

    # 3. Handle Text Input
    if message_text:
        # Check slang, greetings, farewells
        if message_text in knowledge_base[language]['slang']:
            response_text = knowledge_base[language]['slang'][message_text]
            actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{response_text}</p>"})
            actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[language]['mainMenu']})
            return jsonify({'actions': actions})
        # ... Similar checks for greetings, farewells, specific keywords...
        # Fallback to keyword matching
        matched_payload = None
        all_options = knowledge_base[language]['mainMenu'] + knowledge_base[language]['moreOptionsMenu']
        for option in all_options:
            for keyword in option['keywords']:
                if keyword in message_text:
                    matched_payload = option['payload']
                    break
            if matched_payload:
                break
        
        if matched_payload:
            # Re-process as if it were a payload
            return chat_with_payload(matched_payload, language)
        
        # If no match, send fallback
        fallback_response = knowledge_base[language]['responses']['FALLBACK']
        actions.append({'type': 'add_bot_message', 'html': f"<div class='p-3'>{fallback_response['content']}</div>"})
        # Suggest random options for fallback
        all_options_for_suggestion = [opt for opt in knowledge_base[language]['mainMenu'] if opt['payload'] not in ['MORE_OPTIONS']]
        suggestions = random.sample(all_options_for_suggestion, min(len(all_options_for_suggestion), 3))
        actions.append({'type': 'add_quick_replies', 'replies': suggestions})
        return jsonify({'actions': actions})

    # 4. Handle Initial Conversation Start (no payload, no message)
    if not payload and not message_text:
        initial_greeting = "<div class='p-3'><p>Welcome! Please select your language.</p><hr class='my-2 border-red-300'><p>नमस्ते! कृपया अपनी भाषा चुनें।</p><hr class='my-2 border-red-300'><p>வணக்கம்! உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்.</p><hr class='my-2 border-red-300'><p>ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ।</p></div>"
        languages = [{'text': 'English', 'payload': 'LANG_en'}, {'text': 'हिन्दी', 'payload': 'LANG_hi'}, {'text': 'தமிழ்', 'payload': 'LANG_ta'}, {'text': 'ਪੰਜਾਬੀ', 'payload': 'LANG_pa'}]
        actions.append({'type': 'add_bot_message', 'html': initial_greeting})
        actions.append({'type': 'add_quick_replies', 'replies': [{'text': l['text'], 'icon': '🌐', 'payload': l['payload']} for l in languages]})
        actions.append({'type': 'toggle_input_area', 'show': False})

    return jsonify({'actions': actions})

def chat_with_payload(payload, language):
    """A helper function to re-route a text match to the payload logic."""
    # This is a simplified version of the payload handling logic from the main chat function.
    # A more robust implementation might refactor the main function to avoid this repetition.
    actions = []
    response = knowledge_base[language]['responses'].get(payload)
    if 'intro' in response:
        actions.append({'type': 'add_bot_message', 'html': f"<p class='p-3'>{response['intro']}</p>"})
    if response.get('type') == 'cards':
        for card in response['content']:
            actions.append({'type': 'add_link_card', 'cardData': card})
    elif response.get('type') == 'text':
        actions.append({'type': 'add_bot_message', 'html': f"<div class='p-3'>{response['content']}</div>"})
    
    actions.append({'type': 'add_quick_replies', 'replies': knowledge_base[language]['mainMenu']})
    actions.append({'type': 'toggle_input_area', 'show': True})
    return jsonify({'actions': actions})


if __name__ == "__main__":
    app.run(debug=True, port=5001) 