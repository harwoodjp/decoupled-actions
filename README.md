Decoupled action execution architecture with multiple interfaces.

## Architecture

Dynamic module loading system with pluggable actions. Three execution patterns:

- **Synchronous** - Direct CLI execution
- **Request/Response** - HTTP API 
- **Asynchronous** - File-based queue with worker process

## Potential

- Microservice decomposition via action modules
- Background job processing with file queue persistence  
- Multi-interface APIs (CLI + HTTP + queue) from single codebase
- Horizontal scaling: multiple subscribers, load balancing
- Fault tolerance: queue survives crashes, retry logic
- Service mesh integration via HTTP endpoints
- Event-driven workflows by chaining enqueue actions

## Usage

```bash
python cli.py reverse_string hello # CLI
python server.py 8000 # HTTP API  
python subscriber.py queue.txt # Queue worker
python cli.py enqueue_action reverse_string hello  # Async
```