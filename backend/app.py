from app_factory import create_app

app = create_app()


@app.get("/")
def home():
    return {
        "message": "Trekking Management Application API"
    }

@app.get("/send-test-email")
def send_email():

    from tasks import send_test_email

    send_test_email.delay()

    return {
        "msg": "Email queued successfully"
    }

if __name__ == "__main__":
    app.run(debug=True)

