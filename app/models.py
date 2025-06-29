from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    country = Column(String(100),  nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    country = Column(String(50))
    league = Column(String(100))
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    position = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    team = relationship("Team", backref="players")


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    match_date = Column(Date)
    home_score = Column(Integer)
    away_score = Column(Integer)
    status = Column(String(20), default="scheduled")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    home_team = relationship("Team", foreign_keys=[home_team_id], backref="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], backref="away_matches")


class PlayerStats(Base):
    __tablename__ = "player_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    whoscored_rating = Column(Numeric(2, 2), default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    player = relationship("Player", backref="stats")
    match = relationship("Match", backref="player_stats") 