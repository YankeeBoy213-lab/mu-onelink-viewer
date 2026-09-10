# MU OneLink Viewer

A comprehensive asset device management, custody reference, and financial access control system with real-time audit trails and privacy-minimized AI analysis.

## Features

✅ **Permanent Asset Device Management** - Track and manage enrolled company devices  
✅ **Custody & Containment** - Suspend devices while preserving evidence and maintaining service continuity  
✅ **Virtual Financial Credentials** - Issue unique credentials per worker with real-time transaction monitoring  
✅ **Real-time Event Timeline** - Nightingale alert system with privacy-minimized logging  
✅ **AI Incident Analysis** - Local privacy-preserving incident analysis using asset IDs  
✅ **File Transfer Queuing** - Secure drop/pull file management with approval workflow  
✅ **Comprehensive Audit Trail** - All enrollment, containment, credential, and transaction events logged  
✅ **Financial Control Rules** - Per-worker and per-device transaction limits with documentation tracking  

## Tech Stack

- **Backend**: Python (FastAPI), PostgreSQL
- **Frontend**: Next.js 14+, TypeScript, Tailwind CSS
- **Real-time**: WebSocket for event streaming
- **Security**: JWT authentication, encryption at rest/transit
- **Deployment**: Docker, Kubernetes ready

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Project Structure

```
mu-onelink-viewer/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── security/     # Auth & encryption
│   ├── migrations/       # Alembic migrations
│   └── tests/
├── frontend/             # Next.js frontend
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API client
│   └── types/            # TypeScript types
├── docker-compose.yml
└── docs/                 # API & system documentation
```

## API Endpoints

### Devices
- `GET /api/devices` - List all devices
- `POST /api/devices` - Register new device
- `GET /api/devices/{id}` - Get device details
- `PUT /api/devices/{id}` - Update device
- `POST /api/devices/{id}/contain` - Contain device (suspend + evidence)
- `POST /api/devices/{id}/release` - Release contained device

### Events & Alerts
- `GET /api/events` - Event timeline (paginated, filtered)
- `GET /api/alerts` - Alert timeline
- `WS /ws/events` - WebSocket for real-time events

### Financial Credentials
- `GET /api/credentials` - List all credentials
- `POST /api/credentials` - Register new credential
- `GET /api/credentials/{id}` - Get credential details
- `PUT /api/credentials/{id}` - Update credential
- `POST /api/credentials/{id}/suspend` - Suspend credential

### Transactions
- `GET /api/transactions` - Transaction history (with risk scoring)
- `POST /api/transactions` - Record transaction
- `GET /api/transactions/{id}/documentation` - Get transaction docs

### File Management
- `POST /api/files/drop` - Queue file drop to device
- `POST /api/files/pull` - Queue file pull from device
- `GET /api/transfer-queue` - View pending transfers

### Audit
- `GET /api/audit` - Complete audit trail
- `GET /api/audit/{resource_type}/{resource_id}` - Resource-specific audit

## Security

- All credentials encrypted at rest
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- API rate limiting
- Request signing for financial operations
- Comprehensive audit logging of all sensitive operations
- Privacy-minimized event logging (no raw PII in observability)

## Documentation

- [API Documentation](./docs/API.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Security Model](./docs/SECURITY.md)
- [Database Schema](./docs/DATABASE.md)

## Development

```bash
# Run tests
cd backend && pytest
cd ../frontend && npm test

# Format code
cd backend && black . && isort .
cd ../frontend && npm run lint

# Build for production
cd backend && pip install -r requirements-prod.txt
cd ../frontend && npm run build
```

## Version

v0.4.2-alpha

## License

Proprietary - MU OneLink
