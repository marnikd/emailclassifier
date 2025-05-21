# base image
FROM python:3.11

# working directory
WORKDIR /app

# copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy wheel file
COPY pipple_template-1.0-py3-none-any.whl .

# install the wheel file
RUN pip install pipple_template-1.0-py3-none-any.whl

# install nltk data
RUN python -m nltk.downloader punkt_tab

# copy the rest of app code
COPY . .

# expose the port and start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
