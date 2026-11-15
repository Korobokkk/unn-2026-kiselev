FROM python:3.14-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY python_first_v_bot ./bot
CMD ["python", "-m", "bot"]
