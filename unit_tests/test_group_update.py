from unit_test_common import execute_csv2_request, initialize_csv2_request, ut_id
from sys import argv

# lno: GV - error code identifier.

def main(gvar):
    if not gvar:
        gvar = {}
        if len(argv) > 1:
            initialize_csv2_request(gvar, selections=argv[1])
        else:
            initialize_csv2_request(gvar)

    # 01
    execute_csv2_request(
        gvar, 2, None, 'HTTP response code 401, unauthorized.',
        '/group/update/',
        server_user='invalid-unit-test'
    )

    # 02
    execute_csv2_request(
        gvar, 2, None, 'HTTP response code 403, forbidden.',
        '/group/update/',
        server_user=ut_id(gvar, 'gtu1') 
    )

    # 03
    execute_csv2_request(
        gvar, 2, None, 'HTTP response code 403, forbidden.',
        '/group/update/',
        server_user=ut_id(gvar, 'gtu3') 
    )

    # 04
    execute_csv2_request(
        gvar, 1, None, 'user "{}" is not a member of any group.'.format(ut_id(gvar, 'gtu2')),
        '/group/update/',
        server_user=ut_id(gvar, 'gtu2') 
    )

    # 05
    execute_csv2_request(
        gvar, 1, 'GV', 'invalid method "GET" specified.',
        '/group/update/',
        server_user=ut_id(gvar, 'gtu5')
    )

    # 06
    execute_csv2_request(
        gvar, 1, 'GV', 'cannot switch to invalid group "invalid-unit-test".',
        '/group/update/', group='invalid-unit-test',
        server_user=ut_id(gvar, 'gtu5')
    )

    # 07
    execute_csv2_request(
        gvar, 1, 'GV', 'request contained a bad parameter "invalid-unit-test".',
        '/group/update/', form_data={'invalid-unit-test': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 08
    execute_csv2_request(
        gvar, 1, 'GV', 'value specified for "group_name" must be all lower case, numeric digits, and dashes but cannot start or end with dashes.',
        '/group/update/', form_data={'group_name': ut_id(gvar, 'Gtg1')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 09
    execute_csv2_request(
        gvar, 1, 'GV', 'value specified for "group_name" must be all lower case, numeric digits, and dashes but cannot start or end with dashes.',
        '/group/update/', form_data={'group_name': ut_id(gvar, 'gtg!1')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 10
    execute_csv2_request(
        gvar, 1, 'GV', 'value specified for "group_name" must be all lower case, numeric digits, and dashes but cannot start or end with dashes.',
        '/group/update/', form_data={'group_name': ut_id(gvar, 'gtg1-')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 11
    execute_csv2_request(
        gvar, 1, 'GV', 'group update must specify at least one field to update.',
        '/group/update/', form_data={'group_name': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 12
    execute_csv2_request(
        gvar, 1, 'GV', 'value specified for "user_option" must be one of the following options: [\'add\', \'delete\'].',
        '/group/update/', form_data={'user_option': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 13
    execute_csv2_request(
        gvar, 1, 'GV', 'group update request did not contain mandatory parameter "group_name".',
        '/group/update/', form_data={'username': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 14
    execute_csv2_request(
        gvar, 1, 'GV', 'the request did not match any rows.',
        '/group/update/', form_data={
            'group_name': 'invalid-unit-test',
            'htcondor_fqdn': 'invalid-unit-test'
        },
        server_user=ut_id(gvar, 'gtu5')
    )

    ''' Currently htcondor_fqdn is allowed to be the empty string.
    execute_csv2_request(
        gvar, 1, 'GV', 'group update parameter "htcondor_fqdn" contains an empty string which is specifically disallowed.',
        '/group/update/', form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'htcondor_fqdn': ''
        },
        server_user=ut_id(gvar, 'gtu5')
    )
    '''

    # 15
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/', 
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'htcondor_fqdn': 'unit-test-group-four-update.ca'
        },
        server_user=ut_id(gvar, 'gtu5')
    )

    # 16
    execute_csv2_request(
        gvar, 0, None, None,
        '/group/list/',
        expected_list='group_list', list_filter={'group_name': ut_id(gvar, 'gtg4')},
        values={'group_name': ut_id(gvar, 'gtg4'), 'htcondor_fqdn': 'unit-test-group-four-update.ca'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 17
    execute_csv2_request(
        gvar, 1, 'GV', 'specified user "invalid-unit-test" does not exist.',
        '/group/update/', 
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': 'invalid-unit-test'
        },
        server_user=ut_id(gvar, 'gtu5')
    )

    # 18
    execute_csv2_request(
        gvar, 1, 'GV', 'group update, "{}" failed - user "{}" was specified twice.'.format(ut_id(gvar, 'gtg4'), ut_id(gvar, 'gtu4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': ut_id(gvar, 'gtu4'),
            'username.2': ut_id(gvar, 'gtu4')
        },
        server_user=ut_id(gvar, 'gtu5')
    )

    # 19
    execute_csv2_request(
        gvar, 0, None, None,
        '/group/list/',
        expected_list='group_list', list_filter={'group_name': ut_id(gvar, 'gtg4')},
        values={'group_name': ut_id(gvar, 'gtg4'), 'htcondor_fqdn': 'unit-test-group-four-update.ca'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 20
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': ut_id(gvar, 'gtu4')
        },
        server_user=ut_id(gvar, 'gtu5')
    )

    # 21
    execute_csv2_request(
        gvar, 0, None, None,
        '/group/list/',
        expected_list='group_list', list_filter={'group_name': ut_id(gvar, 'gtg4')},
        values={'group_name': ut_id(gvar, 'gtg4'), 'htcondor_fqdn': 'unit-test-group-four-update.ca'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 22
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu4')},
        values={'user_groups': ut_id(gvar, 'gtg4')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 23 Remove gtu4 (and all others) from gtg4
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username': ''
        },
        server_user=ut_id(gvar, 'gtu5'), html=True
    )

    # 24 Verify that 23 actually removed gtu4 from gtg4
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/', group=ut_id(gvar, 'gtg5'),
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu4')},
        values={'user_groups': None},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 25
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': ut_id(gvar, 'gtu4')
        },
        server_user=ut_id(gvar, 'gtu5'), html=True
    )

    # 26
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu4')},
        values={'user_groups': ut_id(gvar, 'gtg4')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 27
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': ut_id(gvar, 'gtu5')
        },
        server_user=ut_id(gvar, 'gtu5'), html=True
    )

    # 28 Ensure that 27 actually replaced gtu4 with gtu5 in gtg4 (and gtu4 is therefore not in any groups).
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu4')},
        values={'user_groups': None},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 29 We want to check that 27 added gtu5 to gtg4, but if group_add has been run since the last setup, it will have added gtu5 to gtg1.
    # So we remove all users from gtg1, but ignore any error if gtg1 doesn't exist.
    execute_csv2_request(
        gvar, None, None, None,
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg1'),
            'username': ''
        },
        server_user=ut_id(gvar, 'gtu5'), html=True
    )

    # 30 Now we can assume that gtu5 is in only gtg4 and gtg5.
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu5')},
        values={'user_groups': ut_id(gvar, 'gtg4,gtg5')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 31
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully updated.'.format(ut_id(gvar, 'gtg4')),
        '/group/update/',
        form_data={
            'group_name': ut_id(gvar, 'gtg4'),
            'username.1': ut_id(gvar, 'gtu4'),
            'username.2': ut_id(gvar, 'gtu5')
        },
        server_user=ut_id(gvar, 'gtu5'), html=True
    )

    # 32
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu4')},
        values={'user_groups': ut_id(gvar, 'gtg4')},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 33
    execute_csv2_request(
        gvar, 0, None, None,
        '/user/list/',
        expected_list='user_list', list_filter={'username': ut_id(gvar, 'gtu5')},
        values={'user_groups': ut_id(gvar, 'gtg4,gtg5')},
        server_user=ut_id(gvar, 'gtu5')
    )

if __name__ == "__main__":
    main(None)
