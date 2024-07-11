from setuptools import setup, find_packages

setup(
    name='document_processor',
    version='0.1.0',
    author='Fon Godwill Ivan Tana',
    author_email='ivan8tana@gmail.com',
    description='A document processing library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Fonality-code/Document-Processor',  # Replace with your GitHub repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyPDF2',  # Add your required packages here
        'pillow',
    ],
)
