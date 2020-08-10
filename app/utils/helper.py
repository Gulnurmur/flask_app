from app.models.model import User
from werkzeug.security import check_password_hash,generate_password_hash




def check_existence(email):
    
    return False if User.query.filter_by(email=email).first() else True


def check_user(user_id):

    # return True if User.query.filter_by(id=user_id).first() else False 

    user= User.query.filter_by(id=user_id).first()

    if user:
        return True

    
    print(user)

    return False



def password_hash(password):

    hashed_password = generate_password_hash(password,"sha256")

    return hashed_password



def check_password(hashed_password, password):

    check = check_password_hash(pwhash=hashed_password, password = password)

    if check:

        return True
    
    return False