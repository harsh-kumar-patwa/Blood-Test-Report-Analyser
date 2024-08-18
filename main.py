from crewai import Crew, Task
from utils.pdf_parser import PDFParser
from gemini.gemini_api import GoogleGeminiAPI
from agents.analysis_agent import BloodTestAnalysisAgent
from agents.search_agent import ArticleSearchAgent
from agents.recommendation_agent import HealthRecommendationAgent
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import re
import sys
from datetime import datetime

def convert_markdown_to_html(text):
    # Convert bold (**text**) to HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Convert italic (*text*) to HTML
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Convert bullet points
    text = re.sub(r'^\s*-\s', '• ', text, flags=re.MULTILINE)
    
    return text

def create_pdf(analysis_summary, articles, recommendations, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story = []
    
    # Title
    Story.append(Paragraph("Blood Test Report Analysis", styles['Title']))
    Story.append(Spacer(1, 12))
    
    # Date
    Story.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Analysis Summary
    Story.append(Paragraph("Analysis Summary:", styles['Heading2']))
    Story.append(Paragraph(convert_markdown_to_html(analysis_summary), styles['Justify']))
    Story.append(Spacer(1, 12))
    
    # Relevant Articles
    Story.append(Paragraph("Relevant Articles:", styles['Heading2']))
    for i, article in enumerate(articles, 1):
        Story.append(Paragraph(f"{i}. {article}", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Health Recommendations
    Story.append(Paragraph("Health Recommendations:", styles['Heading2']))
    Story.append(Paragraph(convert_markdown_to_html(recommendations), styles['Justify']))
    
    doc.build(Story)

def main():
    try:
        # Step 1: Parse PDF report
        pdf_file_path = "/home/harsh/Desktop/blood_test_report/WM17S.pdf"
        parser = PDFParser(pdf_file_path)
        text = parser.parse_text()
        
        if not text:
            print("Error: No text extracted from the PDF. Please check the PDF file.")
            return

        # Step 2: Initialize Google Gemini API
        gemini_api = GoogleGeminiAPI()

        # Step 3: Create agents
        analysis_agent = BloodTestAnalysisAgent(
            name="Blood Test Analyzer",
            goal="Analyze blood test reports and provide summaries",
            backstory="An expert in interpreting medical test results",
            verbose=True,
            allow_delegation=False,
            gemini_api=gemini_api
        )
        search_agent = ArticleSearchAgent(
            name="Article Searcher",
            goal="Find relevant health articles based on blood test analysis",
            backstory="A skilled researcher with vast knowledge of medical literature",
            verbose=True,
            allow_delegation=False,
            gemini_api=gemini_api
        )
        recommendation_agent = HealthRecommendationAgent(
            name="Health Recommender",
            goal="Generate health recommendations based on blood test results and relevant articles",
            backstory="An experienced health advisor specializing in personalized recommendations",
            verbose=True,
            allow_delegation=False,
            gemini_api=gemini_api
        )

        # Step 4: Define tasks
        analyze_task = Task(
            description=text,
            agent=analysis_agent
        )

        search_task = Task(
            description="Search for relevant health articles based on the analysis summary",
            agent=search_agent
        )

        recommend_task = Task(
            description="Generate health recommendations based on the analysis and articles",
            agent=recommendation_agent
        )

        # Step 5: Create and run the crew
        crew = Crew(
            agents=[analysis_agent, search_agent, recommendation_agent],
            tasks=[analyze_task, search_task, recommend_task],
            verbose=2
        )
        result = crew.run()

        # Step 6: Extract results
        analysis_summary = result[0]
        articles = result[1]
        recommendations = result[2]

        # Step 7: Generate PDF report
        output_pdf_path = "/home/harsh/Desktop/blood_test_report/analysis_report.pdf"
        create_pdf(analysis_summary, articles, recommendations, output_pdf_path)
        print(f"\nPDF report generated and saved to: {output_pdf_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()