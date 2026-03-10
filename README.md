# Blood Test Report Analyser

This project uses AI to analyze blood test reports, search for relevant health articles, and generate health recommendations. It features a Streamlit frontend and a FastAPI backend.

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
├── app.py              # Streamlit frontend
├── server.py           # FastAPI backend
├── start.sh            # Script to start both backend and frontend
├── custom_LLM.py
├── main.py             # CLI version
└── requirements.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/harsh-kumar-patwa/Blood-Test-Report-Analyser
   cd Blood-Test-Report-Analyser
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web UI (Recommended)

Run the start script to launch both the backend and frontend:

```
./start.sh
```

This will:
1. Start the FastAPI backend on `http://localhost:8000`
2. Wait for the backend to be ready
3. Start the Streamlit frontend on `http://localhost:3000`

On the frontend:
1. Enter your three API keys (Gemini API Key, Search Web API Key, Search Engine ID) and click **Start**
2. Upload a blood test PDF report
3. Click **Analyse Report** and wait for the progress bar to complete
4. View the analysis, relevant articles, and health recommendations
5. Download the output PDF (named `<input-filename>-recommendation.pdf`)

Press `Ctrl+C` to stop both servers.

### CLI

Alternatively, create a `config.py` file with your API keys:
```python
GEMINI_API_KEY = "your_gemini_api_key_here"
SEARCH_WEB_KEY = "your_search_web_key_here"
SEARCH_WEB_ENGINE_ID = "your_search_engine_id_here"
```

Then run:
```
python main.py
```

## API Keys Required

- **Gemini API Key** - Google Gemini API key for AI analysis
- **Search Web API Key** - Google Custom Search API key for article search
- **Search Engine ID** - Google Custom Search Engine ID

## Components

- `app.py`: Streamlit frontend with API key configuration, PDF upload, progress bar, and results display
- `server.py`: FastAPI backend exposing `/analyse` and `/download` endpoints
- `start.sh`: Startup script that launches backend first, waits for it, then starts frontend
- `main.py`: CLI version of the analyser
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

## Approach Document
[Approach Doc](https://docs.google.com/document/d/1qswPhiAZiHuFvGDQlNAxWRFoS7MrNRlAeg1ZwoXzVZU/edit?usp=sharing)
