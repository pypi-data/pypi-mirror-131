echo "Installing package dependencies inside docker:"
echo ""
poetry run pip install .
poetry run python "$@"

