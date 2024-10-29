# Dockerfile

FROM python:3.9-slim

# Install dependencies
RUN pip install requests ovh load_dotenv

# Copy files
COPY app /app

# Set working directory
WORKDIR /app

# Run
CMD ["python", "__main__.py"]