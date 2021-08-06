
# Supermarket Automation Software

Made a Supermarket Automation Software (SAS) that lets a user log in and perform actions as a manager or a clerk

Allows the user to perform those operations that take place at the payment counters of Supermarkets (like DMart)

## Installation

Requirements for installation and proper working of this software:

- Python 3
- Git

Open the Terminal / Command Prompt and change the directory to the one, where you want to install this software.

Then run the following command.


```bash
git clone https://github.com/kaushal-banthia/supermarket.git
```

## Usage

In the Terminal / Command Prompt, run the following commands one after the other

(These commands are also available in the file 'Commands to Run.txt')

```bash
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## Testing
Some tests have been written for this software during its development and they can be called using the following commands. Using these commands would generate a detailed report for the automated testing results
```bash
py manage.py test
python manage.py test -v 3 --testrunner parth.HtmlTestReporter
```
