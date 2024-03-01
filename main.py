import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import JobDescAndResumeProcessing as jp

# Create the main application window
root = tk.Tk()
root.title("Skills Matcher Tool")
root.geometry("1000x800")

# Global variables for storing candidate match scores
candidate_names = []
match_scores_values = []
initial_candidate_names = []
initial_match_scores_values = []

# Get JD test and extract words and match with skills
data_jd_title, data_jd_desc = jp.scrape_job_details()
keywords_jd = jp.nltk_keywords(data_jd_desc)
print("Keywords in JD : {} ", keywords_jd)
skills = jp.load_skills_dataset('data/ruleDictionary/Skills.csv')
matchedJDKeywords = jp.matchKeywords(keywords_jd, skills)
resumeList = []
percentage_details = dict({})


def matchSkills():
    resumeList = os.listdir('data/Input/Resumes/')
    print('Resume List', resumeList)

    for resume in resumeList:
        resume_filename = 'data/Input/Resumes/' + str(resume)
        data_resume = jp.data_load(resume_filename, resume)
        # print("Resume Data : {} ", data_resume)
        keywords_resume = jp.nltk_keywords(data_resume)
        print("Keywords in Resume : {} ", keywords_resume)
        print("matched keywords in JD  : {}", matchedJDKeywords)
        matchedResumeKeywords = jp.matchKeywords(keywords_resume, matchedJDKeywords)
        print("matched keywords in matchedResumeKeywords  : {}", matchedResumeKeywords)
        print("matched percentage for resume against JD ")
        match_score = (len(matchedResumeKeywords) / len(matchedJDKeywords)) * 100
        matchPercentage = round(match_score, 2)
        print("Matched percentage : {} for file {}", matchPercentage, resume)

        if matchPercentage >= 30:
            percentage_details[resume] = matchPercentage

    print("shortlisted resume : {}", percentage_details)
    initial_candidate_names = list(percentage_details.keys())
    initial_match_scores_values = list(percentage_details.values())
    plot_radar(initial_candidate_names, initial_match_scores_values)


# Function to regenerate match score
def regenerate_match_score():
    matchSkills()


# Function to display job description
def display_job_description():
    job_title_label.config(text=data_jd_title)
    job_description_text.delete('1.0', tk.END)
    job_description_text.insert(tk.END, data_jd_desc)


# Function to plot radar chart
def plot_radar(candidate_names, match_scores_values):
    # Clear the existing plot if it exists
    for widget in radar_frame.winfo_children():
        widget.destroy()

    # Abbreviate candidate names
    abbreviated_names = [name[:10] + '...' if len(name) > 10 else name for name in candidate_names]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(abbreviated_names, match_scores_values, color='skyblue')
    ax.set_title('Best Fit Candidates', fontsize=14)  # Set title font size
    ax.set_xlabel('Candidates', fontsize=10)  # Set x-axis label font size
    ax.set_ylabel('Match Score (%)', fontsize=10)  # Set y-axis label font size
    ax.set_ylim(0, 100)
    ax.set_xticklabels(abbreviated_names, rotation=45,
                       fontsize=8)  # Set x-axis tick label font size and rotation
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=radar_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Function to upload a PDF file
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            # Save the uploaded file to the Resumes folder
            destination = os.path.join('data/Input/Resumes', os.path.basename(file_path))
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            os.rename(file_path, destination)
            messagebox.showinfo("Success", "PDF uploaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Frame for displaying job description
jd_frame = tk.Frame(root)
jd_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

job_title_label = tk.Label(jd_frame, text=data_jd_title, font=('Helvetica', 16, 'bold'))
job_title_label.pack(anchor=tk.W)

job_description_text = tk.Text(jd_frame, height=10, wrap=tk.WORD)
job_description_text.pack(fill=tk.BOTH, expand=True)

display_job_description()

# Frame for uploading PDF and regenerating match score
upload_frame = tk.Frame(root)
upload_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

upload_button = tk.Button(upload_frame, text="Upload PDF", command=upload_pdf)
upload_button.pack(side=tk.LEFT)

regenerate_button = tk.Button(upload_frame, text="Regenerate Match Score", command=regenerate_match_score)
regenerate_button.pack(side=tk.LEFT, padx=(10, 0))

# Frame for displaying radar chart
radar_frame = tk.Frame(root)
radar_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
matchSkills()

root.mainloop()
