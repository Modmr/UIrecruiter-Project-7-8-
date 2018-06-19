from fpdf import FPDF


def create(subject_info, match_scores, transcript, session_id):
    class PDF(FPDF):
        def header(self):
            self.title_style(title)
            self.subtitle_style(subtitle)

            self.line(3)

        def footer(self):
            self.set_y(-15)
            self.set_font("Merriweather", "", 10)
            self.set_text_color(102, 103, 100)
            self.cell(0, 10, str(self.page_no()), 0, 0, "C")

        def add_subject_info(self, subject_info, session_id):
            subject_parameters = ["First Name", "Last Name", "Age", "Positive Traits", "Neutral Traits", "Negative Traits",
                                  "College Degree", "College Major", "Position", "Experience (years)", "Strengths", "Weaknesses", "Availablity (hours a week)"]

            self.h1("Subject \"{}\" Info".format(session_id))

            index = 0
            for info in subject_info.values():
                self.strong("{}: ".format(subject_parameters[index]), 60, 0)
                self.p(str(info).strip("[]").replace("'", ""), 0, 1)
                self.ln(2)

                index = index + 1

        def add_match_scores(self, match_scores):
            positions = ["Junior Software Engineer", "Software Engineer", "Data Analyst", "Data Scientist",
                         "Social Media Manager", "Sales Representative", "Human Resources Specialist",
                         "IT Consultant", "Management Consultant", "Business Adviser",
                         "Project Manager", "Risk Manager", "Statistician",
                         "Accountant", "Digital Copywriter", "Writer",
                         "Web Content Manager", "Therapist", "Market Researcher",
                         "Network Engineer", "Design Engineer", "Advertising"]

            self.ln(10)
            self.h1("Match Scores")

            index = 0
            for score in match_scores:
                self.strong("{}: ".format(positions[index]), 60, 0)
                self.p("{:.2%}".format(score), 32, index % 2)

                if index % 2:
                    self.ln(2)

                index = index + 1

        def add_transcript(self, transcript, subject_name, recruiter_name="Recruiter Diana"):
            self.add_page()
            self.h1("Transcript")

            index = 0
            for i in range(len(transcript[0])):
                self.strong("{}: ".format(subject_name), 32, 0)
                self.ps(transcript[0][i], 0)
                self.ln(5)
                self.strong("{}: ".format(recruiter_name), 32, 0)
                self.ps(transcript[1][i], 0)
                self.ln(5)

                index = index + 1

        def line(self, width=1, margin=5):
            self.set_line_width(0.1)
            self.ln(5)
            for i in range(width):
                self.cell(0, 0.1, "", 1, 1, "C", 0)
            self.ln(5)
            self.set_line_width(0.2)

        def title_style(self, text_input, pos=1, border=0):
            self.set_font("Merriweather", "B", 36)
            self.set_text_color(0, 0, 0)
            self.cell(0, 18, text_input, border, pos, "C", 0)

        def subtitle_style(self, text_input, pos=1, border=0):
            self.set_font("Montserrat", "", 11)
            self.set_text_color(102, 103, 100)
            self.cell(0, 5, text_input, border, pos, "C", 0)

        def h1(self, text_input, pos=1, border=0):
            self.set_font("Montserrat", "B", 12)
            self.set_text_color(102, 217, 239)
            self.cell(0, 5, text_input.upper(), border, pos, "L", 0)
            self.ln(3)

        def p(self, text_input, width=0, pos=0, border=0):
            self.set_font("Merriweather", "", 10)
            self.set_text_color(102, 103, 100)
            self.cell(width, 4, text_input, border, pos, "L", 0)

        def ps(self, text_input, width=0, border=0):
            self.set_font("Merriweather", "", 10)
            self.set_text_color(102, 103, 100)
            self.multi_cell(width, 4, text_input, border, "L", 0)

        def strong(self, text_input, width=0, pos=0, border=0):
            self.set_font("Merriweather", "B", 10)
            self.set_text_color(102, 103, 100)
            self.cell(width, 4, text_input, border, pos, "L", 0)

    pdf = PDF()
    pdf.set_margins(13, 16, 13)

    pdf.add_font("Montserrat", "",
                 "./resources/fonts/Montserrat/Montserrat-Regular.ttf", uni=True)
    pdf.add_font("Montserrat", "B",
                 "./resources/fonts/Montserrat/Montserrat-Bold.ttf", uni=True)
    pdf.add_font("Montserrat", "I",
                 "./resources/fonts/Montserrat/Montserrat-Italic.ttf", uni=True)
    pdf.add_font("Montserrat", "BI",
                 "./resources/fonts/Montserrat/Montserrat-BoldItalic.ttf", uni=True)
    pdf.add_font("Merriweather", "",
                 "./resources/fonts/Merriweather/Merriweather-Regular.ttf", uni=True)
    pdf.add_font("Merriweather", "B",
                 "./resources/fonts/Merriweather/Merriweather-Bold.ttf", uni=True)
    pdf.add_font("Merriweather", "I",
                 "./resources/fonts/Merriweather/Merriweather-Italic.ttf", uni=True)
    pdf.add_font("Merriweather", "BI",
                 "./resources/fonts/Merriweather/Merriweather-BoldItalic.ttf", uni=True)

    title = "Interview Report"
    subtitle = "Project 7/8: Automated Screening Interview"

    pdf.set_title("Interview report")
    pdf.set_author(
        "Osman Altun, Muhammet Demir, Endy Hu, Muhammed Incekara, Mahmut Ozler, Satrya Sabeni")

    pdf.add_page()
    pdf.add_subject_info(subject_info, session_id)
    pdf.add_match_scores(match_scores)
    pdf.add_transcript(transcript, "{} {}".format(
        subject_info["given-name"], subject_info["last-name"]))

    pdf.output("./resources/reports/report-{}.pdf".format(session_id), "F")
    print("Interview Report created in ./resources/reports/report-{}.pdf".format(session_id))
