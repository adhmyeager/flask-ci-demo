FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ ./app/

# Expose and run
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "app:create_app", "run", \
     "--host=0.0.0.0", "--port=5000"]