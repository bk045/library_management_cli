FROM python:3.10-alpine
RUN addgroup app && adduser -S -G app app
COPY . /code
# Changes group to app for code and its all contents.
RUN chgrp -R app code
# Changes rights to rwx for assigned group for code folder and all its contents.
RUN chmod -R g=rwx code
# Sets user to app user
USER app
# Changes working directory to appFile.
WORKDIR /code/appFiles/
CMD python main.py