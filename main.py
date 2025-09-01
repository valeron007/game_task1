from src.models import Player, Boost, PlayerBoost, TypeBoost
from src.player_exception import PlayerException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Body, HTTPException, Response, status
from fastapi.responses import JSONResponse

SQLALCHEMY_DATABASE_URL = "postgresql://valeron:rfk,fcf@172.21.1.3/game"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

app = FastAPI()

@app.post('/player')
def create_task(data=Body()):    
    player = Player(name=data['name'])
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=player.create(db),
    )

@app.post('/player/login')
def login_player(data=Body()):
    try:    
        player = Player()
        player.login(db, data['name'])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="logging succesfull",
        )              
    except PlayerException as error:
        return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=repr(error),
    )

@app.post('/boost')
def create_boost(data=Body()):    
    player = db.query(Player).filter(Player.id==data['player']).first()    
    boost = Boost(name=data['name'], 
                description=data['description'],
                count_bonus=data['count_bonus']                
            )
    
    player.score += data['count_bonus']
    player_boost = PlayerBoost(player=player, boost=boost)
    db.add(boost)    
    db.add(player_boost)
    db.commit()

        

