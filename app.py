from buying_frenzy import create_app
from buying_frenzy.cli import bp as cli_bp
from buying_frenzy.endpoints.v1.hello import bp as hello_bp
from buying_frenzy.endpoints.v1.restaurant import bp as restaurant_bp

app = create_app()
app.register_blueprint(cli_bp)
app.register_blueprint(hello_bp)
app.register_blueprint(restaurant_bp)

if __name__ == '__main__':
    app.run()
