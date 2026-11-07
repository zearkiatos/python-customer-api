FROM python:3.13-alpine

RUN apk add --no-cache make

RUN addgroup -S appgroup -g 10001 && adduser -S -D -H -u 10001 -G appgroup appuser

WORKDIR /app
COPY --chown=appuser:appgroup . /app/

RUN make install

EXPOSE 8000

USER appuser

RUN make install

USER appuser

ENTRYPOINT ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]