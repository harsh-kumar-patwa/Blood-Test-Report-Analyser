# Blood Test Report Analyser 

This project uses AI to analyze blood test reports, search for relevant health articles, and generate health recommendations.

## Table of content
   - Project Structure
   - Setup
   - Usage
   - Components
   - [Approach Document](https://docs.google.com/document/d/1qswPhiAZiHuFvGDQlNAxWRFoS7MrNRlAeg1ZwoXzVZU/edit?usp=sharing)

## Project Structure

```
├── agents/
│   ├── base_agent.py
│   ├── analysis_agent.py
│   ├── recommendation_agent.py
│   └── search_agent.py
├── gemini/
│   └── gemini_api.py
├── utils/
│   ├── pdf_creator.py
│   └── pdf_parser.py
├── .gitignore
├── WM17S.pdf
├── custom_LLM.py
├── main.py
├── output.pdf
└── requirements.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/harsh-kumar-patwa/Blood-Test-Report-Analyser
   cd Blood-Test-Report-Analyser
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `config.py` file in the root directory with your API keys:
   ```python
   GEMINI_API_KEY = "your_gemini_api_key_here"
   SEARCH_WEB_KEY = "your_search_web_key_here"
   SEARCH_WEB_ENGINE_ID = "your_search_engine_id_here"
   ```


## Usage

Run the main script:

```
python main.py
```
This will prompt you to add input pdf file path , just add 

```
WM17S.pdf
```

At the end it will ask for output pdf file path , just add

```
ouput.pdf
```



This will:
1. Analyze the blood test report (WM17S.pdf)
2. Search for relevant health articles
3. Generate health recommendations
4. Create a PDF report (output.pdf) with the results

## Components

- `agents/`: Contains agent classes for the AI system
  - `base_agent.py`: Base class for all agents
  - `analysis_agent.py`: Agent for analyzing blood test reports
  - `recommendation_agent.py`: Agent for generating health recommendations
  - `search_agent.py`: Agent for searching relevant health articles
- `gemini/`: Handles interactions with the Gemini API
  - `gemini_api.py`: Implementation of Gemini API calls
- `utils/`: Utility functions for PDF handling
  - `pdf_creator.py`: Functions for creating the output PDF report
  - `pdf_parser.py`: Functions for parsing input PDF blood test reports
- `custom_LLM.py`: Custom language model implementation
- `main.py`: Main script orchestrating the analysis process

## Approach Document 
[Approach Doc](https://docs.google.com/document/d/1qswPhiAZiHuFvGDQlNAxWRFoS7MrNRlAeg1ZwoXzVZU/edit?usp=sharing)

