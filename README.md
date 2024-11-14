# Cython in a repl
This repl runs [Cython](https://cython.org/), which is a language that aims to be a superset of Python. Cython compiles your Python code to C, thus leveraging the speed of C while retaining the benefits of Python. Using Cython allows great improvements in the preformance of your Python programs.

## Usage
For a tutorial on Cython, look [here](https://www.peterbaumgartner.com/blog/intro-to-just-enough-cython-to-be-useful/). This repl already has Cython installed, and `setup.py` configured. The `.replit` file has been set up so that it automatically compiles your code with `python setup.py build_ext --inplace` before running your main script. `setup.py` also manages your .c and .so files behind-the-scenes so that you don't need to worry about them. All you need to do is to write your Python code in main.py, and your Cython code in main_cy.pyx!

## Notice
This template only supports files in your main directory. If you want to customize your project structure (eg. add folders) you will need to `show hidden files` and configure setup.py yourself.