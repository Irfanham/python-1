# This script connects to a PostGIS DB
# Then creates a new gvsig layer with geospatial information retrieved from the DB

import sys
import os
from gvsig import *
from geom import *
from java.util import Properties

sys.path.append("/APLICACIONES/GIS/gvSIG-desktop-2.2.0/postgresql-9.1-903.jdbc4.jar");
import org.postgresql.Driver as Driver

def getGeometryType(type, subtype):
  geometryManager = GeometryLocator.getGeometryManager()
  return geometryManager.getGeometryType(type,subtype)

def main():
  # Create the new layer
  newProjection = currentView().getProjectionCode()
  newLayerSchema = createSchema()
  newLayerSchema.append("ID","INTEGER")
  newLayerSchema.append("GEOMETRY","GEOMETRY")
  geometryType = getGeometryType(POINT,D2)
  newLayerSchema.get("GEOMETRY").setGeometryType(geometryType)
  newLayerName = "/APLICACIONES/GIS/gvSIG-desktop-2.2.0/mynewlayer.shp"
  newLayer = createShape(newLayerSchema,newLayerName,CRS=newProjection,geometryType=POINT)
  # Connect to the database
  props = Properties()
  props.put("user","YOUR_USER")
  props.put("password","YOUR_PASSWD")
  db = Driver().connect("jdbc:postgresql://localhost/YOUR_DB", props)
  # Get geometry info from database and insert it into the new layer
  c = db.createStatement()
  rs = c.executeQuery("select table.id, ST_X(table.coordinatesxy),ST_Y(table.coordenatesxy) from YOUR_TABLES where YOUR_WHERE_CLAUSE")
  data = {}
  while rs.next():
    id = rs.getInt(1)
    newX = rs.getObject(2)
    newY = rs.getObject(3)
    print(id,newX,newY)
    newGeom = createPoint(newX,newY)
    dbValues = {"ID":id,"GEOMETRY":newGeom}
    newLayer.append(dbValues)
  rs.close()
  c.close()
  db.close()
  
  currentView().addLayer(newLayer)
  newLayer.commit()
