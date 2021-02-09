import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
log = logging.getLogger(__name__)


class OdmLibraryMixinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''OD Mekong agreement plugin.'''
    plugins.implements(plugins.IRoutes, inherit=True)

    def before_map(self, m):
        m.connect('odm_library_index', '/library_record', controller='package', type='library_record', action='search')
        m.connect('odm_library_new', '/library_record/new', controller='package', type='library_record', action='new')
        m.connect('odm_library_new_resource', '/library_record/new_resource/{id}', controller='package',
                  type='library_record', action='new_resource')
        m.connect('odm_library_read', '/library_record/{id}', controller='package', type='library_record', action='read',
                  ckan_icon='book')
        m.connect('odm_library_edit', '/library_record/edit/{id}', controller='package', type='library_record',
                  action='edit')
        m.connect('odm_library_delete', '/library_record/delete/{id}', controller='package', type='library_record',
                  action='delete')
        return m

