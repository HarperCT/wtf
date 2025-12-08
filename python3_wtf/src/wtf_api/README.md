# WTF API

FastAPI backend for WheresTheFault - provides REST API for plugin discovery and execution.

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Development Server

```bash
python server.py
```

Or:

```bash
uvicorn wtf_api.main:app --reload
```

Server will start at: http://localhost:8000

### API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health

- `GET /api/v1/health` - Health check
- `GET /api/v1/ping` - Simple ping

### Plugins

- `GET /api/v1/plugins` - List all available plugins
- `GET /api/v1/plugins/{name}` - Get plugin info
- `GET /api/v1/plugins/{name}/applicable` - Check if plugin is applicable

### Execution

- `POST /api/v1/execute` - Execute plugins synchronously
- `POST /api/v1/execute/async` - Execute plugins asynchronously (TODO)
- `GET /api/v1/execution/{id}` - Get execution status (TODO)
- `GET /api/v1/executions` - List executions (TODO)
- `DELETE /api/v1/execution/{id}` - Cancel execution (TODO)

## Example Usage

### List Plugins

```bash
curl http://localhost:8000/api/v1/plugins
```

### Execute Plugins

```bash
curl -X POST http://localhost:8000/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "timeout": 5,
    "max_concurrent": 16,
    "plugin_args": [
      {"ps": []},
      {"df": []},
      {"free": []}
    ],
    "output_dir": "/tmp"
  }'
```

## Configuration

Environment variables (prefix with `WTF_`):

- `WTF_API_HOST` - Host to bind (default: 0.0.0.0)
- `WTF_API_PORT` - Port to bind (default: 8000)
- `WTF_DEFAULT_TIMEOUT` - Default timeout (default: 5)
- `WTF_DEFAULT_OUTPUT_DIR` - Default output directory (default: /tmp)

## Project Structure

```
wtf_api/
├── __init__.py
├── main.py              # FastAPI app
├── config.py            # Configuration
├── server.py            # Server runner
├── models.py            # Pydantic models
├── routers/             # API endpoints
│   ├── health.py
│   ├── plugins.py
│   └── execution.py
└── services/            # Business logic
    ├── plugin_service.py
    └── execution_service.py
```

## TODO

- [ ] Implement async execution with task tracking
- [ ] Add WebSocket support for real-time progress
- [ ] Add authentication/authorization
- [ ] Add rate limiting
- [ ] Implement execution history persistence
- [ ] Add result caching
- [ ] Add plugin output streaming
- [ ] Add execution cancellation
