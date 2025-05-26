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
app.wsgi_app = WsgiApplication(soap_app)

@app.route('/')
def home():
    return "Hello from Flask SOAP API!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
