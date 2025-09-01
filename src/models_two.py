import sqlalchemy.orm as orm
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Date, Boolean
from typing import List

class Base(orm.DeclarativeBase): pass

class Player(Base): 
    __tablename__ = "player"
    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)

    levels: orm.Mapped[List["Level"]] = orm.relationship(
        secondary="player_level", back_populates="players"
    )
    
    level_associations: orm.Mapped[List["PlayerLevel"]] = orm.relationship(
        back_populates="player"
    )

class Level(Base):  
    __tablename__ = "level"
    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    title:orm.Mapped[str] = orm.mapped_column(String(100), index=True, unique=True)
    order: orm.Mapped[int] = Column(Integer, default=0)

    players: orm.Mapped[List["Player"]] = orm.relationship(
        secondary="player_level", back_populates="levels"
    )

    player_associations: orm.Mapped[List["PlayerLevel"]] = orm.relationship(
        back_populates="level"
    )

    prizes: orm.Mapped[List["Prize"]] = orm.relationship(
        secondary="level_prize", back_populates="levels"
    )

    prize_associations: orm.Mapped[List["LevelPrize"]] = orm.relationship(
        back_populates="level"
    )



class Prize(Base): 
    __tablename__ = "prize"
    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    title:orm.Mapped[str] = orm.mapped_column(String(100), index=True, unique=True)

    levels: orm.Mapped[List["Level"]] = orm.relationship(
        secondary="level_prize", back_populates="prizes"
    )
    
    level_associations: orm.Mapped[List["LevelPrize"]] = orm.relationship(
        back_populates="prize"
    )


class LevelPrize(Base): 
    __tablename__ = "level_prize"
    level_id = orm.mapped_column(ForeignKey("level.id"), primary_key=True)
    prize_id = orm.mapped_column(ForeignKey("prize.id"), primary_key=True)    
    
    prize: orm.Mapped["Prize"] = orm.relationship(back_populates="level_associations")    
    level: orm.Mapped["Level"] = orm.relationship(back_populates="prize_associations")

    received = Column(Date)

class PlayerLevel(Base): 
    __tablename__ = "player_level"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    player_id = orm.mapped_column(ForeignKey("player.id"), primary_key=True)
    level_id = orm.mapped_column(ForeignKey("level.id"), primary_key=True)    
    
    player: orm.Mapped["Player"] = orm.relationship(back_populates="level_associations")    
    level: orm.Mapped["Level"] = orm.relationship(back_populates="player_associations")
    
    completed = Column(Date)
    is_completed = Column(Boolean, default=True, nullable=False) 
    score: orm.Mapped[int] = Column(Integer, default=0)

