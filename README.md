# Eye Deep-Net — Retinal Disease Detection

**Project summary**  
Eye Deep-Net is an end-to-end retinal disease classification system built using Python and deep learning. It classifies OCT / fundus images into categories (Normal, CNV, DME, Drusen) using a CNN model and provides a simple web interface for inference.

**Tech stack**  
- Python, TensorFlow / Keras, OpenCV, NumPy, Pandas  
- Flask or Streamlit for web inference  
- Power BI (for analytics - optional)

**Files in this repo**
- `app.py` — Streamlit/Flask app for inference (upload image → get prediction)  
- `notebooks/` — preprocessing and training notebooks  
- `requirements.txt` — Python dependencies  
- `sample_images/` — sample inputs for testing  
- `outputs/` — sample outputs / screenshots from report  
- `model/weights_info.txt` — link to download full model weights if large

**How to run (local)**  
1. Create & activate Python virtual environment:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
2. Install dependencies:
pip install -r requirements.txt

3. Run the app (Streamlit):
streamlit run app.py

or Flask:
python app.py

4. Open the displayed local URL in your browser, upload a sample image and view predictions.

**Model weights**  
If model files are large, download weights using the link in `model/weights_info.txt`. The README describes how to place the weights file.

**Screenshots**  
See `outputs/` for model accuracy plots, confusion matrix and example input/output screenshots.

**Contact**  
Pulicheru Mythri — pulicherumythri2930@gmail.com  
GitHub: https://github.com/PulicheruMythri
