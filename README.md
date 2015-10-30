# Meetup Tools

Make sure you have virtualenvwrapper installed.

```
mkvirtualenv meetup
pip install -r requirements.txt
```

Create a file called `settings_local.py`. Its contents should look something like this:

```python
SHORT_NAME = 'cow-tipping'
FULL_NAME = 'Chicago Cow Tipping Meetup Group'
CONTACT_EMAIL = 'chicago.cow.tipping@gmail.com'
ADMIN_EMAIL = 'chicago.cow.tipping@gmail.com'
SIGNATURE = 'Julius Caesar'

EXCEPTIONS = """
Han Solo
John Smith
Edward Scissorhands
"""

REMOVAL_EXPLANATION = """
Hi $name,

You have been removed from the $full_name due to inactivity. If you would like to become an active member again, simply go to http://www.meetup.com/${short_name}/ and create a new profile. Note that our events remain visible even if you are not a member, although you will not receive email updates about them. If you have any questions, please email us at ${email}.

Sincerely,
$signature
"""
```
