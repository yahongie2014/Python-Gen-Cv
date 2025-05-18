import requests
from fpdf import FPDF
from PIL import Image, ImageDraw
from datetime import datetime
import os


# Function to download icons from URL and ensure they are saved as PNG
def download_icon(url, icon_name):
    """Download icon and save to disk as PNG"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(icon_name, 'wb') as f:
            f.write(response.content)

        # Open the image to check its format and ensure it is in PNG format
        img = Image.open(icon_name)

        # If the image is not in PNG format, convert it to PNG
        if img.format != 'PNG':
            img = img.convert("RGBA")  # Convert to RGBA if not in PNG format
            img.save(icon_name, 'PNG')


# Function to make an image rounded (optional for profile image)
def make_image_rounded(input_path, output_path, size=(150, 150)):
    img = Image.open(input_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)

    # Create a circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Apply the mask to the image
    rounded = Image.new("RGBA", size)
    rounded.paste(img, (0, 0), mask=mask)
    rounded.save(output_path)


# Create a custom CV template using FPDF
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.is_first_page = True
        self.last_page_number = None

    def header(self):
        if self.is_first_page:
            rounded_image_path = './me_rounded.png'
            make_image_rounded('./me.png', rounded_image_path)

            # Insert the image
            self.image(rounded_image_path, 10, 10, 25)

            # Add name and title
            self.set_xy(40, 10)
            self.set_font("Arial", '', 20)
            self.cell(0, 10, "Ahmed Saeed", ln=True, align="L")
            self.set_xy(40, 20)
            self.set_font("Arial", '', 14)
            self.set_text_color(50, 50, 50)
            self.cell(0, 10, "Senior Full-Stack Software Developer", ln=True, align="L")
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            self.line(10, 35, 200, 35)
            self.is_first_page = False

    def footer(self):
        # Set footer position 15mm from the bottom
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)

        # Add page number in the footer
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

        # Add a custom footer message
        self.ln(5)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, '"The only way to do great work is to love what you do." - Steve Jobs', 0, 0, 'C')

    def contact_info(self):
        self.ln(10)
        self.set_font("Arial", "", 12)

        # Center the phone and email text (optional)
        self.cell(0, 10, "Phone: +20 10 9195 0488  |  Email: a.saeed@null.net", ln=True, align="C")

        # Set up text color for the icons (Blue color for links)
        self.set_text_color(0, 0, 255)  # Blue color for links

        # Center the icons without text
        icon_size = 8  # Size of the icons
        icon_y_position = self.get_y() + 3

        # Download the icons automatically and save them in PNG format
        download_icon("https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo_2023.png", "linkedin_icon.png")
        download_icon("https://upload.wikimedia.org/wikipedia/commons/8/83/GitHub_Logo_2023.png", "github_icon.png")
        download_icon("https://upload.wikimedia.org/wikipedia/commons/6/6c/Portfolio_icon.svg", "portfolio_icon.png")

        # Check if icons are downloaded successfully
        if os.path.exists("linkedin_icon.png") and os.path.exists("github_icon.png") and os.path.exists(
                "portfolio_icon.png"):
            # Center the LinkedIn icon
            self.image("linkedin_icon.png", x=(self.w - 3 * icon_size) * 3 / 7, y=icon_y_position, w=icon_size)
            self.link(x=(self.w - 3 * icon_size) * 3 / 7, y=icon_y_position, w=icon_size, h=icon_size,
                      link="https://linkedin.com/in/devahmedsaeed")

            # GitHub icon and link
            self.image("github_icon.png", x=(self.w - 3 * icon_size) * 4 / 8, y=icon_y_position, w=icon_size)
            self.link(x=(self.w - 3 * icon_size) * 4 / 8, y=icon_y_position, w=icon_size, h=icon_size,
                      link="https://github.com/yahongie2014")

            # Portfolio icon and link
            self.image("portfolio_icon.png", x=(self.w - 3 * icon_size) * 6 / 10.5, y=icon_y_position, w=icon_size)
            self.link(x=(self.w - 3 * icon_size) * 6 / 10.5, y=icon_y_position, w=icon_size, h=icon_size,
                      link="http://coder79.me")

        self.ln(10)

    def section_title(self, title):
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)

    def section_body(self, body):
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)

        # Check if the body is a list and convert it to a string if it is
        if isinstance(body, list):
            body = "\n".join(body)  # Join list items into a single string with line breaks

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

            duration = calculate_duration(details['Duration'].split(' - ')[0],
                                          details['Duration'].split(' - ')[1] if ' - ' in details[
                                              'Duration'] else "Present")
            self.set_font("Arial", "", 10)
            self.cell(0, 10, f"Duration: {duration}", ln=True)
            self.ln(3)

            self.set_font("Arial", "", 9)
            for responsibility in details['Responsibilities']:
                self.cell(10)
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

    def section_certifications(self, certifications):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, "Certifications", ln=True)
        self.ln(5)
        self.set_text_color(0, 0, 0)

        for certification in certifications:
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, certification)
            self.ln(3)

    def section_education(self, education):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, "Education", ln=True)
        self.ln(5)
        self.set_text_color(0, 0, 0)

        for edu in education:
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, edu)
            self.ln(3)

    def section_skills(self, skills):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, "Skills", ln=True)
        self.ln(5)
        self.set_text_color(0, 0, 0)

        for skill in skills:
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, skill)
            self.ln(3)

    def section_divider(self):
        self.set_draw_color(169, 169, 169)  # Light gray
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)


def calculate_duration(start_date: str, end_date: str) -> str:
    date_format = "%b %Y"

    try:
        start = datetime.strptime(start_date, date_format)
        if end_date.lower() == "present":
            end = datetime.today()
        else:
            end = datetime.strptime(end_date, date_format)

        delta = end - start
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f"{years} years, {months} months"
    except Exception as e:
        return "Invalid dates"


# Data
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
        "Duration": "Feb 2020 - Jul 2020",
        "Responsibilities": [
            "Developed a secure CRM platform serving 20,000+ Employee.",
            "Integrated payment gateways, reducing transaction failures by 15%.",
            "Automated deployment processes, saving more than 10 hours/week in manual efforts."
        ]
    },
    "Full Stack Dev": {
        "Company": "MCLedger Corporation",
        "Duration": "Mar 2018 - Aug 2019",
        "Responsibilities": [
            "Delivered 3 ERP systems, driving efficiency for EMIRATE-based clients.",
            "Reduced page load times by 40% through query optimization.",
            "Trained 5 junior developers, fostering a collaborative team culture."
        ]
    },
    "SR-PHP Dev": {
        "Company": "ITSMART Corporation (Frame Work - Micro Services)",
        "Duration": "Oct 2016 - Jun 2018",
        "Responsibilities": [
            "Contributed to the development of an internal project with a team of developers. (Ratbli Project & Others)",
            "Reduced page load times by 40% through query optimization.",
            "Trained 5 junior developers, fostering a collaborative team culture."
        ]
    },
    "MD-PHP Developer": {
        "Company": "Arqqa Digital Agency (CMS - Native)",
        "Duration": "Sept 2015 - Aug 2016",
        "Responsibilities": [
            "Contributed to the development of an internal project with a team of developers.",
            "Focused on maintaining and developing core PHP-based solutions for travel services."
        ]
    }
}

certifications = [
    "AWS Certified Developer Associate (2017)",
    "Scrum Master Certification (2016)",
    "Certified Microsoft Developer MSP (2013)"
]

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

education = [
    "Bachelor's Degree in MISE - Modern Academy Institute (Jan 2010 - May 2014)",
    "Professional Diploma in Programming - YAT Center (2013 - 2014)",
    "Professional Diploma in Web Development - Russian Culture Center (2014)"
]

skills = [
    "Programming: PHP, JavaScript (Pure, Node.js), Python",
    "Frameworks: Laravel, CakePHP , Symfony , Nextjs ,React Native, Django, Flask",
    "CMS: Wordpress , Magento , Shopify , Laravel Nova",
    "Tools: Git ,Docker, Kubernetes",
    "Databases: MySQL, MongoDB, Firebase",
    "Servers: AWS, DigitalOcean, Vercel,railway",
    "Additional: Agile methodologies, API Documentation, Payment Systems Integration , Socket IO, Redis"
]

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
languages = """
 - English: Fluent
 - Arabic: Native
"""

pdf.section_divider()

# Technical Skills
pdf.section_title("Technical Skills")
pdf.section_skills(skills)
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

# Output PDF
output_path = "./Ahmed-Saeed(SR).pdf"
pdf.output(output_path)
