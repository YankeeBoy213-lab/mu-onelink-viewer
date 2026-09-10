from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import DeviceStatus, CredentialType, EventLevel, AlertSeverity

# ============== DEVICE SCHEMAS ==============
class DeviceCreate(BaseModel):
    asset_id: str
    device_name: str
    device_type: str
    serial_number: str
    assigned_worker_id: str
    os_type: str
    os_version: str
    mac_address: str
    ip_address: str
    imei: Optional[str] = None
    enrollment_acceptance: Optional[dict] = None
    integrity_baseline: Optional[dict] = None

class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    ip_address: Optional[str] = None
    last_latitude: Optional[float] = None
    last_longitude: Optional[float] = None
    metadata: Optional[dict] = None

class DeviceResponse(BaseModel):
    id: str
    asset_id: str
    device_name: str
    device_type: str
    status: DeviceStatus
    is_contained: bool
    assigned_worker_id: str
    enrolled_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class DeviceDetailResponse(DeviceResponse):
    serial_number: str
    mac_address: str
    ip_address: str
    os_type: str
    os_version: str
    last_latitude: Optional[float]
    last_longitude: Optional[float]
    last_location_timestamp: Optional[datetime]
    contained_at: Optional[datetime]
    contained_reason: Optional[str]
    heartbeat_active: bool
    metadata: Optional[dict]

# ============== WORKER SCHEMAS ==============
class WorkerCreate(BaseModel):
    worker_name: str
    email: str
    employee_id: str
    department: str
    role: str

class WorkerResponse(BaseModel):
    id: str
    worker_name: str
    email: str
    employee_id: str
    department: str
    role: str
    has_financial_access: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============== CREDENTIAL SCHEMAS ==============
class CredentialCreate(BaseModel):
    device_id: str
    worker_id: str
    credential_type: CredentialType
    opaque_provider_reference: str
    last_four: str
    issuer: str
    wallet_app: Optional[str] = None
    single_transaction_limit: Optional[float] = None
    daily_limit: Optional[float] = None
    monthly_limit: Optional[float] = None
    allow_peer_to_peer: bool = False
    allow_atm_use: bool = False

class CredentialResponse(BaseModel):
    id: str
    device_id: str
    worker_id: str
    credential_type: CredentialType
    last_four: str
    issuer: str
    is_active: bool
    is_suspended: bool
    registered_at: datetime
    
    class Config:
        from_attributes = True

# ============== EVENT & ALERT SCHEMAS ==============
class EventCreate(BaseModel):
    device_id: str
    level: EventLevel
    category: str
    log_source: str
    message: str
    raw_data: Optional[dict] = None

class EventResponse(BaseModel):
    id: str
    device_id: str
    level: EventLevel
    category: str
    message: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: str
    asset_id: str
    severity: AlertSeverity
    rule_name: str
    reason: str
    triggered_at: datetime
    status: str
    
    class Config:
        from_attributes = True

# ============== TRANSACTION SCHEMAS ==============
class TransactionCreate(BaseModel):
    credential_id: str
    device_id: str
    worker_id: str
    amount: float
    merchant: str
    merchant_category: str
    channel: str
    reference_id: str
    business_purpose: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    credential_id: str
    amount: float
    merchant: str
    channel: str
    status: str
    risk_level: str
    risk_score: Optional[float]
    documentation_status: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ============== FILE TRANSFER SCHEMAS ==============
class FileTransferCreate(BaseModel):
    device_id: str
    direction: str  # drop or pull
    file_name: str
    relative_path: str
    file_size: int

class FileTransferResponse(BaseModel):
    id: str
    device_id: str
    direction: str
    file_name: str
    file_size: int
    status: str
    initiated_at: datetime
    
    class Config:
        from_attributes = True

# ============== CONTAINMENT SCHEMAS ==============
class ContainmentRequest(BaseModel):
    reason: str
    evidence_checkpoint: Optional[str] = None

class ContainmentResponse(BaseModel):
    device_id: str
    is_contained: bool
    contained_at: datetime
    heartbeat_active: bool
    cache_purged: bool
    message: str
