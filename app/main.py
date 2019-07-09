from server import create_app
import sys

app = create_app('config.Prod')

if __name__ == "__main__":
    app.run()