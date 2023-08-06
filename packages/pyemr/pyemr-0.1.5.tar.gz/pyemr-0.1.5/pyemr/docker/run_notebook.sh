echo "Installing package dependencies inside docker:"
echo ""
poetry install
poetry run pip install jupyter
poetry run jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port 8889
