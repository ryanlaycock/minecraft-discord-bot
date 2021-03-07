FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main.py ./

CMD [ "python", "-u", "main.py" ]