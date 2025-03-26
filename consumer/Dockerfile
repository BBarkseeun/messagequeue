# Python 3.9 이미지를 기반으로 한다.
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# requirements.txt 파일을 복사하고 필요한 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 애플리케이션 실행
CMD ["python", "consumer.py"]

