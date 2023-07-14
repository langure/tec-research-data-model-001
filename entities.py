from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from dataclasses import dataclass

Base = declarative_base()

class YouTubeChannel(Base):
    __tablename__ = 'youtube_channels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    you_tube_id = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    subscribers = Column(Integer)
    views = Column(Integer)
    videos = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __init__ (self, you_tube_id, title, description, subscribers, views, videos):
        self.you_tube_id = you_tube_id
        self.title = title
        self.description = description
        self.subscribers = subscribers
        self.views = views
        self.videos = videos

    def __str__(self):
        table_data = [
            ["YT_ID", "Title", "Description", "Subscribers", "Views", "Videos"],
            [self.you_tube_id, self.title, self.description, self.subscribers, self.views, self.videos]
        ]
        return tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")

class YouTubeComment(Base):
    __tablename__ = 'youtube_comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    youtube_id = Column(String(255))
    author = Column(String(255))
    text = Column(Text)
    likes = Column(Integer)
    date = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    def __init__(self, youtube_id, author, text, likes, date):        
        self.youtube_id = youtube_id
        self.author = author
        self.text = text
        self.likes = likes
        self.date = date
        

    def __str__(self):
        table_data = [
            ["YT_ID", "Author", "Text", "Likes", "Date"],
            [self.youtube_id, self.author, self.text, self.likes, self.date]
        ]
        return tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    
    
    
@dataclass
class DatabaseDriver:
    username: str
    password: str
    host: str
    port: int
    database: str
    engine: object = None


    def __post_init__(self):
        if self.engine is None:
            connection_string = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string)
            
    
    def initialize_database(self):
        # destroy all tables
        Base.metadata.drop_all(self.engine)
        # Create all tables
        Base.metadata.create_all(self.engine)
        
    def save_youtube_comment(self, youtube_comment):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.add(youtube_comment)
        session.commit()
        session.close()