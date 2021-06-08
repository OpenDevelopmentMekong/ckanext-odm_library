import pytest
from ckanext.odm_library.tests import helpers as test_h
import ckan.plugins.toolkit as toolkit
import ckan.tests.helpers as helpers
from ckan.tests import factories
from ckan import model


@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestLibrarysSchema:

    def setup(self):
        self._org = factories.Organization()
        self._sysadmin = factories.Sysadmin()
        self.context = {
            "user": self._sysadmin['name'],
            "model": model,
            "session": model.Session
        }

    def test_odm_library_create(self):
        pkg = test_h.OdmLibraryDataset().create(
            type='library_record',
            odm_reference_document="test source",
            document_type="case_studies",
            odm_language=["en", "th"]
        )
        assert "type" in pkg
        assert pkg.get('type', '') == 'library_record'
        assert "notes_translated" in pkg
        assert pkg.get('odm_reference_document', "") == "test source"
        assert pkg.get('document_type', "") == "case_studies"
        assert len(pkg.get('odm_language', [''])) == 2

    def test_library_update(self):
        pkg = test_h.OdmLibraryDataset().create(
            type='library_record',
        )

        pkg_show = toolkit.get_action('package_show')(self.context, {"id": pkg['id']})

        assert pkg['id'] == pkg_show['id']
        assert pkg_show['type'] == 'library_record'

        pkg_show['odm_reference_document'] = "test update"
        pkg_sh = toolkit.get_action('package_update')(self.context, pkg_show)

        assert "odm_reference_document" in pkg_sh and pkg_sh['odm_reference_document'] == "test update"

    def test_library_delete(self):
        pkg = test_h.OdmLibraryDataset().create(
            type='library_record'
        )
        toolkit.get_action('package_delete')(self.context, {"id": pkg['id']})
        pkg_show = toolkit.get_action('package_show')(self.context, {"id": pkg['id']})
        assert pkg_show['state'] == 'deleted'
