echo "Installing package dependencies inside docker:"
echo ""
poetry run pip install .
echo $@
poetry run python "$@"

