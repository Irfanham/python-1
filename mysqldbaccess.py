# This script connects to a MySQL DB
# Copyright (C) 2014 Ana Cruz-Martín (anacruzmartin@gmail.com)

import sys
import os
from gvsig import *
from gvsig import geom
from gvsig.geom import *
from java.util import Properties

sys.path.append(“/pathtomygvSIGfolder/mysql-connector-java-5.1.40-bin.jar”);
import org.gjt.mm.mysql.Driver as Driver

def main():

# Connect to the database
props = Properties()
props.put(“user”,”myuser”)
props.put(“password”,”mypasswd”)
db = Driver().connect(“jdbc:mysql://localhost/mydb”, props)
# Get geometry info from database and insert it into the new layer
c = db.createStatement()
rs = c.executeQuery(“select * from mytable where somecolumn=’somevalue'”)
while rs.next():
id = rs.getString(“somecolumn”)
rs.close()
c.close()
db.close()
