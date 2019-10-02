# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://administrador:@localhost:5432/biosql')
Session = sessionmaker(bind=engine)

Base = declarative_base()

"""
count(): Returns the total number of rows of a query.
filter(): Filters the query by applying a criteria.
delete(): Removes from the database the rows matched by a query.
distinct(): Applies a distinct statement to a query.
exists(): Adds an exists operator to a subquery.
first(): Returns the first row in a query.
get(): Returns the row referenced by the primary key parameter passed as argument.
join(): Creates a SQL join in a query.
limit(): Limits the number of rows returned by a query.
order_by(): Sets an order in the rows returned by a query.
"""
