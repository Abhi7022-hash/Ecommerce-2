# Stage-1 Builder
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#Stage-2 Runtime Stage
FROm python:3.11 AS runtime 
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app.py .
EXPOSE 5003
CMD ["python" , "app.py"]
