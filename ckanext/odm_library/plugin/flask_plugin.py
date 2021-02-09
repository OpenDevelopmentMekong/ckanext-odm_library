import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
log = logging.getLogger(__name__)


class OdmLibraryMixinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''OD Mekong agreement plugin.'''
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config):
        '''Update plugin config'''

        toolkit.add_template_directory(config, '../templates-2.9')
        toolkit.add_public_directory(config, '../public')
