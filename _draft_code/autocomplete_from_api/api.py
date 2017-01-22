# curl 127.0.0.1:5000/api?arg=hey

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "hello world!"


@app.route('/api')
def api():
    arg = request.args.get('arg')
    # form the API so select2 can understand it
    response = [{'id': arg + str(a) + '_id',
                 'text': arg + str(a) + '_text',
                 }
                for a in range(10)]
    response = dict(results=response)
    response = jsonify(response)
    # Stop the errors
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
