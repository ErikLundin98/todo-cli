install_cli:
	python -m pip install build
	python -m build
	pip install dist/todo-0.0.1-py3-none-any.whl --force-reinstall