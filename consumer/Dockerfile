# Python 3.9 슬림 이미지를 기반으로 한다
FROM python:3.9-slim

# 시스템 업데이트 및 tzdata 설치 (선택)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# 환경변수 설정 (로깅 등에 유용)
ENV PYTHONUNBUFFERED=1

# 실행 명령
CMD ["python", "consumer.py"]

