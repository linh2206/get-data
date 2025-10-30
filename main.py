from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator
import subprocess
import json
from typing import Optional

app = FastAPI(title="FFprobe UDP Stream Analyzer API")

# API Key configuration
API_KEY = "your-secret-api-key-here"  # Change this to your actual API key
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


class StreamRequest(BaseModel):
    ip: str = Field(..., description="UDP stream IP address", example="232.1.1.172")
    port: int = Field(..., description="UDP stream port", ge=1, le=65535, example=10172)
    
    @validator('ip')
    def validate_ip(cls, v):
        # Basic IP validation
        parts = v.split('.')
        if len(parts) != 4:
            raise ValueError('Invalid IP address format')
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                raise ValueError('Invalid IP address')
        return v


class StreamResponse(BaseModel):
    success: bool
    udp_url: str
    data: Optional[dict] = None
    error: Optional[str] = None


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify the API key from request header"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FFprobe UDP Stream Analyzer API",
        "endpoints": {
            "/probe": "POST - Analyze UDP stream with IP and port",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/probe", response_model=StreamResponse)
async def probe_udp_stream(
    request: StreamRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Probe UDP stream using ffprobe
    
    - **ip**: UDP stream IP address
    - **port**: UDP stream port number
    - **X-API-Key**: Required in header for authentication
    """
    udp_url = f"udp://{request.ip}:{request.port}"
    
    try:
        # Build ffprobe command với các option tối ưu cho UDP
        command = [
            "ffprobe",
            "-v", "quiet",  # Giảm log verbose
            "-analyzeduration", "5000000",  # 5 giây để analyze
            "-probesize", "5000000",  # 5MB probe size
            "-timeout", "10000000",  # 10 giây timeout cho network I/O (microseconds)
            "-i", udp_url,
            "-show_format",
            "-show_streams",
            "-show_programs",
            "-show_chapters",
            "-show_private_data",
            "-print_format", "json"
        ]
        
        # Execute ffprobe command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15  # 15 seconds timeout (giảm từ 30s)
        )
        
        # Check if command executed successfully
        if result.returncode != 0:
            return StreamResponse(
                success=False,
                udp_url=udp_url,
                error=f"ffprobe error: {result.stderr}"
            )
        
        # Parse JSON output
        try:
            probe_data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return StreamResponse(
                success=False,
                udp_url=udp_url,
                error=f"Failed to parse ffprobe output: {str(e)}"
            )
        
        return StreamResponse(
            success=True,
            udp_url=udp_url,
            data=probe_data
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Request timeout - ffprobe took too long to respond"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="ffprobe not found. Please install ffmpeg/ffprobe"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

