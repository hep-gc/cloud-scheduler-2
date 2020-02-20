from unit_test_common import execute_csv2_request, initialize_csv2_request, ut_id, sanity_requests, parameters_requests
from sys import argv

# lno: GV - error code identifier.

def main(gvar):
    if not gvar:
        gvar = {}
        if len(argv) > 1:
            initialize_csv2_request(gvar, selections=argv[1])
        else:
            initialize_csv2_request(gvar)

    # 01 - 05
    sanity_requests(gvar, '/group/delete/', ut_id(gvar, 'gtg5'), ut_id(gvar, 'gtu5'), ut_id(gvar, 'gtg7'), ut_id(gvar, 'gtu2'))

    # 3
    execute_csv2_request(
        gvar, 2, None, 'HTTP response code 403, forbidden.',
        '/group/delete/',
        server_user=ut_id(gvar, 'gtu3')
    )

    # 4
    execute_csv2_request(
        gvar, 1, 'GV', 'group delete request did not contain mandatory parameter "group_name".',
        '/group/delete/',
        server_user=ut_id(gvar, 'gtu5')
    )

    PARAMETERS = [
        # Omit group_name.
        ('group_name', {
            '': 'TODO',
        }, 'invalid-unit-test')
    ]

    parameters_requests(gvar, '/group/delete/', ut_id(gvar, 'gtg5'), ut_id(gvar, 'gtu5'), ut_id(gvar, 'gtg7'), ut_id(gvar, 'gtu2'), PARAMETERS)

    # 5
    execute_csv2_request(
        gvar, 1, 'GV', 'request contained a bad parameter "invalid-unit-test".',
        '/group/delete/', form_data={'invalid-unit-test': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 6
    execute_csv2_request(
        gvar, 1, 'GV', 'cannot switch to invalid group "invalid-unit-test".',
        '/group/delete/', group='invalid-unit-test',
        server_user=ut_id(gvar, 'gtu5')
    )

    # 7
    execute_csv2_request(
        gvar, 1, 'GV', 'group delete request did not contain mandatory parameter "group_name".',
        '/group/delete/', group=ut_id(gvar, 'gtg5'),
        server_user=ut_id(gvar, 'gtu5')
    )

    # 8
    execute_csv2_request(
        gvar, 1, 'GV', 'group delete "invalid-unit-test" failed - the request did not match any rows.',
        '/group/delete/', form_data={'group_name': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 9
    execute_csv2_request(
        gvar, 1, 'GV', 'group delete value specified for "group_name" must be all lower case, numeric digits, and dashes but cannot start or end with dashes.',
        '/group/delete/', form_data={'group_name': 'Invalid-Unit-Test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # 10
    execute_csv2_request(
        gvar, 1, 'GV', 'group delete value specified for "user_option" must be one of the following options: [\'add\', \'delete\'].',
        '/group/delete/', form_data={'user_option': 'invalid-unit-test'},
        server_user=ut_id(gvar, 'gtu5')
    )

    # i1
    execute_csv2_request(
        gvar, 0, None, 'group "{}" successfully deleted.'.format(ut_id(gvar, 'gtg6')),
        '/group/delete/', form_data={'group_name': ut_id(gvar, 'gtg6')},
        server_user=ut_id(gvar, 'gtu5')
    )

if __name__ == "__main__":
    main(None)
