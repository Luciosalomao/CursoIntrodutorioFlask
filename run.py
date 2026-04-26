from app import create_app, db
from flask_migrate import Migrate
import sys

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        print("Modo desenvolvimento - http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        from waitress import serve
        print("Modo producao - http://localhost:8000")
        serve(app, host='0.0.0.0', port=8000)