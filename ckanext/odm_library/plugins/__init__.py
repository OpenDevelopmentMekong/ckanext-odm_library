import ckan
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from beaker.middleware import SessionMiddleware
import sys
import os
from ckanext.odm_library.lib import odm_library_helper
from urlparse import urlparse
from ckan.common import config
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

try:
    toolkit.requires_ckan_version("2.9")
except CkanVersionException:
    from ckanext.odm_laws.plugin.pylons_plugin import OdmLibraryMixinPlugin
else:
    from ckanext.odm_laws.plugin.flask_plugin import OdmLibraryMixinPlugin


def _get_author_list(pkg):
  from ckanext.odm_dataset_ext import helpers as h
  fields = ('marc21_100', 'marc21_110', 'marc21_700', 'marc21_710')
  return ', '.join([s for s in [h.get_currentlang_data(field, pkg) for field in fields] if s])


class OdmLibraryPlugin(OdmLibraryMixinPlugin):
  '''OD Mekong library plugin.'''

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IPackageController, inherit=True)

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_public_directory(config, 'public')


  def get_helpers(self):
    '''Register the plugin's functions above as a template helper function.'''

    return {
      'odm_library_get_dataset_type': odm_library_helper.get_dataset_type,
      'odm_library_validate_fields': odm_library_helper.validate_fields,
      'odm_library_author_list': _get_author_list,
    }


  def after_create(self, context, pkg_dict):

    dataset_type = context['package'].type if 'package' in context else pkg_dict['type']

    if dataset_type == 'library_record':
      log.debug('after_create: %s', pkg_dict['name'])

      review_system = toolkit.asbool(config.get("ckanext.issues.review_system", False))
      if review_system:
        if pkg_dict['type'] == 'library_record':
          odm_library_helper.create_default_issue_library_record(pkg_dict)
