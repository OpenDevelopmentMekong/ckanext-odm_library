import ckan
import pylons
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_library_helper
from urlparse import urlparse
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

DATASET_TYPE_NAME = 'library_record'

def last_library_record():
  '''Returns the last created library_record'''
  return odm_library_helper.last_library_record

def odc_fields():
  '''Return a list of odc fields'''

  log.debug('odc_fields')

  return odm_library_helper.odc_fields

def metadata_fields():
  '''Return a list of metadata fields'''

  log.debug('metadata_fields')

  return odm_library_helper.metadata_fields

def library_fields():
  '''Return a list of library fields'''

  log.debug('library_fields')

  return odm_library_helper.library_fields

def validate_not_empty(value,context):
  '''Returns if a string is empty or not'''

  log.debug('validate_not_empty: %s', value)

  if not value or len(value) is None:
    raise toolkit.Invalid('Missing value')
  return value

class OdmLibraryPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong library plugin.'''

  plugins.implements(plugins.IDatasetForm)
  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IFacets)
  plugins.implements(plugins.IPackageController, inherit=True)

  def dataset_facets(self, facets_dict, package_type):

    facets_dict = {
              'license_id': toolkit._('License'),
              'organization': toolkit._('Organizations'),
              'groups': toolkit._('Groups'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):

    group_facets = {
              'license_id': toolkit._('License'),
              'organization': toolkit._('Organizations'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return group_facets

  def organization_facets(self, facets_dict, organization_type, package_type):

    organization_facets = {
              'license_id': toolkit._('License'),
              'groups': toolkit._('Groups'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return organization_facets

  def before_map(self, m):

    m.connect('odm_library_index','/library',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='search')

    m.connect('odm_library_new','/library/new',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='new')

    m.connect('odm_library_new_resource','/library/new_resource/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='new_resource')

    m.connect('odm_library_read', '/library/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record', action='read')

    m.connect('odm_library_edit', '/library/edit/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record', action='edit')

    return m

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'odm_library')
    toolkit.add_public_directory(config, 'public')

  def get_helpers(self):
    '''Register the plugin's functions above as a template helper function.'''

    return {
      'odm_library_last_library_record': last_library_record,
      'odm_library_library_fields': library_fields,
      'odm_library_odc_fields': odc_fields,
      'odm_library_metadata_fields': metadata_fields
    }

  def _modify_package_schema_write(self, schema):

    for metadata_field in odm_library_helper.metadata_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if metadata_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({metadata_field[0]: validators_and_converters})

    for odc_field in odm_library_helper.odc_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if odc_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({odc_field[0]: validators_and_converters})

    for library_field in odm_library_helper.library_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if library_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({library_field[0]: validators_and_converters})

    for tag_dictionary in odm_library_helper.tag_dictionaries:
      schema.update({tag_dictionary[0]: [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_tags')(tag_dictionary[0])]})

    return schema

  def _modify_package_schema_read(self, schema):

    for metadata_field in odm_library_helper.metadata_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if metadata_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({metadata_field[0]: validators_and_converters})

    for odc_field in odm_library_helper.odc_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if odc_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({odc_field[0]: validators_and_converters})

    for library_field in odm_library_helper.library_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if library_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({library_field[0]: validators_and_converters})

    for tag_dictionary in odm_library_helper.tag_dictionaries:
      schema.update({tag_dictionary[0]: [toolkit.get_converter('convert_from_tags')(tag_dictionary[0]),toolkit.get_validator('ignore_missing')]})

    return schema

  def create_package_schema(self):
    schema = super(OdmLibraryPlugin, self).create_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def update_package_schema(self):
    schema = super(OdmLibraryPlugin, self).update_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def show_package_schema(self):
    schema = super(OdmLibraryPlugin, self).show_package_schema()
    schema = self._modify_package_schema_read(schema)
    return schema

  def is_fallback(self):
    return False

  def package_types(self):
    return ['library_record']

  def new_template(self):
    return 'library/new.html'

  def read_template(self):
    return 'library/read.html'

  def edit_template(self):
    return 'library/edit.html'

  def search_template(self):
    return 'library/search.html'

  def package_form(self):
    return 'library/new_package_form.html'

  def resource_form(self):
    return 'library/snippets/resource_form.html'

  def after_create(self, context, pkg_dict):

    log.debug('after_create: %s', pkg_dict)

    odm_library_helper.last_library_record = pkg_dict

  def after_update(self, context, pkg_dict):

    log.debug('after_update: %s', pkg_dict)
