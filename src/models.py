import sqlalchemy.orm as orm
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from typing import List, Optional
from src.player_exception import PlayerException

class Base(orm.DeclarativeBase): pass

class PlayerBoost(Base):
    __tablename__ = "player_boost"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    player_id = orm.mapped_column(ForeignKey("players.id"), primary_key=True)
    boost_id = orm.mapped_column(
        ForeignKey("boosts.id"), primary_key=True
    )    
    
    player: orm.Mapped["Player"] = orm.relationship(back_populates="boost_associations")    
    boost: orm.Mapped["Boost"] = orm.relationship(back_populates="player_associations")

class Boost(Base):
    __tablename__ = "boosts"

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(String(50), index=True, unique=True)
    description: orm.Mapped[str] = orm.mapped_column(String(200))
    count_bonus: orm.Mapped[int] = Column(Integer, default=0)        
    type_boost: orm.Mapped["TypeBoost"] = orm.relationship(backref="type")    

    players: orm.Mapped[List["Player"]] = orm.relationship(
        secondary="player_boost", back_populates="boosts"
    )

    player_associations: orm.Mapped[List["PlayerBoost"]] = orm.relationship(
        back_populates="boost"
    )
   
    def create(self, db):
        db.add(self)
        db.commit()
        return self.id

class Player(Base):
    __tablename__ = "players"
 
    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(String(50), index=True, unique=True)
    score: orm.Mapped[int] = Column(Integer, default=0)
    login_count: orm.Mapped[int] = Column(Integer, default=0)    

    boosts: orm.Mapped[List["Boost"]] = orm.relationship(
        secondary="player_boost", back_populates="players"
    )
    
    boost_associations: orm.Mapped[List["PlayerBoost"]] = orm.relationship(
        back_populates="player"
    )
        
    def create(self, db):
        db.add(self)
        db.commit()
        return self.id

    def login(self, db, name):                
        player = db.query(Player).filter(Player.name==name).first()
        if player is None:
            raise PlayerException('Not found player!', 404)
        else:
            player.login_count += 1
            db.commit()

    def toJson(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,            
            "score": self.score,
            "login_count": self.login_count,
        }

class TypeBoost(Base):
    __tablename__ = "type_boost"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(String(50), index=True, unique=True)    
    boost_id: orm.Mapped[Optional[int]] = orm.mapped_column(ForeignKey("boosts.id"))
    boost: orm.Mapped[Optional["Boost"]] = orm.relationship(back_populates="type_boost")


