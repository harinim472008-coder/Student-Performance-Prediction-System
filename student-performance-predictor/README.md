# Student Performance Predictor

This project predicts a student's final score using:
- Attendance percentage
- Study hours per day
- Previous grade percentage

It includes:
- A Python backend with Flask API
- Data handling with Pandas
- Numerical/model computations with NumPy
- A simple HTML/CSS/JavaScript dashboard

## Project Structure

```text
student-performance-predictor/
|- app.py
|- model.py
|- preprocessing.py
|- requirements.txt
|- data/
|  |- student_data.csv
|- templates/
|  |- index.html
|- static/
   |- styles.css
   |- app.js
```

## Setup

1. Open a terminal in the project directory.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## API Endpoints

- `GET /api/health` - service health check
- `GET /api/summary` - model and dataset statistics
- `POST /api/predict` - predict final score

### Example Predict Request

```json
{
  "attendance": 88,
  "study_hours": 3.5,
  "previous_grades": 79
}
```

### Example Predict Response

```json
{
  "predicted_score": 81.62,
  "performance_band": "Good",
  "input": {
    "attendance": 88.0,
    "study_hours": 3.5,
    "previous_grades": 79.0
  }
}
```
