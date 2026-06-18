from app_factory import create_app

app = create_app()


@app.get("/")
def home():
    return {
        "message": "Trekking Management Application API"
    }


if __name__ == "__main__":
    app.run(debug=True)

