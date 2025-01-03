from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class RequestLogTable(Base):
   """Definición de la estructura de la tabla de logs"""
   __tablename__ = 'logs'
   
   id = Column(Integer, primary_key=True)
   timestamp = Column(DateTime, default=datetime.now)
   url = Column(String(255))
   endpoint = Column(String(100))
   method = Column(String(10))
   browser = Column(String(50))
   browser_version = Column(String(20))
   os = Column(String(50))
   os_version = Column(String(20))
   device_brand = Column(String(50))
   ip_address = Column(String(50))
   query = Column(Text)

   def to_dict(self):
       """Convierte el objeto a diccionario para serialización"""
       return {
           'id': self.id,
           'timestamp': self.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
           'url': self.url,
           'endpoint': self.endpoint,
           'method': self.method,
           'browser': self.browser,
           'browser_version': self.browser_version,
           'os': self.os,
           'os_version': self.os_version,
           'device_brand': self.device_brand,
           'ip_address': self.ip_address,
           'query': self.query
       }

class RequestLogModel:
   """Maneja la conexión y operaciones con la base de datos"""
   def __init__(self):
       self.engine = None
       self.Table = RequestLogTable

   def initialize_db(self):
       """Inicializa la conexión a la base de datos y crea las tablas"""
       os.makedirs('database', exist_ok=True)
       self.engine = create_engine('sqlite:///database/database.db')
       Base.metadata.create_all(bind=self.engine)
       return self.engine

   def save(self, log_data):
       """
       Guarda un nuevo registro de log
       Args:
           log_data: Instancia de RequestLogTable con los datos a guardar
       """
       from sqlalchemy.orm import Session
       with Session(self.engine) as session:
           session.add(log_data)
           session.commit()

   def get_all(self, limit=None):
       """
       Obtiene todos los registros de log
       Args:
           limit: Número máximo de registros a retornar (opcional)
       """
       from sqlalchemy.orm import Session
       with Session(self.engine) as session:
           if limit:
               logs = session.query(RequestLogTable).order_by(
                   RequestLogTable.timestamp.desc()
               ).limit(limit).all()
           else:
               logs = session.query(RequestLogTable).order_by(
                   RequestLogTable.timestamp.desc()
               ).all()
           return logs