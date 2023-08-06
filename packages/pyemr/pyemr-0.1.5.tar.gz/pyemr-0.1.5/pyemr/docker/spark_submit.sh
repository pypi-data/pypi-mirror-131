echo "Test spark script"
echo ""
poetry run pip install pyspark spark-submit
poetry run spark-submit $@


