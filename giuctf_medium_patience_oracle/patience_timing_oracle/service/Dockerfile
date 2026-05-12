FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000

CMD ["python", "-u", "app.py"]