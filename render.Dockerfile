FROM python:3.13-alpine

RUN apk add --no-cache make

RUN addgroup -S appgroup -g 10001 && adduser -S -D -H -u 10001 -G appgroup appuser

WORKDIR /app
COPY --chown=appuser:appgroup . /app/

RUN make install

EXPOSE 10000

USER appuser

RUN make install

USER appuser

CMD ["sh", "-c", "exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-10000}"]