from app import create_app

#calling the create_app function to create an instance of the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)