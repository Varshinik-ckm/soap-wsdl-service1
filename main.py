from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request, Response, render_template_string
import os

# SOAP service class
class HelloService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Spyne SOAP application
soap_app = Application(
    [HelloService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
wsgi_app = WsgiApplication(soap_app)

# Flask app
app = Flask(__name__)

# HTML form template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Hello Baby</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        input[type="text"] { padding: 8px; font-size: 16px; }
        input[type="submit"] { padding: 8px 16px; font-size: 16px; }
        h1 { color: #007BFF; }
    </style>
</head>
<body>
    <h1>Say Hello 👋</h1>
    <form method="post" action="/hello">
        <input type="text" name="name" placeholder="Enter your name" required />
        <input type="submit" value="Say Hello" />
    </form>
    {% if result %}
        <h2>{{ result }}</h2>
    {% endif %}
</body>
</html>
"""

# Web form route
@app.route("/hello", methods=["GET", "POST"])
def hello_page():
    if request.method == "POST":
        name = request.form.get("name", "Baby")
        result = f"Hello, {name}!"
        return render_template_string(HTML_FORM, result=result)
    return render_template_string(HTML_FORM, result=None)

# SOAP endpoint
@app.route("/", methods=["GET", "POST"])
def soap_interface():
    if request.method == "POST":
        response = []

        def start_response(status, headers):
            response.append(("status", status))
            response.append(("headers", headers))

        result = wsgi_app(request.environ, start_response)
        status = dict(response).get("status", "500 INTERNAL SERVER ERROR")
        headers = dict(response).get("headers", [])

        return Response(result, status=status, headers=dict(headers))
    return "<h2>SOAP Service is running. POST a SOAP request to this URL.</h2>"

# Run locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)