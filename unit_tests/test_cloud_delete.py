from unit_test_common import execute_csv2_request, initialize_csv2_request, ut_id, sanity_requests, parameters_requests
from sys import argv

# lno: CV - error code identifier.

def main(gvar):
    if not gvar:
        gvar = {}
        if len(argv) > 1:
            initialize_csv2_request(gvar, selections=argv[1])
        else:
            initialize_csv2_request(gvar)

    # 01 - 05
    sanity_requests(gvar, '/cloud/delete/', ut_id(gvar, 'ctg1'), ut_id(gvar, 'ctu3'), ut_id(gvar, 'ctg2'), ut_id(gvar, 'ctu1'))
    
    PARAMETERS = [
        # 06 Give an invalid parameter.
        # 07 Omit cloud_name.
        ('cloud_name', {
            # 08
            '': 'cloud delete value specified for "cloud_name" must not be the empty string.',
            # 09
            'Invalid-Unit-Test': 'cloud delete value specified for "cloud_name" must be all lowercase letters, digits, dashes, underscores, periods, and colons, and cannot contain more than one consecutive dash or start or end with a dash.',
            # 10
            'invalid-unit-test-': 'cloud delete value specified for "cloud_name" must be all lowercase letters, digits, dashes, underscores, periods, and colons, and cannot contain more than one consecutive dash or start or end with a dash.',
            # 11
            'invalid-unit-test!': 'cloud delete value specified for "cloud_name" must be all lowercase letters, digits, dashes, underscores, periods, and colons, and cannot contain more than one consecutive dash or start or end with a dash.',
            # 12
            'invalid-unit-test': 'the request did not match any rows.',
        }, 'invalid-unit-test')
    ]

    parameters_requests(gvar, '/cloud/delete/', ut_id(gvar, 'ctg1'), ut_id(gvar, 'ctu3'), PARAMETERS)

    # 13
    execute_csv2_request(
        gvar, 0, None, 'cloud "{}::{}" successfully deleted.'.format(ut_id(gvar, 'ctg1'), ut_id(gvar, 'ctc1')),
        '/cloud/delete/', group=ut_id(gvar, 'ctg1'), form_data={'cloud_name': ut_id(gvar, 'ctc1')},
        server_user=ut_id(gvar, 'ctu3')
    )

if __name__ == "__main__":
    main(None)
