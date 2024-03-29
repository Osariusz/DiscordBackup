FROM python:3.11.2
WORKDIR /src
ADD . /src
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "src/main.py"]
