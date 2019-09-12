FROM python:3.6.8
# Set the working directory to /app
WORKDIR /app

# Copy stuff
ADD ./app /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 57633

# Run when the container launches
CMD ["python", "app.py"]
