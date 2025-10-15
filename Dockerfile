FROM python:3.11-slim

WORKDIR /app

# Install system deps for pip + clean install of Python deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

CMD ["python", "main.py"]
