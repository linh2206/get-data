# FFprobe UDP Stream Analyzer API

API Python để phân tích UDP stream sử dụng ffprobe với xác thực API key.

## Yêu cầu

- Python 3.8+
- ffmpeg/ffprobe đã cài đặt trên hệ thống

### Cài đặt ffprobe

**MacOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Tải từ https://ffmpeg.org/download.html

## Cài đặt

1. Cài đặt các thư viện Python:
```bash
pip install -r requirements.txt
```

2. Thay đổi API key trong file `main.py`:
```python
API_KEY = "your-secret-api-key-here"
```

## Chạy API

```bash
python main.py
```

hoặc:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API sẽ chạy tại: `http://localhost:8000`

## Sử dụng

### 1. Kiểm tra API

```bash
curl http://localhost:8000/health
```

### 2. Probe UDP Stream

**Request:**
```bash
curl -X POST "http://localhost:8000/probe" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "ip": "232.1.1.172",
    "port": 10172
  }'
```

**Response (thành công):**
```json
{
  "success": true,
  "udp_url": "udp://232.1.1.172:10172",
  "data": {
    "streams": [...],
    "format": {...},
    "programs": [...],
    "chapters": [...]
  }
}
```

**Response (lỗi):**
```json
{
  "success": false,
  "udp_url": "udp://232.1.1.172:10172",
  "error": "ffprobe error: ..."
}
```

## API Documentation

Sau khi chạy server, truy cập:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

- `GET /` - Thông tin API
- `GET /health` - Health check
- `POST /probe` - Phân tích UDP stream (cần API key)

## Xác thực

Tất cả requests đến `/probe` cần header `X-API-Key`:

```
X-API-Key: your-secret-api-key-here
```

## Ví dụ với Python

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
result = response.json()

if result["success"]:
    print("Streams:", result["data"]["streams"])
    print("Format:", result["data"]["format"])
else:
    print("Error:", result["error"])
```

## Cấu hình

- **Timeout**: Mặc định 30 giây cho mỗi ffprobe request
- **Port**: Mặc định 8000 (có thể thay đổi trong `main.py`)
- **API Key**: Cần thay đổi trong `main.py`

