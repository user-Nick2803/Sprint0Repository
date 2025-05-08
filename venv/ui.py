from discord.ui import View, Select
from discord import SelectOption, Interaction

class DropdownMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        # Create the dropdown select
        self.select = Select(
            placeholder="What would you like to do?",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label="Admissions & Aid", description="Information on applying to Rowan Univeristy and financial aid", value="admissions_aid"),
                SelectOption(label="Academics", description="Information on Rowan University's academics", value="academics"),
                SelectOption(label="Campus Life", description="Information on Rowan University's campus life and housing", value="campus_life"),
                SelectOption(label="Health & Medicine", description="Information on Rowan's medical schools", value="health_medicine"),
                SelectOption(label="Research", description="Information on research opportunities at Rowan University", value="research"),
                SelectOption(label="Military/Veterans", description="Information for Rowan students with military service history", value="military"),
                SelectOption(label="Thrive", description="Information for aiding your well-being at Rowan University", value="thrive"),
                SelectOption(label="About Rowan", description="Information on Rowan University", value="about"),
                SelectOption(label="Section Tally", description="Look at classes for future semesters", value="section_tally"),
                SelectOption(label="Survey", description="Survey for feedback on the Rowan Chatbot", value="survey"),
            ]
        )
        # Assign callback and add to view
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: Interaction):
        choice = self.select.values[0]
        if choice == "admissions_aid":
            await interaction.response.send_message("Home page for Admissions & Aid: https://www.rowan.edu/admissions_aid/"
                                                    "\nFirst-Year Admissions: https://admissions.rowan.edu/"
                                                    "\nTransfer Admissions: https://admissions.rowan.edu/admissions-process/transfer-requirements/"
                                                    "\nFinancial Aid: https://sites.rowan.edu/financial-aid/"
                                                    "\nGraduate Admissions & Degree Completion: https://global.rowan.edu/"
                                                    "\nMedical Education Admissions: https://www.rowan.edu/admissions_aid/medical_education.html"
                                                    "\nInternational Admissions: https://admissions.rowan.edu/international/"
                                                    "\nTours & Open House: https://apply.rowan.edu/portal/visit"
                                                    "\nOnline Learning: https://www.rowan.edu/online/")
        elif choice == "academics":
            await interaction.response.send_message("Home page for Academics: https://www.rowan.edu/academics/"
                                                    "\nColleges & Schools: https://www.rowan.edu/academics/colleges_and_schools/"
                                                    "\nDegrees & Programs: https://www.rowan.edu/academics/degree_programs.html"
                                                    "\nCourses, Schedules, & Registration: https://www.rowan.edu/academics/cou_sche_reg.html"
                                                    "\nStudent Success: https://sites.rowan.edu/student-success/"
                                                    "\nInternational: https://sites.rowan.edu/international/"
                                                    "\nWinter & Summer Sessions: https://global.rowan.edu/alternate-pathways/summer-winter/"
                                                    "\nCamden Campus: https://global.rowan.edu/alternate-pathways/county-college-partner-schools/"
                                                    "\nRowan Library: https://www.rowan.edu/academics/university_libraries.html"
                                                    "\nBookstore: https://www.rowan.edu/academics/bookstore.html")                                                   
        elif choice == "campus_life":
            await interaction.response.send_message("Home page for Campus Life: https://www.rowan.edu/campus_life/"
                                                    "\nThe Arts At Rowan: https://www.rowan.edu/campus_life/arts.html"
                                                    "\nAthletics & Sports Recreation: https://www.rowan.edu/campus_life/atheletics_sports.html"
                                                    "\nHealth & Safety: https://www.rowan.edu/campus_life/health_safety.html"
                                                    "\nHousing & Dining: https://www.rowan.edu/campus_life/housing_dining.html"
                                                    "\nTechnology On Campus (Information Resources & Technology): https://irt.rowan.edu/"
                                                    "\nEntertainment & Culture: https://www.rowan.edu/campus_life/entert_culture.html"
                                                    "\nCenter For Well-Being: https://sites.rowan.edu/center-for-well-being/")
        elif choice == "health_medicine":
            await interaction.response.send_message("Home page for Health & Medicine: https://www.rowan.edu/health_medicine/"
                                                    "\nCooper Medical School of Rowan University (MD): https://cmsru.rowan.edu/"
                                                    "\nVirtua Health College of Medicine & Life Sciences (DO): https://sites.rowan.edu/vhc/"
                                                    "\nShreiber School of Veterinary Medicine (DVM): https://svm.rowan.edu/")
        elif choice == "research":
            await interaction.response.send_message("Home page for Research: https://research.rowan.edu/"
                                                    "\nOffice Of Research: https://research.rowan.edu/officeofresearch/"
                                                    "\nResearch Centers & Institutes: https://research.rowan.edu/centers/"
                                                    "\nSouth Jersey Technology Park: http://sjtechpark.org/"
                                                    "\nResearch News: https://today.rowan.edu/news/topics/research.html")
        elif choice == "military":
            await interaction.response.send_message("Home page for Military/Veterans: https://sites.rowan.edu/military/")
        elif choice == "thrive":
            await interaction.response.send_message("Home page for Thrive: https://sites.rowan.edu/center-for-well-being/thrive/")
        elif choice == "about":
            await interaction.response.send_message("Home page for About Rowan: https://www.rowan.edu/about/"
                                                    "\nLeadership: https://www.rowan.edu/about/leadership.html"
                                                    "\nRowan's Past, Present, & Future: https://www.rowan.edu/about/oppaf/"
                                                    "\nVisiting Rowan: https://www.rowan.edu/about/visiting/"
                                                    "\nWorking At Rowan: https://www.rowan.edu/about/working.html"
                                                    "\nRowan Fast Facts: https://sites.rowan.edu/fastfacts/"
                                                    "\nGiving To Rowan: https://www.rowan.edu/about/giving.html"
                                                    "\nNews & Events: https://today.rowan.edu/"
                                                    "\nContact Rowan: https://www.rowan.edu/about/contact.html")
        elif choice == "section_tally":
            await interaction.response.send_message("Link to New Section Tally (Much easier to use for people new to Section Tally): https://sectiontally.rowan.edu/"
                                                    "\nLink to Old Section Tally: https://banner.rowan.edu/reports/reports.pl?task=Section_Tally&old=1")
        elif choice == "survey":
            await interaction.response.send_message("Link to feedback survey: https://forms.gle/kaMWSJP5fbGqGe7Q7")
