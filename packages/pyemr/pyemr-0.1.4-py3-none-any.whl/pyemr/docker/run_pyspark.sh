echo "Installing package dependencies inside docker:"
echo ""
poetry install 
poetry run pip install pyspark
poetry run pyspark

