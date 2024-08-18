from crewai import Agent, Task, Crew
from utils.pdf_parser import PDFParser
from gemini.gemini_api import GoogleGeminiAPI
from custom_LLM import GeminiLLM
import sys

def main():
    try:
        # Step 1: Parse PDF report
        pdf_file_path = "/home/harsh/Desktop/blood_test_report/WM17S.pdf"
        parser = PDFParser(pdf_file_path)
        text = parser.parse_text()
        
        if not text:
            print("Error: No text extracted from the PDF. Please check the PDF file.")
            return

        # Step 2: Initialize Google Gemini API and custom LLM
        gemini_api = GoogleGeminiAPI()
        custom_llm = GeminiLLM(gemini_api)

        # Step 3: Create agents
        analysis_agent = Agent(
            role="Blood Test Analyzer",
            goal="Analyze blood test reports and provide detailed summaries",
            backstory="An expert in interpreting medical test results with years of experience in clinical diagnostics.",
            verbose=True,
            allow_delegation=False,
            llm=custom_llm
        )

        search_agent = Agent(
            role="Medical Article Researcher",
            goal="Find relevant health articles based on blood test analysis",
            backstory="A skilled researcher with vast knowledge of medical literature and access to extensive medical databases.",
            verbose=True,
            allow_delegation=False,
            llm=custom_llm
        )

        recommendation_agent = Agent(
            role="Health Advisor",
            goal="Generate health recommendations based on blood test results and relevant articles",
            backstory="An experienced health advisor specializing in personalized recommendations, with a background in integrative medicine.",
            verbose=True,
            allow_delegation=False,
            llm=custom_llm
        )

        # Step 4: Define tasks
        analyze_task = Task(
            description=f"Analyze the following blood test report and provide a detailed summary: {text}",
            agent=analysis_agent,
            expected_output="A comprehensive analysis of the blood test results, highlighting any abnormalities or areas of concern."
        )

        search_task = Task(
            description="Search for 5 relevant health articles based on the blood test analysis. Provide titles and URLs.",
            agent=search_agent,
            expected_output="A list of 5 relevant health articles with their titles and URLs, related to the findings in the blood test analysis."
        )

        recommend_task = Task(
            description="Generate health recommendations based on the blood test analysis and the found articles.",
            agent=recommendation_agent,
            expected_output="A set of actionable health recommendations based on the blood test analysis and information from the relevant articles."
        )

        # Step 5: Create and run the crew
        crew = Crew(
            agents=[analysis_agent, search_agent, recommendation_agent],
            tasks=[analyze_task, search_task, recommend_task],
            verbose=True
        )
        result = crew.kickoff()

        # Step 6: Display results
        for i, task_output in enumerate(result.tasks_output):
            print(f"\n--- Task {i+1} Output ---")
            print(f"Output:\n{task_output.raw}")
            print("-" * 50)

        # Step 6: Display results
        # print("Blood Test Analysis:")
        # print(results[0])
        # print("\nRelevant Articles:")
        # print(results[1])
        # print("\nHealth Recommendations:")
        # print(results[2])

    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()