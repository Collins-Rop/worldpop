echo "=========================================="
echo "WORLDPOP Dashboard"
echo "=========================================="
echo ""
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""
echo "Running data pipeline..."
python src/pipeline.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Pipeline completed successfully!"
    echo "Launching dashboard..."
    echo "=========================================="
    echo ""
    streamlit run app.py
else
    echo ""
    echo "=========================================="
    echo "Pipeline failed. Please check the errors above."
    echo "=========================================="
fi