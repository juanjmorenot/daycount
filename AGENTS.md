# Project Rules for AI Agents

## Do NOT rename `app.py`

The file `app.py` is the entry point required by **Streamlit Community Cloud** to load and deploy the app. Streamlit Community Cloud specifically looks for a file named `app.py` at the repository root.

- Never rename, move, or delete `app.py`.
- Any AI-executed change (refactors, reorganizations, renames) MUST keep the main Streamlit application in a file named exactly `app.py` at the project root.
- If the application logic is split into modules, import them from `app.py`; do not rename `app.py` to another file (e.g. `main.py`, `streamlit_app.py`).
- Renaming `app.py` will break the deployed page on Streamlit Community Cloud.
