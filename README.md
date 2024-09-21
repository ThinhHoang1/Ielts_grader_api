# Project Structure

#### ielts_grader_api/
#### ├── app/
#### │   ├── __init__.py
#### │   ├── main.py
#### │   ├── models.py
#### │   ├── config.py
#### │   └── grader.py
#### ├── .env
#### ├── requirements.txt
#### └── README.md


## Requirements

- Python 3.9 or higher
- pip (Python package installer)
## Install the dependencies:
```bash
- pip install -r requirements.txt
```
## Running the Application Locally
```bash
uvicorn app.main:app --reload

```
- The application will start at http://127.0.0.1:8000/.
- You can access the interactive API documentation at http://127.0.0.1:8000/docs.
  
