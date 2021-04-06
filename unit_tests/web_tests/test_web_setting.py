import unittest
import web_tests.web_test_setup_cleanup as wtsc
import web_tests.web_test_assertions_v2 as wta
import web_tests.web_test_page_objects as pages
import web_tests.web_test_helpers as helpers

class TestWebSettingCommon(unittest.TestCase):
    """A class for the user settings tests that should be repeated in all iterations."""

    @classmethod
    def setUpClass(cls):
        cls.page = pages.SettingsPage(cls.driver)
        cls.status_page = pages.StatusPage(cls.driver)
        cls.oversize = cls.gvar['oversize']

    def setUp(self):
        helpers.get_homepage(self.driver)
        self.page.click_top_nav('User Settings')

    def test_web_setting_find(self):
        # Finds the settings page
        pass

    def test_web_setting_update_password(self):
        # Updates the current user's password
        password = self.gvar['user'] + '-password'
        self.page.click_side_button(self.user)
        self.page.type_password(password)
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        helpers.get_homepage_login(self.driver, self.user, password)
        self.page.click_top_nav_with_login('User Settings', self.user, password)
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_update_user()
        helpers.get_homepage_login(self.driver, self.user, self.gvar['user_secret'])
        self.page.click_top_nav_with_login('User Settings', self.user, self.gvar['user_secret'])

    def test_web_setting_update_password_mismatched(self):
        # Tries to update the current user's password with mismatched passwords
        self.page.click_side_button(self.user)
        self.page.type_password(self.gvar['user'] + '-password1', self.gvar['user'] + '-password2')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())

    def test_web_setting_update_password_too_short(self):
        # Tries to update the current user's password to one that's too short
        self.page.click_side_button(self.user)
        self.page.type_password('Aa1')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())

    def test_web_setting_update_password_without_uppercase(self):
        # Tries to update the current user's password to one without uppercase letters
        self.page.click_side_button(self.user)
        self.page.type_password('abcd1234')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())

    def test_web_setting_update_password_without_lowercase(self):
        # Tries to update the current user's password to one without lowercase letters
        self.page.click_side_button(self.user)
        self.page.type_password('ABCD1234')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())

    def test_web_setting_update_password_without_numbers(self):
        self.page.click_side_button(self.user)
        self.page.type_password('ABCDabcd')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())

    def test_web_setting_update_global_view_on_status_page(self):
        # Update's the current user's "enabled global view on status page" setting
        self.page.click_side_button(self.user)
        self.page.click_global_view_checkbox()
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'flag_global_status', '1', settings=True, server=self.server)
        self.page.click_top_nav('Status')
        self.assertTrue(self.status_page.job_group_exists(self.gvar['user'] + '-wig0'))
        self.assertTrue(self.status_page.job_group_exists(self.global_group))

    def test_web_setting_update_jobs_by_target_alias_on_status_page(self):
        # Updates the current user's "enabled jobs by target alias on status page" setting
        self.page.click_side_button(self.user)
        self.page.click_jobs_by_alias_checkbox()
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'flag_jobs_by_target_alias', '1', settings=True, server=self.server)
        self.page.click_top_nav('Status')
        self.assertTrue(self.status_page.aliases_displayed())

    def test_web_setting_update_foreign_global_vm_on_status_page(self):
        # Updates the current user's "enabled foreign/global VM information on status page" setting
        self.page.click_side_button(self.user)
        self.page.click_foreign_global_vms_checkbox()
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'flag_show_foreign_global_vms', '1', settings=True, server=self.server)
        self.page.click_top_nav('Status')
        self.assertTrue(self.status_page.foreign_global_vms_visible())

    def test_web_setting_update_slot_detail_on_status_page(self):
        # Updates the current user's "enabled slot detail on status page" setting
        self.page.click_side_button(self.user)
        self.page.click_slot_detail_checkbox()
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'flag_show_slot_detail', '0', settings=True, server=self.server)

    def test_web_setting_update_slot_flavor_info_on_status_page(self):
        # Updates the current user's "enabled slot flavor info on status page" setting
        self.page.click_side_button(self.user)
        self.page.click_slot_flavor_info_checkbox()
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'flag_show_slot_flavors', '0', settings=True, server=self.server)

    def test_web_setting_update_status_refresh_interval_by_blank(self):
        # Updates the current user's status page refresh interval by typing it in the blank
        self.page.click_side_button(self.user)
        self.page.type_status_refresh('20')
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'status_refresh_interval', '20', settings=True, server=self.server)

    def test_web_setting_update_status_refresh_interval_by_blank_float(self):
        # Tries to update the current user's status page refresh interval to a float by typing it in the blank
        self.page.click_side_button(self.user)
        self.page.type_status_refresh('30.5')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())
        self.assertTrue(self.page.status_refresh_popup_exists())
        wta.assertHasNotAttribute('settings', self.user, 'status_refresh_interval', '30.5', settings=True, server=self.server)

    def test_web_setting_update_status_refresh_interval_by_blank_string(self):
        # Tries to update the current user's status page refresh interval to a string by typing it in the blank
        self.page.click_side_button(self.user)
        self.page.type_status_refresh('invalid-web-test')
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())
        self.assertTrue(self.page.status_refresh_popup_exists())
        wta.assertHasNotAttribute('settings', self.user, 'status_refresh_interval', 'invalid-web-test', settings=True, server=self.server)

    def test_web_setting_update_status_refresh_interval_by_blank_too_big(self):
        # Tries to update the current user's status page refresh interval to an int that's too big for the database by typing it in the blank
        self.page.click_side_button(self.user)
        self.page.type_status_refresh(str(self.oversize['int_11']))
        self.page.click_update_user()
        #self.assertTrue(self.page.error_message_displayed())
        #self.assertTrue(self.page.status_refresh_popup_exists())
        wta.assertHasNotAttribute('settings', self.user, 'status_refresh_interval', str(self.oversize['int_11']), settings=True, server=self.server)

    def test_web_setting_update_status_refresh_interval_by_arrow_keys(self):
        # Updates the current user's status page refresh interval using the arrow keys
        self.page.click_side_button(self.user)
        self.page.increment_status_refresh_by_arrows(40)
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'status_refresh_interval', '40', settings=True, server=self.server)

    @unittest.skip("Probably takes too long to be worth running")
    def test_web_setting_update_status_refresh_interval_by_arrow_keys_too_big(self):
        # Updates the current user's status page refresh interval to an int that's too long for the database using the arrow keys
        self.page.click_side_button(self.user)
        self.page.increment_status_refresh_by_arrows(self.oversize['int_11'])
        self.page.click_update_user()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasNotAttribute('settings', self.user, 'status_refresh_interval', str(self.oversize['int_11']), settings=True, server=self.server)

    def test_web_setting_update_default_group(self):
        # Updates the current user's default group
        self.page.click_side_button(self.user)
        self.page.select_default_group(self.global_group)
        self.page.click_update_user()
        self.assertFalse(self.page.error_message_displayed())
        wta.assertHasAttribute('settings', self.user, 'default_group', self.global_group, settings=True, server=self.server)

    @classmethod
    def tearDownClass(cls):
        wtsc.cleanup(cls)

