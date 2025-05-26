from flask import Flask
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

app = Flask(__name__)

class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

soap_app = Application([HelloWorldService], 'spyne.examples.hello.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# Wrap the Spyne application with WsgiApplication
wsgi_app = WsgiApplication(soap_app)

# Flask route for root - simple message
@app.route('/')
def home():
    return "Hello from Flask SOAP API!"

# Route for SOAP service
@app.route('/soap', methods=['POST', 'GET'])
def soap_service():
    # Dispatch request to Spyne WSGI app
    return wsgi_app.app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
