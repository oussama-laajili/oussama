# setup.py
from setuptools import setup, find_packages
from setuptools.extension import Extension # Good, keep this
import os

# --- Define the C extension module optionally ---
# Set BUILD_CEXT=1 to enable building the native extension. Default: disabled for portability.
ext_modules = []
if os.environ.get("BUILD_CEXT") == "1":
    ext_modules = [
        Extension(
            name="main_c_module",
            sources=["main.c"],
        )
    ]

setup(
    name="Traffic", # Your project name
    version="0.1.0", # Your project version

    # --- Specify Python packages to include ---
    # This addresses the "Multiple top-level packages discovered" error.
    # find_packages() will automatically discover directories that contain __init__.py
    # like 'core', 'models', 'source'.
    # You can exclude directories that are not Python packages (like 'tests', 'docs', 'data' if 'data' isn't a package).
    packages=find_packages(exclude=['tests', 'docs']),

    # --- Include data files ---
    # If your 'data' directory contains non-Python files you want in your distribution:
    include_package_data=True,
    package_data={
        '': ['README.md', 'pyproject.toml', 'requirements.txt'], # Include these top-level files
        'data': ['*'], # Include all files in the 'data' directory
        # If your Python packages (e.g., 'core') have data files:
        # 'core': ['*.json', '*.csv'],
    },

    # --- Define extension modules ---
    # Pass the list containing your C extension directly.
    # We are NOT using cythonize here because main.c is already a C file.
    ext_modules=ext_modules,

    # --- Other metadata (good practice) ---
    author="Ahmed",
    author_email="achebbi2002@gmail.com",
    description="A traffic simulation project using C and Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url="http://your-project-url.com", # Uncomment and set your project URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8', # Adjust if your project needs a different Python version
    install_requires=[
        # List any Python package dependencies here, e.g., 'numpy', 'scipy'
    ],
)