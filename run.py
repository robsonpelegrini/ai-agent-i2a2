import os
import subprocess
import sys

# Pegar porta do Railway
port = os.environ.get('PORT', '8501')

# Executar Streamlit com a porta correta
cmd = [
    sys.executable, '-m', 'streamlit', 'run', 'app.py',
    '--server.port', port,
    '--server.address', '0.0.0.0',
    '--server.headless', 'true'
]

subprocess.run(cmd)