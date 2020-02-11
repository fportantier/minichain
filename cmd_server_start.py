import click
import flask
from web import make_app

@click.command()
@click.option('-p', 'port', default=5000, help='Port to use')
def cmd_server_start(port):

    app = make_app(port)
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    cmd_server_start()


