from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, JSON, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from uuid import uuid4

class DeviceStatus(str, enum.Enum):
    ACTIVE = "active"
    CONTAINED = "contained"
    INACTIVE = "inactive"
    REVOKED = "revoked"

class CredentialType(str, enum.Enum):
    VIRTUAL_CARD = "virtual_card"
    EMPLOYEE_ID = "employee_id"
    WALLET_TOKEN = "wallet_token"
    API_KEY = "api_key"

class EventLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    COMPLETED = "completed"
    FAILED = "failed"

class TransactionRisk(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"

class FileTransferDirection(str, enum.Enum):
    DROP = "drop"
    PULL = "pull"

class FileTransferStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AuditAction(str, enum.Enum):
    DEVICE_ENROLLED = "device_enrolled"
    DEVICE_CONTAINED = "device_contained"
    DEVICE_RELEASED = "device_released"
    DEVICE_REVOKED = "device_revoked"
    CREDENTIAL_REGISTERED = "credential_registered"
    CREDENTIAL_SUSPENDED = "credential_suspended"
    CREDENTIAL_REVOKED = "credential_revoked"
    TRANSACTION_PROCESSED = "transaction_processed"
    TRANSACTION_DECLINED = "transaction_declined"
    FILE_TRANSFER_INITIATED = "file_transfer_initiated"
    FILE_TRANSFER_COMPLETED = "file_transfer_completed"
    CONTAINMENT_INITIATED = "containment_initiated"
    EVIDENCE_COLLECTED = "evidence_collected"

# ============== DEVICE MODELS ==============
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    asset_id = Column(String, unique=True, index=True)  # Permanent asset identifier
    device_name = Column(String, index=True)
    device_type = Column(String)  # laptop, phone, tablet, etc.
    serial_number = Column(String, unique=True)
    assigned_worker_id = Column(String, ForeignKey("workers.id"))
    status = Column(Enum(DeviceStatus), default=DeviceStatus.ACTIVE, index=True)
    
    # Device Characteristics
    os_type = Column(String)
    os_version = Column(String)
    mac_address = Column(String, unique=True)
    ip_address = Column(String)
    imei = Column(String, unique=True, nullable=True)
    
    # Location (privacy-minimized: coordinates only if deliberately reported)
    last_latitude = Column(Numeric(10, 8), nullable=True)
    last_longitude = Column(Numeric(11, 8), nullable=True)
    last_location_timestamp = Column(DateTime, nullable=True)
    location_consent = Column(Boolean, default=False)
    
    # Containment & Evidence
    is_contained = Column(Boolean, default=False, index=True)
    contained_at = Column(DateTime, nullable=True)
    contained_reason = Column(Text, nullable=True)
    evidence_checkpoint = Column(String, nullable=True)  # Reference to evidence snapshot
    heartbeat_active = Column(Boolean, default=True)  # Heartbeat preserved during containment
    cache_purged_at = Column(DateTime, nullable=True)
    
    # Enrollment
    enrolled_at = Column(DateTime, default=func.now())
    enrollment_acceptance = Column(JSON, nullable=True)  # Enrollment acceptance record
    integrity_baseline = Column(JSON, nullable=True)  # Device integrity baseline
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    worker = relationship("Worker", back_populates="devices")
    events = relationship("Event", back_populates="device", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="device", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="device")
    file_transfers = relationship("FileTransfer", back_populates="device")
    audit_logs = relationship("AuditLog", back_populates="device")

class Worker(Base):
    __tablename__ = "workers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    worker_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    employee_id = Column(String, unique=True)
    department = Column(String)
    role = Column(String)
    
    # Financial Access
    has_financial_access = Column(Boolean, default=True)
    financial_access_revoked_at = Column(DateTime, nullable=True)
    
    # Relationships
    devices = relationship("Device", back_populates="worker")
    credentials = relationship("Credential", back_populates="worker")
    transactions = relationship("Transaction", back_populates="worker")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# ============== CREDENTIAL MODELS ==============
class Credential(Base):
    __tablename__ = "credentials"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    worker_id = Column(String, ForeignKey("workers.id"), index=True)
    credential_type = Column(Enum(CredentialType), index=True)
    
    # Credential Details (encrypted)
    opaque_provider_reference = Column(String, unique=True)  # Provider's opaque ID
    last_four = Column(String)  # Last 4 digits for UI display
    issuer = Column(String)  # Bank, payment processor, etc.
    wallet_app = Column(String, nullable=True)
    
    # Limits
    single_transaction_limit = Column(Numeric(10, 2), nullable=True)
    daily_limit = Column(Numeric(10, 2), nullable=True)
    monthly_limit = Column(Numeric(10, 2), nullable=True)
    
    # Permissions
    allow_peer_to_peer = Column(Boolean, default=False)
    allow_atm_use = Column(Boolean, default=False)
    allowed_merchants = Column(JSON, nullable=True)  # Whitelist of merchants
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_suspended = Column(Boolean, default=False, index=True)
    suspended_at = Column(DateTime, nullable=True)
    suspension_reason = Column(Text, nullable=True)
    
    registered_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="credentials")
    worker = relationship("Worker", back_populates="credentials")
    transactions = relationship("Transaction", back_populates="credential")

