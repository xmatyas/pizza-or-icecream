FROM python:3.10.14-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Copy the application files
COPY . /app

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
