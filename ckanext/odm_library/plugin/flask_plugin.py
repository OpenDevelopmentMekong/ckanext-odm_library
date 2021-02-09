import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
log = logging.getLogger(__name__)


class OdmLibraryMixinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''OD Mekong agreement plugin.'''

    plugins.implements(plugins.IBlueprint)
