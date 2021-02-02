import unittest
import web_tests.web_test_setup_cleanup as wtsc
import web_tests.web_test_assertions as wta
import web_tests.web_test_page_objects as pages

class TestWebUser(unittest.TestCase):
    """A class to test user operations via the web interface."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2)
        cls.page = pages.UsersPage(cls.driver)
        print("\nUser Tests:")

    def setUp(self):
        wtsc.get_homepage(self.driver)
        self.page.click_top_nav('Users')

    def test_web_user_find(self):
        # Finds the users page
        pass

    def test_web_user_add_with_group(self):
        # Adds a user who's in a group
        user_name = self.gvar['user'] + '-wiu5'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.side_button_exists(user_name))
        self.assertTrue(self.page.group_box_checked(group_name))
        wta.assertAddedWithAttribute('user', user_name, 'user_groups', group_name)

    def test_web_user_add_without_group(self):
        # Adds a user who's not in any groups
        user_name = self.gvar['user'] + '-wiu6'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_superuser_checkbox()
        self.page.click_add_user()
        self.assertTrue(self.page.side_button_exists(user_name))
        wta.assertAddedWithAttribute('user', user_name, 'user_groups', 'None')

    def test_web_user_add_superuser(self):
        # Adds a super user
        user_name = self.gvar['user'] + '-wiu7'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.side_button_exists(user_name))
        self.assertTrue(self.page.superuser_box_checked())
        wta.assertAddedWithAttribute('user', user_name, 'is_superuser', '1')

    def test_web_user_add_regular_user(self):
        # Adds a non-super user
        user_name = self.gvar['user'] + '-wiu8'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.side_button_exists(user_name))
        self.assertFalse(self.page.superuser_box_checked())
        wta.assertAddedWithAttribute('user', user_name, 'is_superuser', '0')

    def test_web_user_add_without_username(self):
        # Tries to add a user without a username
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.error_message_displayed())

    def test_web_user_add_with_conflicting_username(self):
        # Tries to add a user with a username that's already taken
        user_name = self.gvar['user'] + '-wiu1'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_password(self.gvar['user_secret'])
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasAttribute('user', user_name, 'is_superuser', '0')
        
    def test_web_user_add_without_password(self):
        # Tries to add a user without a password
        user_name = self.gvar['user'] + '-wiu9'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertNotAdded('user', user_name)

    def test_web_user_add_mismatched_passwords(self):
        # Tries to add a user with a non-matching "confirm password"
        user_name = self.gvar['user'] + '-wiu9'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_add_button()
        self.page.type_user_name(user_name)
        self.page.type_password(self.gvar['user_secret'], 'incorrect_password')
        self.page.click_superuser_checkbox()
        self.page.click_group_checkbox(group_name)
        self.page.click_add_user()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertNotAdded('user', user_name)

    def test_web_user_edit_change_password(self):
        # Changes a user's password
        user_name = self.gvar['user'] + '-wiu4'
        self.page.click_side_button(user_name)
        self.page.type_password(user_name + '-password')
        self.page.click_update_user()
        # TODO: Assertion?
        self.assertFalse(self.page.error_message_displayed())

    def test_web_user_edit_mismatched_passwords(self):
        # Tries to change a user's password with a non-matching "confirm password"
        user_name = self.gvar['user'] + '-wiu4'
        self.page.click_side_button(user_name)
        self.page.type_password(user_name + '-password', 'incorrect_password')
        self.page.click_update_user()
        self.assertTrue(self.page.error_message_displayed())

    @unittest.skip("No current infrastructure to test this.")
    def test_web_user_edit_change_cert_cn(self):
        # Changes a user's certificate common name
        pass

    def test_web_user_edit_change_superuser_status(self):
        # Changes a regular user to a super user
        user_name = self.gvar['user'] + '-wiu4'
        self.page.click_side_button(user_name)
        self.page.click_superuser_checkbox()
        self.page.click_update_user()
        self.assertTrue(self.page.superuser_box_checked())
        wta.assertHasAttribute('user', user_name, 'is_superuser', '1')

    def test_web_user_edit_add_to_group(self):
        # Adds a user to a group
        user_name = self.gvar['user'] + '-wiu4'
        group_name = self.gvar['user'] + '-wig3'
        self.page.click_side_button(user_name)
        self.page.click_group_checkbox(group_name)
        self.page.click_update_user()
        self.assertTrue(self.page.group_box_checked(group_name))
        wta.assertHasAttribute('user', user_name, 'user_groups', group_name)

    def test_web_user_edit_remove_from_group(self):
        # Removes a user from a group
        user_name = self.gvar['user'] + '-wiu4'
        group_name = self.gvar['user'] + '-wig1'
        self.page.click_side_button(user_name)
        self.page.click_group_checkbox(group_name)
        self.page.click_update_user()
        self.assertFalse(self.page.group_box_checked(group_name))
        wta.assertHasNotAttribute('user', user_name, 'user_groups', group_name)

    def test_web_user_delete(self):
        # Deletes a user
        user_name = self.gvar['user'] + '-wiu3'
        self.page.click_side_button(user_name)
        self.page.click_delete_button()
        self.page.click_delete_modal()
        self.assertFalse(self.page.side_button_exists(user_name))
        wta.assertDeleted('user', user_name)

    @classmethod
    def tearDownClass(cls):
        wtsc.cleanup(cls)

if __name__ == "__main__":
    unittest.main()