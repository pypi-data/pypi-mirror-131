echo "Installing package dependencies inside docker:"
echo ""
pip install .
echo $@
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port 8889

