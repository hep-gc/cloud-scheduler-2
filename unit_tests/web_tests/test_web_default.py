import unittest
import web_tests.web_test_setup_cleanup as wtsc
import web_tests.web_test_assertions as wta
import web_tests.web_test_page_objects as pages

class TestWebDefaultSuperUser(unittest.TestCase):
    """A class to test default operations via the web interface, with a super user."""

    @classmethod
    def setUpClass(cls):
        wtsc.setup(cls, 2, ['defaults'])
        cls.page = pages.DefaultsPage(cls.driver)
        cls.group_name = cls.gvar['user'] + '-wig1'
        print("\nDefault Tests (Super User):")

    def setUp(self):
        wtsc.get_homepage(self.driver)
        self.page.switch_default_group(self.group_name)
        self.page.click_top_nav('Defaults')

    def test_web_default_find(self):
        pass

# TODO: check longer than 128 character strings (in all files)

    def test_web_default_update_htcondor_fqdn(self):
        group_name = self.gvar['user'] + '-wig2'
        self.page.switch_default_group(group_name)
        self.page.click_side_button(group_name)
        self.page.click_side_tab('Settings')
        self.page.type_htcondor_fqdn('csv2-dev2.heprc.uvic.ca')
        self.page.click_update_group()
        #TODO: make assertions to work with group defaults

    def test_web_default_update_htcondor_container_hostname(self):
        group_name = self.gvar['user'] + '-wig2'
        self.page.switch_default_group(group_name)
        self.page.click_side_button(group_name)
        self.page.click_side_tab('Settings')
        self.page.type_htcondor_container_hostname(self.gvar['user'] + '-host')
        self.page.click_update_group()

    def test_web_default_update_htcondor_other_submitters(self):
        group_name = self.gvar['user'] + '-wig2'
        self.page.swich_default_group(group_name)
        self.page.click_side_button(group_name)
        self.page.click_side_tab('Settings')
        self.page.type_htcondor_other_submitters(self.gvar['user'] + '-wiu1') #change for regular user
        self.page.click_update_group()

    def test_web_default_update_job_cpus(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.type_job_cpus('8')
        self.page.click_update_group()

    def test_web_default_update_job_ram(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.type_job_ram('1024')
        self.page.click_update_group()

    def test_web_default_update_job_disk(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.type_job_disk('4')
        self.page.click_update_group()

    def test_web_default_update_job_swap(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.type_job_swap('2')
        self.page.click_update_group()

    @unittest.skip("TODO: implement")
    def test_web_default_update_vm_keyname(self):
        pass

    def test_web_default_update_vm_image(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.select_vm_image('cirros-0.3.5')
        self.page.click_update_group()

    def test_web_default_update_vm_flavor(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.select_vm_flavor('s8')
        self.page.click_update_group()

    def test_web_default_update_vm_network(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.select_vm_network('private')
        self.page.click_update_group()

    def test_web_default_update_vm_keep_alive(self):
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Settings')
        self.page.type_vm_keep_alive('2048')
        self.page.click_update_group()

    def test_web_default_metadata_add(self):
        # Adds metadata to a group
        metadata_name = self.gvar['user'] + '-wim3.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_tab_exists(metadata_name))
        wta.assertAdded('metadata', metadata_name, self.group_name)

    @unittest.skip("Not working in production (issue 319)")
    def test_web_default_metadata_add_without_name(self):
        # Tries to add metadata to a group without a name
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())

    @unittest.skip("Not working in production (issue 319)")
    def test_web_default_metadata_add_name_with_symbols(self):
        # Tries to add metadata with symbols in its name
        metadata_name = 'inv@|id-web-te$t.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasNotAttribute('cloud', cloud_name, 'metadata_names', metadata_name, self.gvar['base_group'])

    @unittest.skip("Not working in production (issue 319)")
    def test_web_default_metadata_add_name_with_two_dashes(self):
        # Tries to add metadata with two dashes in its name
        metadata_name = 'invalid--web--test.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasNotAttribute('cloud', cloud_name, 'metadata_names', metadata_name, self.gvar['base_group'])

    @unittest.skip("Not working in production (issue 319)")
    def test_web_default_metadata_add_name_with_uppercase(self):
        # Tries to add metadata with uppercase letters in its name
        metadata_name = 'INVALID-WEB-TEST.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasNotAttribute('cloud', cloud_name, 'metadata_names', metadata_name, self.gvar['base_group'])

    @unittest.skip("Not working in production (issue 319)")
    def test_web_default_metadata_add_name_with_starting_ending_dash(self):
        # Tries to add metadata with starting and ending dashes in its name
        metadata_name = '-invalid-web-test-.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())
        wta.assertHasNotAttribute('cloud', cloud_name, 'metadata_names', metadata_name, self.gvar['base_group'])

    def test_web_default_metadata_add_not_enabled(self):
        # Adds metadata to a group without enabling it
        metadata_name = self.gvar['user'] + '-wim4.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.click_metadata_enabled()
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_tab_exists(metadata_name))
        wta.assertAddedWithAttribute('metadata', metadata_name, 'enabled', '0', self.group_name)

    def test_web_default_metadata_add_different_priority_by_typing(self):
        # Adds metadata to a group with a different priority by typing it in the blank
        metadata_name = self.gvar['user'] + '-wim5.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.type_metadata_priority('8')
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_tab_exists(metadata_name))
        wta.assertAddedWithAttribute('metadata', metadata_name, 'priority', '8', self.group_name)

    def test_web_default_metadata_add_different_priority_by_typing_float(self):
        # Tries to add metadata to a cloud with a float value for its priority by typing it in the blank
        metadata_name = self.gvar['user'] + '-wim8.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.type_metadata_priority('8.5')
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_priority_popup_exists())
        self.assertFalse(self.page.metadata_tab_exists(metadata_name))
        wta.assertNotAdded('metadata', metadata_name, self.group_name)

    def test_web_default_metadata_add_different_priority_by_typing_string(self):
        # Tries to metadata to a group with a string value priority by typing it in the blank
        metadata_name = self.gvar['user'] + '-wim8.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.type_metadata_priority('invalid-web-test')
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_priority_popup_exists())
        self.assertFalse(self.page.metadata_tab_exists(metadata_name))
        wta.assertNotAdded('metadata', metadata_name, self.group_name)

    def test_web_default_metadata_add_different_priority_by_arrows(self):
        # Adds metadata to a group with a different priority using the arrow keys
        metadata_name = self.gvar['user'] + '-wim6.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.increment_metadata_priority_by_arrows(16)
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_tab_exists(metadata_name))
        wta.assertAddedWithAttribute('metadata', metadata_name, 'priority', '16', self.group_name)

    def test_web_default_metadata_add_different_mime_type(self):
        # Adds metadata to a group with a different MIME type
        metadata_name = self.gvar['user'] + '-wim7.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.select_metadata_mime_type('ucernvm-config')
        self.page.type_metadata('sample_key: sample_value')
        self.page.click_metadata_add()
        self.assertTrue(self.page.metadata_tab_exists(metadata_name))
        wta.assertAddedWithAttribute('metadata', metadata_name, 'mime_type', 'ucernvm-config', self.group_name)

    @unittest.skip("Not working (supposed to work?)")
    def test_web_group_metadata_add_mismatched_file_type(self):
        # Tries to add metadata to a group with a file that doesn't match its name
        metadata_name = self.gvar['user'] + '-wim8.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata_new()
        self.page.type_metadata_name(metadata_name)
        self.page.type_metadata('invalid-unit-test')
        self.page.click_metadata_add()
        self.assertTrue(self.page.error_message_displayed())
        self.assertFalse(self.page.metadata_tab_exists(metadata_name))
        wta.assertNotAdded('metadata', metadata_name, self.group_name)

    def test_web_default_metadata_update_enabled_status(self):
        # Changes enabled metadata to not enabled
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.click_metadata_enabled()
        self.page.click_metadata_update()
        # TODO: implement checkbox clicked check method
        wta.assertHasAttribute('metadata', metadata_name, 'enabled', '0', self.group_name)

    def test_web_default_metadata_update_priority_by_typing(self):
        # Changes metadata priority by typing in the blank
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.type_metadata_priority('8')
        self.page.click_metadata_update()
        wta.assertHasAttribute('metadata', metadata_name, 'priority', '8', self.group_name)

    def test_web_default_metadata_update_priority_by_typing_float(self):
        # Tries to change metadata priority to a float by typing it in the blank
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.type_metadata_priority('8.5')
        self.page.click_metadata_update()
        self.assertTrue(self.page.metadata_priority_popup_exists())
        wta.assertHasNotAttribute('metadata', metadata_name, 'priority', '8.5', self.group_name)

    def test_web_default_metadata_update_priority_by_typing_string(self):
        # Tries to change metadata priority to a string by typing it in the blank
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.type_metadata_priority('invalid-web-test')
        self.page.click_metadata_update()
        self.assertTrue(self.page.metadata_priority_popup_exists())
        wta.assertHasNotAttribute('metadata', metadata_name, 'priority', 'invalid-web-test', self.group_name)

    def test_web_default_metadata_update_priority_by_arrow_keys(self):
        # Changes metadata priority using the arrow keys
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.increment_metadata_priority_by_arrows(16)
        self.page.click_metadata_update()
        wta.assertHasAttribute('metadata', metadata_name, 'priority', '16', self.group_name)

    def test_web_default_metadata_update_mime_type(self):
        # Changes metadata mime type
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.select_metadata_mime_type('ucernvm-config')
        self.page.click_metadata_update()
        wta.assertHasAttribute('metadata', metadata_name, 'mime_type', 'ucernvm-config', self.group_name)

    def test_web_default_metadata_update_contents(self):
        # Changes metadata text
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.type_metadata('sample_key_2: sample_value_2')
        self.page.click_metadata_update()
        # Note: there appears to be no way to test that this has been updated
        self.assertFalse(self.page.error_message_displayed())

    @unittest.skip("Not working (supposed to work?)")
    def test_web_default_metadata_update_contents_mismatched(self):
        # Tries to change metadata text to something of the wrong file type
        metadata_name = self.gvar['user'] + '-wim1.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.type_metadata('invalid-web-test')
        self.page.click_metadata_update()
        # Note: there appears to be no way to test that this has not been updated
        self.assertTrue(self.page.error_message_displayed())

    def test_web_default_metadata_delete(self):
        # Deletes metadata from a group
        metadata_name = self.gvar['user'] + '-wim2.yaml'
        self.page.click_side_button(self.group_name)
        self.page.click_side_tab('Metadata')
        self.page.click_metadata(metadata_name)
        self.page.click_metadata_delete()
        self.page.click_metadata_delete_modal()
        self.assertFalse(self.page.metadata_tab_exists(metadata_name))
        wta.assertDeleted('metadata', metadata_name, self.group_name)

    @classmethod
    def tearDownClass(cls):
        wtsc.cleanup(cls)

if __name__ == "__main__":
    unittest.main()
