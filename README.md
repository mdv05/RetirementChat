# RetireChat

A retirement planning coach for early-career professionals. It answers retirement and financial-basics questions in plain language, asks about your age, savings and goals, and helps you put together a step-by-step plan.

**Live app:** https://mdv05-retirementchat-app-rgqcfx.streamlit.app/

RetireChat started as half of my team's winning intern project at Segal (summer 2025), paired with the [RetireHub](https://github.com/mdv05/RetirementHub) dashboard.

## How it works
- `app.py` is a single Streamlit app that sends the conversation to Google's Gemini API with a retirement-coach prompt (the prompt spec is in `GEMINI.md`).
- If the API errors out or a response is blocked, the app retries and then falls back to a short, helpful message instead of an error.

## Run it locally
```bash
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run app.py
```

Built with Python, Streamlit and the Gemini API. Hosted on Streamlit Community Cloud.
