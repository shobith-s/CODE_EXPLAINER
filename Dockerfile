FROM python:3.9 
WORKDIR /app 
COPY . . 
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["streamlit", "run", "scripts/run_app.py", "--server.port=8000"] 
