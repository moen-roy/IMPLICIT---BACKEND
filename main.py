
from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True,port=5501)