class TestWebSettingSuperUserFirefox(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Firefox, with a super user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2, ['settings', 'servers'], browser='firefox')
        super(TestWebSettingSuperUserFirefox, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis2'
        cls.user = cls.gvar['user'] + '-wiu2'
        cls.global_group = cls.gvar['user'] + '-wig2'
        print("\nUser Settings Tests (Super User):")

class TestWebSettingRegularUserFirefox(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Firefox, with a regular user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 1, ['settings', 'servers'], browser='firefox')
        super(TestWebSettingRegularUserFirefox, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis1'
        cls.user = cls.gvar['user'] + '-wiu1'
        cls.global_group = cls.gvar['user'] + '-wig1'
        print("\nUser Settings Tests (Regular User):")

class TestWebSettingSuperUserChromium(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Chromium, with a super user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2, ['settings', 'servers'], browser='chromium')
        super(TestWebSettingSuperUserChromium, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis2'
        cls.user = cls.gvar['user'] + '-wiu2'
        cls.global_group = cls.gvar['user'] + '-wig2'
        print("\nUser Settings Tests (Chromium) (Super User):")

class TestWebSettingRegularUserChromium(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Chromium, with a regular user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 1, ['settings', 'servers'], browser='chromium')
        super(TestWebSettingRegularUserChromium, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis1'
        cls.user = cls.gvar['user'] + '-wiu1'
        cls.global_group = cls.gvar['user'] + '-wig1'
        print("\nUser Settings Tests (Chromium) (Regular User):")

class TestWebSettingSuperUserOpera(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Opera, with a super user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2, ['settings', 'servers'], browser='opera')
        super(TestWebSettingSuperUserOpera, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis2'
        cls.user = cls.gvar['user'] + '-wiu2'
        cls.global_group = cls.gvar['user'] + '-wig2'
        print("\nUser Settings Tests (Opera) (Super User):")

class TestWebSettingRegularUserOpera(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Opera, with a regular user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 1, ['settings', 'servers'], browser='opera')
        super(TestWebSettingRegularUserOpera, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis1'
        cls.user = cls.gvar['user'] + '-wiu1'
        cls.global_group = cls.gvar['user'] + '-wig1'
        print("\nUser Settings Tests (Opera) (Regular User):")

class TestWebSettingSuperUserChrome(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Chrome, with a super user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2, ['settings', 'servers'], browser='chrome')
        super(TestWebSettingSuperUserChrome, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis2'
        cls.user = cls.gvar['user'] + '-wiu2'
        cls.global_group = cls.gvar['user'] + '-wig2'
        print("\nUser Settings Tests (Chrome) (Super User):")

class TestWebSettingRegularUserChrome(TestWebSettingCommon):
    """A class to test user settings operations via the web interface, in Chrome, with a regular user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 1, ['settings', 'servers'], browser='chrome')
        super(TestWebSettingRegularUserChrome, cls).setUpClass()
        cls.server = cls.gvar['user'] + '-wis1'
        cls.user = cls.gvar['user'] + '-wiu1'
        cls.global_group = cls.gvar['user'] + '-wig1'
        print("\nUser Settings Tests (Chrome) (Regular User):")

if __name__ == "__main__":
    unittest.main()
