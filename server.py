from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from pathlib import Path

from utils.pdf_parser import PDFParser
from gemini.gemini_api import GoogleGeminiAPI
from custom_LLM import GeminiLLM
from crewai import Agent, Task, Crew
from utils.pdf_creator import create_pdf

app = FastAPI(title="Blood Test Report Analyser API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyse")
def analyse_report(
    file: UploadFile = File(...),
    gemini_api_key: str = Form(...),
    search_web_key: str = Form(...),
    search_engine_id: str = Form(...),
):
    # Save uploaded PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        # Step 1: Parse PDF
        parser = PDFParser(tmp_path)
        text = parser.parse_text()

        if not text:
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF. Please check the file.")

        # Step 2: Initialize API and LLM
        gemini_api = GoogleGeminiAPI(
            gemini_api_key=gemini_api_key,
            search_web_key=search_web_key,
            search_engine_id=search_engine_id,
        )
        custom_llm = GeminiLLM(gemini_api)

        # Step 3: Create agents
        analysis_agent = Agent(
            role="Blood Test Analyzer",
            goal="Analyze the blood test report and provide a summary that is understandable to a person without medical knowledge. Also make the summary short and simple",
            backstory="A normal human is interpreting medical test results with no experience in clinical diagnostics.",
            verbose=False,
            allow_delegation=False,
            llm=custom_llm,
        )

        search_agent = Agent(
            role="Medical Article Researcher",
            goal="Find relevant health articles based on blood test analysis",
            backstory="A normal human with less knowledge of medical literature.",
            verbose=False,
            allow_delegation=False,
            llm=custom_llm,
        )

        recommendation_agent = Agent(
            role="Health Advisor",
            goal="Generate health recommendations based on blood test results and relevant articles",
            backstory="An experienced health advisor specializing in personalized recommendations, with a background in integrative medicine.",
            verbose=False,
            allow_delegation=False,
            llm=custom_llm,
        )

        # Step 4: Define tasks
        analyze_task = Task(
            description=f"Analyze the following blood test report and provide a summary that is understandable to a person without medical knowledge. Also make the summary short and simple  {text}",
            agent=analysis_agent,
            expected_output="A short summary of analysis of the blood test results, highlighting any abnormalities or areas of concern with short.",
        )

        search_task = Task(
            description="Based on the blood test analysis provided, search for 5 relevant health articles. Provide titles and URLs.",
            agent=search_agent,
            expected_output="A list of 5 relevant health articles with their titles and URLs, related to the findings in the blood test analysis.",
            context=[analyze_task],
        )

        recommend_task = Task(
            description="Based on the blood test analysis and the found articles, generate actionable health recommendations.",
            agent=recommendation_agent,
            expected_output="A set of actionable health recommendations based on the blood test analysis and information from the relevant articles.",
            context=[analyze_task, search_task],
        )

        # Step 5: Run the crew
        crew = Crew(
            agents=[analysis_agent, search_agent, recommendation_agent],
            tasks=[analyze_task, search_task, recommend_task],
            verbose=False,
        )
        result = crew.kickoff()

        # Step 6: Extract results
        if hasattr(result, "tasks_output"):
            analysis_text = result.tasks_output[0].raw_output
            articles_text = result.tasks_output[1].raw_output
            recommendations_text = result.tasks_output[2].raw_output
        else:
            result_str = str(result)
            analysis_text = (
                analyze_task.output.raw_output
                if hasattr(analyze_task, "output") and analyze_task.output
                else result_str
            )
            articles_text = (
                search_task.output.raw_output
                if hasattr(search_task, "output") and search_task.output
                else ""
            )
            recommendations_text = (
                recommend_task.output.raw_output
                if hasattr(recommend_task, "output") and recommend_task.output
                else ""
            )

        # Step 7: Generate output PDF
        input_filename = Path(file.filename).stem
        output_filename = f"{input_filename}-recommendation.pdf"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as out_tmp:
            output_path = out_tmp.name

        create_pdf(analysis_text, articles_text, recommendations_text, output_path)

        return {
            "analysis": analysis_text,
            "articles": articles_text,
            "recommendations": recommendations_text,
            "pdf_path": output_path,
            "output_filename": output_filename,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.get("/download")
def download_pdf(path: str, filename: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="PDF not found. It may have expired.")
    return FileResponse(path, media_type="application/pdf", filename=filename)
