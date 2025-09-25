import os
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY, temperature=1)


def get_career_path(reformatted_question):
    path_generation_prompt = """**Prompt for AI Assessment of Student Interests in Academic Streams**
    
    You are tasked with developing an AI system that evaluates a student's interests and aptitudes based on their responses to a set of 10 multiple-choice questions. Each question is designed to reveal the student's natural inclinations towards specific academic streams: Arts, Science, Commerce, or Vocational. The AI will analyze the answers, assign points to each option based on the associated stream, and ultimately recommend the most suitable academic pathway based on the highest score.
    
    **Instructions:**
    
    1. **Input Format:** 
       - The AI will receive the student's answers to 10 predefined questions in a structured format (e.g., a list or dictionary).
       - Each answer corresponds to one of four categories: Science, Arts, Commerce, or Vocational.
    
    2. **Scoring System:**
       - Each answer option should be associated with a specific stream and assigned points as follows:
         - Science: 3 points
         - Arts: 3 points
         - Commerce: 3 points
         - Vocational: 3 points
       - The points can vary based on the perceived strength of the inclination (e.g., primary choice could get 3 points, secondary 2, and tertiary 1).
    
    3. **Processing Logic:**
       - For each answer, tally points for the corresponding streams.
       - After processing all answers, compare the total scores of each stream.
    
    4. **Recommendation Output:**
       - Include a brief description of potential career paths associated with the recommended stream.
       - Don't Show the scores allocated to each stream but use it behind the scenes to evaluate choices
    
    5. **Response Format:**
       - Present the output in a structured dictionary format starting with [] or {}:
         - **Recommended Stream:** [Stream Name]
         - **Career Paths:** [Brief list of potential careers and a short introduction to them in dictionary format with keys(title,description)]
    
    **Example Questions:**
    1. If you had to choose a fun project for the weekend, what would it be?
    2. Which section of a newspaper do you read most often?
    3. When faced with a complex problem, what is your first instinct?
    4. Which of these tasks sounds the most satisfying?
    5. Imagine you are part of a team creating a new mobile app. What role would you love to play?
    6. What kind of questions do you ask most often?
    7. If you were to watch a documentary, which topic would you pick?
    8. In school, which type of assignment do you enjoy the most?
    9. What do you value most in a future career?
    10. You are given ₹5,000 to start a small project. What would you do?
    
    **End of Prompt**"""

    prompt = ChatPromptTemplate.from_messages([SystemMessage(content=path_generation_prompt),
                                               ("user", "{input}")])

    chain = prompt | llm | JsonOutputParser()
    response = chain.invoke({"input": reformatted_question})
    print(response)
    return response


def get_roadmap(pathway_selected):
    roadmap_generation_prompt = """
    **Prompt:**

    Given the user's input, analyze their interests and skills to recommend an appropriate academic stream. Structure the output as follows:

    User Input Structure Below:
    - **Recommended Stream:** [Stream Name]
    - **Total Scores:**
      - Science: [Score]
      - Arts: [Score]
      - Commerce: [Score]
      - Vocational: [Score]
    - **Career Paths:** [Brief list of potential careers]

    Once the user selects a career path from the suggested list, provide a detailed roadmap that includes in a dictionary format with keys(heading,pointers,learning_resource,skills,scope) respectively:

    1. **heading:** [Career Path Title]
    2. **pointers:**
       - [Key point 1]
       - [Key point 2]
       - [Key point 3]
    3. **learning_resource:**
       - [Resource 1: title and link in a dictionary format with keys(title,link)]
    4. **skills_to_develop:**
       - [Skill 1]
       - [Skill 2]
       - [Skill 3]
    5. **scope:**
       - Brief description of job_market, growth_opportunities, and salary_range(always return in a string) in a dictionary format with appropriate keys

    Ensure that each section is concise, informative, and tailored to the specific career path chosen by the user."""

    prompt = ChatPromptTemplate.from_messages([SystemMessage(content=roadmap_generation_prompt),
                                                ("user", "{input}")])
    chain = prompt | llm | JsonOutputParser()
    response = chain.invoke({"input": pathway_selected})
    print(response)
    return response
