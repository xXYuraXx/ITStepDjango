FROM python:3.14-slim

ARG DOWNLOAD_PATH=/app
ENV APP_PATH=${DOWNLOAD_PATH}
WORKDIR ${APP_PATH}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PROJECT_USER_NAME=django_user
RUN useradd -m ${PROJECT_USER_NAME} && \
    chmod +x ${APP_PATH}/entrypoint.sh && \
    chown -R ${PROJECT_USER_NAME}:${PROJECT_USER_NAME} ${APP_PATH}
    
USER ${PROJECT_USER_NAME}

ENTRYPOINT [ "./entrypoint.sh" ]

ENV SITE_PORT=8000
CMD [ "sh", "-c", "exec python manage.py runserver 0.0.0.0:${SITE_PORT}" ]