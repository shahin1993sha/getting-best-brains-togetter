import os
import JobDescAndResumeProcessing as jp

resumeList = os.listdir('data/Input/Resumes/')
print('Resume List', resumeList)

data_jd_title, data_jd_desc = jp.scrape_job_details()

percentage_details = dict({})

for resume in resumeList:
    resume_filename = 'data/Input/Resumes/' + str(resume)
    data_resume = jp.data_load(resume_filename, resume)
    # print("Resume Data : {} ", data_resume)
    keywords_resume = jp.nltk_keywords(data_resume)
    print("Keywords in Resume : {} ", keywords_resume)

    # print(" Job Description from web page {}", data_jd_desc)

    keywords_jd = jp.nltk_keywords(data_jd_desc)
    print("Keywords in JD : {} ", keywords_jd)

    # skills = jp.load_skills_dataset(
    #     'C:\\Users\\shahi\\PycharmProjects\\GettingBestBrainsTogether\\getting-best-brains-togetter\\data\\ruleDictionary\\Skills.csv')

    skills = jp.load_skills_dataset('data/ruleDictionary/Skills.csv')

    matchedJDKeywords = jp.matchKeywords(keywords_jd, skills)

    print("matched keywords in JD  : {}", matchedJDKeywords)

    matchedResumeKeywords = jp.matchKeywords(keywords_resume, matchedJDKeywords)

    print("matched keywords in matchedResumeKeywords  : {}", matchedResumeKeywords)
    # matchedJDKeywords = jp.matchKeywords(keywords_jd, skills)

    print("matched percentage for resume against JD ")

    match_score = (len(matchedResumeKeywords) / len(matchedJDKeywords)) * 100
    matchPercentage = round(match_score, 2)
    print("Matched percentage : {} for file {}", matchPercentage, resume)
    if matchPercentage > 30:
        percentage_details[resume] = matchPercentage

print("shortlisted resume : {}", percentage_details)

jp.plot_radar_chart(percentage_details)