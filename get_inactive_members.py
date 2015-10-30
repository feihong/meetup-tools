import arrow
import members
import settings


if __name__ == '__main__':
    now = arrow.now()
    cutoff = now.replace(months=-6).replace(day=1)
    cutoff_date = cutoff.date()

    # Get members who joined more than 6 months ago and have not yet attended a
    # single event.
    members = members.get_members(settings.SHORT_NAME, settings.ADMIN_EMAIL)
    result = list(m for m in members
        if m['Joined Group on'] < cutoff_date and
           m['Meetups attended'] == 0 and
           m['Name'] not in settings.EXCEPTIONS)
    result.sort(key=lambda x: x['Joined Group on'])

    count = 0
    for i, m in enumerate(result, 1):
        print i, m['Joined Group on'], m['Name'], '->', m['URL of Member Profile']
        count += 1

    print '\nMembers who joined before %s but have not attended any events: %d' % (
        cutoff_date, count)
    # print 'Press ENTER to delete inactive members'
    # yes = raw_input()
    #
    # remover = meetuptools.MemberRemover(
    #     settings.SHORT_NAME, settings.REMOVAL_EXPLANATION)
    # for i, member in enumerate(result, 1):
    #     print 'Removing member %s (%d of %d)' % (member['Name'], i, len(members))
    #     remover.remove(member)
