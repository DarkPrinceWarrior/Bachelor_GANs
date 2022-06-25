from app import app

if __name__ == '__main__':

    # models.db_setup.init_db()
    app.run(host="0.0.0.0", debug=True)
