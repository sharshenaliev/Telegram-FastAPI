FROM python:3.10.6
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bot/registration_bot.py ./bot.py
COPY . .
EXPOSE 8000