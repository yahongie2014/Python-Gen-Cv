from fpdf import FPDF
from reportlab.pdfgen import canvas

# Create a custom CV template using FPDF
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.is_first_page = True
        self.last_page_number = None

    def header(self):
        if self.is_first_page:
            self.image('./me.png', 10, 10, 18)
            # Add name and title
            self.set_xy(40, 10)
            self.set_font("Arial", '', 20)
            self.cell(0, 10, "Ahmed Saeed", ln=True, align="L")
            self.set_xy(40, 20)
            self.set_font("Arial", '', 14)
            self.set_text_color(50, 50, 50)
            self.cell(0, 10, "Senior Full-Stack Software Developer", ln=True, align="L")

            # Draw a horizontal line to separate the header
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            self.line(10, 35, 200, 35)

            self.is_first_page = False

    def contact_info(self):
        self.ln(10)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "Phone: +20 10 9195 0488  |  Email: a.saeed@null.net", ln=True, align="C")
        self.cell(0, 10, "LinkedIn: linkedin.com/in/devahmedsaeed | GitHub: github.com/yahongie2014", ln=True, align="C")
        self.cell(0, 10, "Portfolio: coder79.me", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)

    def section_body(self, body):
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, body)
        self.ln(5)

    def section_experience(self, experiences):
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, "Professional Experience", ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

        for role, details in experiences.items():
            # Role and Company
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, f"{role}", ln=True)
            self.set_font("Arial", "I", 10)
            self.cell(0, 10, f"{details['Company']} | {details['Duration']}", ln=True)
            self.ln(3)

            # Responsibilities
            self.set_font("Arial", "", 9)
            for responsibility in details['Responsibilities']:
                self.cell(10)  # Indentation
                self.multi_cell(0, 10, f"- {responsibility}")
            self.ln(5)

    def section_projects(self, projects):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, "Projects", ln=True)
        self.ln(5)
        self.set_text_color(0, 0, 0)

        for project in projects:
            # Title
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, project["Title"], ln=True)

            # Details
            self.set_font("Arial", "", 9)
            self.cell(10)
            self.multi_cell(0, 10, f"{project['Description']}")
            self.ln(3)

    def footer(self):
        if self.page_no() == self.last_page_number:
            self.set_y(-15)
            self.set_font("Arial", "I", 10)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, '"The only way to do great work is to love what you do." - Steve Jobs', align="C")

    def section_divider(self):
        self.set_draw_color(169, 169, 169)  # Light gray
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

# Generate PDF
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Contact Information Section
pdf.contact_info()

# Professional Summary
pdf.section_title("Professional Summary")
pdf.section_body(
"""Innovative Software Engineer with 13+ years of experience in PHP, JavaScript, and Python, adept at designing scalable APIs and CMS platforms, with a proven history of delivering high-quality Software Solutions"""
)
pdf.section_divider()

experiences = {
    "SR Full-Stack Dev (Team Lead)": {
        "Company": "Future Group (UnitLabs)",
        "Duration": "Feb 2022 - Present",
        "Responsibilities": [
            "Led a team of 3 engineers, delivering 10+ web and mobile solutions with zero downtime.",
            "Improved system performance by 25% by optimizing APIs.",
            "Create AI Models With python to help translator in CRM.",
            "Spearheaded the migration to PHP 8.0 and Laravel, enhancing code maintainability."
        ]
    },
    "SR Full-Stack Dev": {
        "Company": "Aramco Fal",
        "Duration": "Feb 2022 - June 2022",
        "Responsibilities": [
            "Developed a secure CRM platform serving 20,000+ Employee.",
            "Integrated payment gateways, reducing transaction failures by 15%.",
            "Automated deployment processes, saving more than 10 hours/week in manual efforts."
        ]
    },
    "SR PHP Developer": {
        "Company": "4Deve Corporation",
        "Duration": "Jan 2019 - May 2020",
        "Responsibilities": [
            "Delivered 3 ERP systems, driving efficiency for KSA-based clients.",
            "Reduced page load times by 40% through query optimization.",
            "Trained 5 junior developers, fostering a collaborative team culture."
        ]
    },
    "MD-PHP Dev": {
        "Company": "ITSMART Corporation",
        "Duration": "April 2016 - Dec 2018",
        "Responsibilities": [
            "Contributed to the development of an internal project with a team of developers.",
            "Reduced page load times by 40% through query optimization.",
            "Trained 5 junior developers, fostering a collaborative team culture."
        ]
    },
    "MD-PHP Developer": {
        "Company": "Gobus Corporation",
        "Duration": "March 2015 - Feb 2016",
        "Responsibilities": [
            "Contributed to the development of an internal project with a team of developers.",
            "Focused on maintaining and developing core PHP-based solutions for travel services."
        ]
    }
}

education = """
 - Bachelor's Degree in MISE - Modern Academy Institute (Jan 2010 - May 2014)
 - Professional Diploma in Programming - YAT Center (2013 - 2014)
 - Professional Diploma in Web Development - Russian Culture Center (2014)
"""

skills = """
 - Programming: PHP, JavaScript (Pure, Node.js), Python
 - Frameworks: Laravel, React Native, Django, Flask
 - Tools: Docker, Kubernetes, Git, AWS
 - Databases: MySQL, MongoDB, Firebase
 - Additional: Agile methodologies, API Documentation, Payment Systems Integration
"""

certifications = """
 - AWS Certified Developer Associate (2017)
 - Scrum Master Certification (2016)
 - Certified Microsoft Developer MSP (2013)
"""

projects = [
    {
        "Title": "Ratbli, SaaeiApp, and BlueAge,etc..",
        "Description": "Developed and launched businesses in KSA, leading a team of 5 engineers."
    },
    {
        "Title": "SmartFurniture and BexBeauty,etc..",
        "Description": "Designed scalable e-commerce platforms used by 20,000+ active customers."
    },
    {
        "Title": "TPS , FAL ,MaCledger",
        "Description": "CRM Hub For Freelancers and more with Integrated AR technology and AI Models."
    },
    {
        "Title": "Open-Source Contributions",
        "Description": "Actively contributed to 80+ GitHub repositories, enhancing software functionality and documentation."
    }
]

languages = """
 - English: Fluent
 - Arabic: Native
"""

# Technical Skills
pdf.section_title("Technical Skills")
pdf.section_body(skills)
pdf.section_divider()

# Education
pdf.section_title("Education")
pdf.section_body(education)
pdf.section_divider()

# Certifications
pdf.section_title("Certifications")
pdf.section_body(certifications)
pdf.section_divider()


# Professional Experience
pdf.section_experience(experiences)
pdf.section_divider()


# Projects
pdf.section_projects(projects)
pdf.section_divider()

# Languages
pdf.section_title("Languages")
pdf.section_body(languages)


pdf.last_page_number = pdf.page_no()

# Output PDF
output_path = "./Ahmed-Saeed(SR).pdf"
pdf.output(output_path)
