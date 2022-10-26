# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Warning: A port below 1024 has been exposed. This requires the image to run as a root user which is not a best practice.
# For more information, please refer to https://aka.ms/vscode-docker-python-user-rights`
EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ENV FLASK_APP=project

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

ENTRYPOINT [ "/bin/sh" ]

CMD ["python3", "-m", "venv", "auth"]
CMD ["source", "auth/bin/activate"]
CMD ["flask", "run"]