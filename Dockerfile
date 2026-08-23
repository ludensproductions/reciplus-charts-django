FROM issirmax/django:5.2-3.13-2.0

# Setup project's workdir and own requirements, and then copy
WORKDIR /app
COPY requirements.project.txt .
RUN pip install --no-cache-dir -r requirements.project.txt
COPY . .

# Expose port 8000
EXPOSE 8000