# ============== EVENT & ALERT MODELS ==============
class Event(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    level = Column(Enum(EventLevel), index=True)
    category = Column(String, index=True)  # security, transaction, device_health, etc.
    
    log_source = Column(String)  # Origin of the event
    message = Column(Text)  # Privacy-minimized message (no raw PII)
    raw_data = Column(JSON, nullable=True)  # Sensitive data (encrypted/access-restricted)
    
    timestamp = Column(DateTime, default=func.now(), index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="events")
    alert = relationship("Alert", back_populates="event", uselist=False)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    event_id = Column(String, ForeignKey("events.id"), index=True)
    asset_id = Column(String, index=True)  # Permanent asset identifier only (no worker names)
    
    severity = Column(Enum(AlertSeverity), index=True)
    rule_name = Column(String)
    reason = Column(Text)
    
    triggered_at = Column(DateTime, default=func.now(), index=True)
    status = Column(String, default="triggered")  # triggered, acknowledged, resolved
    
    # Relationships
    event = relationship("Event", back_populates="alert")

# ============== TRANSACTION MODELS ==============
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    credential_id = Column(String, ForeignKey("credentials.id"), index=True)
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    worker_id = Column(String, ForeignKey("workers.id"), index=True)
    
    # Transaction Details
    amount = Column(Numeric(10, 2))
    merchant = Column(String)
    merchant_category = Column(String)
    channel = Column(String)  # card, atm, p2p, online, etc.
    reference_id = Column(String, unique=True)
    
    # Status & Risk
    status = Column(Enum(TransactionStatus), index=True)
    risk_level = Column(Enum(TransactionRisk), index=True)
    risk_score = Column(Numeric(5, 2), nullable=True)  # 0-100
    risk_factors = Column(JSON, nullable=True)  # Flags that triggered risk assessment
    
    # Limits Check
    exceeds_single_limit = Column(Boolean, default=False)
    exceeds_daily_limit = Column(Boolean, default=False)
    exceeds_monthly_limit = Column(Boolean, default=False)
    
    # Documentation
    business_purpose = Column(Text, nullable=True)
    documentation_status = Column(String, default="pending")  # pending, provided, overdue
    documentation_uploaded_at = Column(DateTime, nullable=True)
    documentation_overdue_at = Column(DateTime, nullable=True)
    
    timestamp = Column(DateTime, default=func.now(), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="transactions")
    worker = relationship("Worker", back_populates="transactions")
    credential = relationship("Credential", back_populates="transactions")

# ============== FILE TRANSFER MODELS ==============
class FileTransfer(Base):
    __tablename__ = "file_transfers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    
    direction = Column(Enum(FileTransferDirection), index=True)  # drop or pull
    source_path = Column(String)
    relative_path = Column(String)  # Under approved drop/pull folder
    file_name = Column(String)
    file_size = Column(Integer)  # bytes
    file_hash = Column(String, nullable=True)  # SHA256 for integrity
    
    status = Column(Enum(FileTransferStatus), index=True)
    error_message = Column(Text, nullable=True)
    
    initiated_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="file_transfers")

# ============== AUDIT MODELS ==============
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), nullable=True, index=True)
    credential_id = Column(String, nullable=True, index=True)
    transaction_id = Column(String, nullable=True, index=True)
    
    action = Column(Enum(AuditAction), index=True)
    actor = Column(String)  # Admin, system, automated process
    subject = Column(String)  # What was acted upon
    reason = Column(Text, nullable=True)
    details = Column(JSON)  # Full audit details
    
    timestamp = Column(DateTime, default=func.now(), index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="audit_logs")

# ============== AI ANALYSIS MODEL ==============
class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    asset_id = Column(String, index=True)  # References permanent asset ID only
    analysis_scope = Column(String)  # Device health, anomaly detection, risk assessment
    
    # Privacy-minimized analysis (no raw messages, no worker names)
    signals = Column(JSON)  # Technical signals detected
    evidence_gaps = Column(JSON)  # Missing data points
    recommendations = Column(JSON)  # Suggested actions
    
    severity_score = Column(Numeric(5, 2))
    
    # Execution details
    execution_start = Column(DateTime)
    execution_end = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Safety: No automatic containment or revocation
    requires_human_review = Column(Boolean, default=True)
    reviewed_by = Column(String, nullable=True)
    review_timestamp = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
