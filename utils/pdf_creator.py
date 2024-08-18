from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
import re

def parse_markdown(text):
    """Parse Markdown formatting and return formatted HTML."""
    # Replace bold and italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Replace headers (assuming we want to keep them as bold)
    text = re.sub(r'^#+ (.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    
    # Replace links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<link href="\2">\1</link>', text)
    
    return text

def create_pdf(analysis, articles, recommendations, output_path):
    """Create a PDF report from the given content."""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    content = []

    # Title
    content.append(Paragraph("Blood Test Analysis Report", styles['Title']))
    content.append(Spacer(1, 12))

    # Blood Test Analysis
    content.append(Paragraph("Blood Test Analysis", styles['Heading1']))
    analysis_paragraphs = analysis.split('\n')
    for para in analysis_paragraphs:
        if para.strip():
            content.append(Paragraph(parse_markdown(para), styles['Normal']))
    content.append(Spacer(1, 12))

    # Relevant Articles
    content.append(Paragraph("Relevant Articles", styles['Heading1']))
    articles_list = articles.split('\n')
    for article in articles_list:
        if article.strip():
            content.append(Paragraph(parse_markdown(article), styles['Normal']))
    content.append(Spacer(1, 12))

    # Health Recommendations
    content.append(Paragraph("Health Recommendations", styles['Heading1']))
    recommendations_paragraphs = recommendations.split('\n')
    for para in recommendations_paragraphs:
        if para.strip():
            content.append(Paragraph(parse_markdown(para), styles['Normal']))

    doc.build(content)