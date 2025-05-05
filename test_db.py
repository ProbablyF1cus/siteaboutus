from data.users import User
from data.recipes import Recipe
from data import db_session

db_session.global_init('db/db.db')


db_sess = db_session.create_session()
for user in db_sess.query(User).all():
    print(user.name, user.image)
    # db_sess.delete(user)
    # db_sess.commit()