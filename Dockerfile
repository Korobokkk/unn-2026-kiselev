FROM python:3.14-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY new_bot/ ./new_bot
CMD ["python", "-m", "new_bot"]
