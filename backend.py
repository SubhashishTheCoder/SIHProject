import os
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash", google_api_key=API_KEY,temperature = 1)

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
     - **Career Paths:** [Brief list of potential careers and a short introduction to them]

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

with open('questions.json',encoding="utf8") as file:
    questions = json.load(file)


for question in questions:
    print(question["question"])
    for item in question["options"].keys():
        print(f"{item}. {question["options"][item]}")
    user_choice = input("Your Answer: ")
    question["answer"] = question["options"][user_choice]

reformated_question = [f"{question["question"]} -> {question["answer"]}" for question in questions]

response = chain.invoke({"input": reformated_question})

print(response)
career_path = input("Choose any of the above mentioned career path \n")

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

Once the user selects a career path from the suggested list, provide a detailed roadmap that includes in a dictionary format with appropriate key:

1. **Heading:** [Career Path Title]
2. **Pointers:** 
   - [Key point 1]
   - [Key point 2]
   - [Key point 3]
3. **Learning Resources:** 
   - [Resource 1: Title and link]
   - [Resource 2: Title and link]
   - [Resource 3: Title and link]
4. **Skills to Develop:** 
   - [Skill 1]
   - [Skill 2]
   - [Skill 3]
5. **Scope:** 
   - [Brief description of job market, growth opportunities, and potential salary range]

Ensure that each section is concise, informative, and tailored to the specific career path chosen by the user."""

prompt2 = ChatPromptTemplate.from_messages([SystemMessage(content=roadmap_generation_prompt),
                                           ("user", "{input}")])


chain2 = prompt2 | llm | JsonOutputParser()

response["Career Path Opted"] = career_path

print(response)
response2  = chain2.invoke({"input":response})
print(response2)

