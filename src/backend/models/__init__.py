from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb")

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
mst_user = Base.classes.mst_user

# session = Session(engine)
