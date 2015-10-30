import sys
import os
import os.path as op
import datetime
import unicodecsv
import requests
import keyring


LOGIN_URL = 'https://secure.meetup.com/login/'
FILE_NAME = 'members_list.csv'
INT_FIELDS = ['Meetups attended', 'No shows']
DATE_FIELDS = ['Joined Group on', 'Last visited group on']


def get_members(short_name, admin_email):
    if not recent_file_exists():
        print 'No recent members file exists, downloading...'
        download_file(short_name, admin_email)

    with open(FILE_NAME) as csvfile:
        reader = unicodecsv.DictReader(csvfile, delimiter='\t')
        for item in reader:
            replace_with_ints(item, INT_FIELDS)
            replace_with_dates(item, DATE_FIELDS)
            yield item


def download_file(short_name, admin_email):
    password = keyring.get_password('meetup', admin_email)
    if password is None:
        print 'Please enter the password for %s:' % admin_email,
        password = raw_input().strip()
        keyring.set_password('meetup', admin_email, password)

    sess = requests.Session()

    res = sess.get(LOGIN_URL)
    token = sess.cookies['MEETUP_CSRF']
    data = dict(
        email=admin_email,
        password=password,
        rememberme='on',
        token=token,
        submitButton='Log In',
        returnUri='http://www.meetup.com',
        op='login',
    )
    res = sess.post(LOGIN_URL, data=data)
    # with open('response.html', 'w') as fp: fp.write(res.content)

    file_url = 'http://www.meetup.com/%s/members/?op=csv' % short_name
    res = sess.get(file_url)
    with open(FILE_NAME, 'wb') as fp:
        fp.write(res.content)


def recent_file_exists():
    "Returns True if the file is there and it was last modified today."
    if op.exists(FILE_NAME):
        create_date = datetime.datetime.fromtimestamp(op.getmtime(FILE_NAME)).date()
        return create_date >= datetime.date.today()

    return False


def replace_with_ints(dict_, keys):
    "For a given dict, replace some of its values with int objects."
    for key in keys:
        dict_[key] = int(dict_[key])


def replace_with_dates(dict_, keys):
    "For a given dict, replace some of its values with date objects."
    format = '%m/%d/%Y'

    for key in keys:
        new_val = datetime.datetime.strptime(dict_[key], format).date()
        dict_[key] = new_val
