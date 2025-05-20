from app import app

# This exposes the WSGI server variable that Gunicorn needs
server = app.server

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)