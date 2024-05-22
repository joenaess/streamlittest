# Use a suitable Python base image with Streamlit pre-installed
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /

# Copy the app's requirements file
COPY requirements.txt requirements.txt

# Copy the app's secrets.toml with api_key to groq
COPY secrets.toml /root/.streamlit/secrets.toml

# Install the app's Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your Streamlit application's code
COPY . .

# Copy the secrets file
COPY secrets.toml /app/secrets.toml

# Expose the port Streamlit uses by default
EXPOSE 8501

# Define the command to run when the container starts
CMD ["streamlit", "run", "./app/app.py"]

# Alternative run if testing gaudi_mixtral on intel servers
#CMD ["streamlit", "run", "./app/app_gaudi.py"]