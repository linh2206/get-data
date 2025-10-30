# FFprobe UDP Stream Analyzer API

FastAPI application để phân tích UDP stream sử dụng ffprobe.

## Tính năng

- API REST để probe UDP stream
- Xác thực bằng API Key
- Trả về thông tin chi tiết về stream (format, programs, streams, chapters)
- Hỗ trợ Docker để dễ dàng triển khai
- Auto-generated API documentation (Swagger UI)

## Cài đặt

### Cách 1: Chạy trực tiếp với Python

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/get-data.git
cd get-data

# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt ffmpeg/ffprobe (nếu chưa có)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Chạy server
python main.py
```

Server sẽ chạy tại: http://localhost:8000

### Cách 2: Chạy với Docker

```bash
# Build và chạy
docker-compose up --build

# Chạy ở background
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

Server sẽ chạy tại: http://localhost:8000

## API Endpoints

### 1. Root - `GET /`
Thông tin về API

### 2. Health Check - `GET /health`
Kiểm tra trạng thái server

### 3. Probe Stream - `POST /probe`
Phân tích UDP stream

**Headers:**
- `X-API-Key`: your-secret-api-key-here

**Request Body:**
```json
{
  "ip": "232.1.1.172",
  "port": 10172
}
```

**Response:**
```json
{
  "success": true,
  "udp_url": "udp://232.1.1.172:10172",
  "data": {
    "streams": [...],
    "programs": [...],
    "format": {...}
  }
}
```

## Sử dụng API

### Với cURL:

```bash
curl -X POST "http://localhost:8000/probe" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"ip": "232.1.1.172", "port": 10172}'
```

### Với Python:

```python
import requests

url = "http://localhost:8000/probe"
headers = {
    "X-API-Key": "your-secret-api-key-here",
    "Content-Type": "application/json"
}
data = {
    "ip": "232.1.1.172",
    "port": 10172
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## API Documentation

Sau khi chạy server, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Cấu hình

### Thay đổi API Key

Trong file `main.py`, dòng 11:
```python
API_KEY = "your-secret-api-key-here"  # Đổi thành API key của bạn
```

### Thay đổi Port

Trong file `main.py`, dòng 145:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Đổi port nếu cần
```

Hoặc trong `docker-compose.yml`:
```yaml
ports:
  - "8000:8000"  # host_port:container_port
```

## Cấu trúc thư mục

```
get-data/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker compose configuration
├── .gitignore         # Git ignore rules
├── .dockerignore      # Docker ignore rules
└── README.md          # Documentation
```

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- FFmpeg/FFprobe

Hoặc:
- Docker & Docker Compose

## Troubleshooting

### Lỗi "ffprobe not found"
Cài đặt ffmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### Lỗi "Invalid API Key"
Kiểm tra header `X-API-Key` trong request phải khớp với API_KEY trong `main.py`

### Timeout
Tăng timeout trong `main.py` dòng 99:
```python
timeout=30  # Tăng số giây nếu cần
```

## License

MIT
