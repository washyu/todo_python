# Use the official Python image from the Docker Hub
FROM python:3.10-slim AS base

# Set the working directory in the container
WORKDIR /workspace

# Copy the requirements file into the container
COPY app/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY app/ ./app/

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Copy the React application code into the container
COPY vite_todo_app/ ./vite_todo_app/

# Build the React app
RUN cd vite_todo_app && npm install && npm run build

# Use a multi-stage build to keep the final image small
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy the built React app from the previous stage
COPY --from=base /workspace/vite_todo_app/build ./vite_todo_app/build

# Copy the FastAPI application code from the previous stage
COPY --from=base /workspace/app ./app

# Install the dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install a simple HTTP server to serve the React app
RUN pip install fastapi uvicorn

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the default command to run when starting the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]