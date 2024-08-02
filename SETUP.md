# Clone the repository
git clone https://github.com/yourusername/supply_chain_optimization.git
cd supply_chain_optimization

# Set up virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Downgrade pip
pip install pip==23.1.2

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -c "from app import db; db.create_all()"

# Populate the database (optional)
python populate_db.py

# Start the Flask application
python app.py

# Start the Celery worker (in a separate terminal)
venv\Scripts\activate  # if not already activated
celery -A tasks worker --loglevel=info

# Access the web application
# Open a web browser and navigate to http://localhost:5000
