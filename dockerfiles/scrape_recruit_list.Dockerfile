FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./scrape_recruit_list.py 2010 2021