FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG BUILD_APP_PATH=/app
ENV APP_PATH=${BUILD_APP_PATH}
WORKDIR ${APP_PATH}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG BUILD_USER_NAME=django_user
ENV USER_NAME=${BUILD_USER_NAME}
RUN useradd -m ${USER_NAME} && \
    chmod +x ${APP_PATH}/entrypoint.sh && \
    chown -R ${USER_NAME}:${USER_NAME} ${APP_PATH}
    
USER ${USER_NAME}

ENTRYPOINT [ "./entrypoint.sh" ]

ENV PORT=8080

EXPOSE 8080

CMD [ "sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} testy_proj.wsgi:application" ]
