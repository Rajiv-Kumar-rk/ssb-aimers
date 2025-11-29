# SSB TAT Preparation (ssb-prep)

Lightweight Streamlit app to practice Thematic Apperception Test (TAT) tasks for SSB preparation. The app can generate suggested stories from images and evaluate candidate-written stories across Officer-Like Qualities (OLQs) using a Google Generative AI (Gemini) adapter via LangChain.

Quick features:
- Upload or randomly pick images from `tat_images/` and generate TAT-style stories.
- Automated evaluation with structured output (OLQ scores, image–story relevance, psychological summary).
- Modular prompt/chain code in `chains/` and Pydantic response schemas in `schemas/`.

Getting started (Windows / PowerShell):

1. Install dependencies using Pipenv (Pipfile is included):
```powershell
pipenv install
```

2. Create a `.env` file at the project root with your Gemini API key (the adapter reads `GEMINI_API_KEY`):
```
GEMINI_API_KEY=your_api_key_here
```

3. Run the app:
```powershell
pipenv run streamlit run app.py
```

Notes and recommendations:
- The LangChain / Google GenAI adapter expects compatible `langchain`/`langchain-google-genai` packages. If you run into API mismatches, check the installed package versions.
- Uploaded images are limited to 5 MB by the UI. If you add new images, place them in `tat_images/`.
- For development, consider pinning exact dependency versions in `Pipfile.lock` and adding tests around chains and the adapter.

License: project has no license file in this repo; add one if you plan to publish.
