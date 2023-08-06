import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


setuptools.setup(
    	name="WtfPy",
    	version="0.0.2",
    	author="Zyycyx",
    	author_email="peterschmidt5575@gmail.com",
    	description="A basic module to work with memory addresses and references.",
    	long_description=README,
    	long_description_content_type="text/markdown",
    	url="https://github.com/Zyycyx/wtfpy",
    	packages=setuptools.find_packages(),
    	classifiers=[
        	"Programming Language :: Python :: 3.8",
        	"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
    	],
	include_package_data=True,
	install_requires=['sys'],
    	python_requires='>=3.8',
)

