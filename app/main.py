import os
from server import create_app


app = create_app(os.environ.get('CONFIG_MODE'))

if __name__ == "__main__":
    print("eeee")
    app.run(ssl_context="adhoc")
