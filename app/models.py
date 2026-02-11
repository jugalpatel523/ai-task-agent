from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class AgentRun(Base):
    __tablename__ = "agent_runs"

    run_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), index=True)
    goal = Column(Text, nullable=False)
    status = Column(String(32), default="created")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("AgentMessage", back_populates="run", cascade="all, delete-orphan")

class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(64), ForeignKey("agent_runs.run_id"), index=True)
    role = Column(String(32), nullable=False)  # user / assistant / tool
    name = Column(String(64), nullable=True)   # tool name if role=tool
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    run = relationship("AgentRun", back_populates="messages")
