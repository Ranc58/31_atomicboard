# Integration tests for AtomicBoard

The aim of this project is to cover by integration tests the web service AtomicBoard. The stage server is available by address 
[atomicboard.devman.org](http://atomicboard.devman.org).

What is being tested?
- Display all tasks on site.
- Switch tasks conditions as 'close'.
- Edit task.
- Drag&drop tasks between columns.
- Creating new tasks.

# How to install
1. Recomended use venv or virtualenv for better isolation.\
   Venv setup example: \
   `python3 -m venv myenv`\
   `source myenv/bin/activate`
2. Install requirements: \
   `pip3 install -r requirements.txt` (alternatively try add `sudo` before command)
3. If you don't have `PhantomJS` - download and install from official site: [phantomjs.org/download](http://phantomjs.org/download.html)
# How to launch
Run `python3 tests.py`
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
