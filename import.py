import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine('postgres://ngacmtaorcbftl:74b94bc7266c5c43999b3b23dea851cb0130a08f9bd75eb70bc75e6a05946b2e@ec2-54-83-17-151.compute-1.amazonaws.com:5432/depfs798olo8t9')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    
    for isb,tit,aut,yr in reader:
        db.execute("INSERT INTO book_info (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isb, "title":tit, "author":aut, "year":yr})
    db.commit()
    
if __name__== "__main__":    
    main()