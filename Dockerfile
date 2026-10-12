FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir 'gunicorn>=23,<24'
COPY app.py masking.py ./
COPY static ./static
RUN useradd --uid 10001 --create-home appuser
USER appuser
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 30 app:application"]
