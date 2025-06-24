Decoupled action execution architecture with multiple interfaces.

<ins>Architecture</ins>

Dynamic module loading system with pluggable actions. Four execution patterns:

- **Synchronous** - Direct CLI execution
- **Request/Response** - HTTP API 
- **Asynchronous** - File-based queue with worker process
- **Scheduled** - Time-based recurring execution

<ins>Potential</ins>

- Microservice decomposition via action modules
- Background job processing with file queue persistence  
- Multi-interface APIs (CLI + HTTP + queue) from single codebase
- Horizontal scaling: multiple subscribers, load balancing
- Fault tolerance: queue survives crashes, retry logic
- Service mesh integration via HTTP endpoints
- Event-driven workflows by chaining enqueue actions
- Cron-like scheduling without external dependencies

<ins>Usage</ins>

```bash
python cli.py reverse_string hello          # Direct
python server.py 8000                       # HTTP API  
python subscriber.py queue.txt              # Queue worker
python schedule.py reverse_string hello     # Scheduled (10s)
python cli.py enqueue_action reverse_string hello  # Async
```
