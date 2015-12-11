#!/usr/bin/env python
# -*- coding: utf-8 -*-

document_types = [
  ('advocacy_and_promotional_materials','Advocacy and promotional materials'),
  ('analysis_discussion_papers_and_blogs','Analysis, discussion papers, and blogs'),
  ('books_and_book_chapters','Books and book chapters'),
  ('case_studies','Case studies'),
  ('issue_and_policy_briefs','Issue and policy briefs'),
  ('profiles_people','Profiles - People'),
  ('profiles_organizations_and_projects','Profiles - Organizations  and projects'),
  ('profiles_geographical_areas_and_sites','Profiles - Geographical areas and sites'),
  ('conference_workshops_proceedings_and_presentations','Conference/workshop proceedings and presentations'),
  ('reports_journal_articles_and_research_papers','Reports, journal articles, and research papers (including theses and dissertations)')
]

library_fields = [
  ('document_type','Document type',False),
  ('marc21_020','ISBN',False),
  ('marc21_022','ISSN',False),
  ('marc21_100','Author',False),
  ('marc21_110','Corporate Author',False),
  ('marc21_245','Title',False),
  ('marc21_246','Varying Form of Title',False),
  ('marc21_250','Edition',False),
  ('marc21_260a','Publication Place',False),
  ('marc21_260b','Publication Name',False),
  ('marc21_260c','Publication Date',False),
  ('marc21_300','Pagination',False),
  ('marc21_500','General Note',False),
  ('marc21_700','Co-Author',False),
  ('marc21_710','Co-Author (Corporate)',False)
]

odc_fields = [
  ('file_name_kh','File (Khmer)',False),
  ('file_name_en','File (English)',False),
  ('adopted_date','Adopted Date',False),
  ('number_en','Number (English)',False),
  ('number_kh','Number (Khmer)',False),
  ('published_date','Publication date',False),
  ('published_under','Published under',False)
]

metadata_fields = [
  ('odm_copyright','Copyright',False),
  ('odm_access_and_use_constraints','Access and Use Constraints',False),
  ('odm_contact','Contact',False),
  ('odm_language','Language',True),
  ('odm_date_uploaded','Date Uploaded',True),
  ('odm_spatial_range','Geographic area (Spatial Range)',True)
]

ckan_fields= [
  ('version','Version',True)
]

taxonomy_dictionary = 'taxonomy'

session = {}
