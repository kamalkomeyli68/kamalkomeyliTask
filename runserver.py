
import os
from komeyliTask import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8083))
    app.run('127.0.0.1', port=port)
