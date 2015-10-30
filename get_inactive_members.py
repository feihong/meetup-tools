import arrow
import members
from string import Template
import settings


def get_members_who_have_not_attended(cutoff_date, members):
    result = list(m for m in members
        if m['Joined Group on'] < cutoff_date and
           m['Meetups attended'] == 0 and
           m['Name'] not in settings.EXCEPTIONS)
    result.sort(key=lambda x: x['Joined Group on'])
    return result


def get_members_who_have_not_visited(cutoff_date, members):
    result = list(m for m in members
        if m['Last visited group on'] < cutoff_date and
           m['Name'] not in settings.EXCEPTIONS)
    result.sort(key=lambda x: x['Joined Group on'])
    return result


def print_members(members, message):
    count = 0
    for i, m in enumerate(members, 1):
        print i, m['Joined Group on'], m['Name'], '->', m['URL of Member Profile']
        count += 1

    message = Template(message).substitute(dict(count=count))
    print '\n' + message


if __name__ == '__main__':
    members = list(members.get_members(settings.SHORT_NAME, settings.ADMIN_EMAIL))
    now = arrow.now()

    # Get members who joined more than 6 months ago and have not yet attended a
    # single event.
    cutoff = now.replace(months=-6).replace(day=1)
    cutoff_date = cutoff.date()
    subset = get_members_who_have_not_attended(cutoff_date, members)

    print_members(
        subset,
        'Members who joined before %s but have not attended any events: $count' % cutoff_date)

    # Get members who haven't visited the site in a year.
    cutoff = now.replace(months=-12).replace(day=1)
    cutoff_date = cutoff.date()
    subset = get_members_who_have_not_visited(cutoff_date, members)

    print_members(
        subset,
        'Members who have not visited the meetup group site since %s: $count' % cutoff_date)

    # print 'Press ENTER to delete inactive members'
    # yes = raw_input()
    #
    # remover = meetuptools.MemberRemover(
    #     settings.SHORT_NAME, settings.REMOVAL_EXPLANATION)
    # for i, member in enumerate(result, 1):
    #     print 'Removing member %s (%d of %d)' % (member['Name'], i, len(members))
    #     remover.remove(member)
