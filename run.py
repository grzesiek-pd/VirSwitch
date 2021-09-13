from virswitch_client import app
import webbrowser

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(port=5000)
