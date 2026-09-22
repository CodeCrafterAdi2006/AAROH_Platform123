"""
AAROH Database Schema (SQLAlchemy 2.0 ORM)
Stores longitudinal patient screening assessments.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(64), nullable=False, index=True)
    assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    classical_score = Column(Float, nullable=False)
    quantum_score = Column(Float, nullable=False)
    hybrid_score = Column(Float, nullable=False)
    risk_tier = Column(String(32), nullable=False)  # ELEVATED, MODERATE, BASELINE
    consensus_status = Column(String(32), nullable=False)  # CONCORDANT, DISCORDANT_REVIEW
    feature_json = Column(Text, nullable=True)
    shap_json = Column(Text, nullable=True)
    clinical_memo_json = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "assessed_at": self.assessed_at.isoformat() if self.assessed_at else None,
            "classical_score": round(self.classical_score, 4),
            "quantum_score": round(self.quantum_score, 4),
            "hybrid_score": round(self.hybrid_score, 4),
            "risk_tier": self.risk_tier,
            "consensus_status": self.consensus_status,
            "feature_json": self.feature_json,
            "shap_json": self.shap_json,
            "clinical_memo_json": self.clinical_memo_json,
        }
