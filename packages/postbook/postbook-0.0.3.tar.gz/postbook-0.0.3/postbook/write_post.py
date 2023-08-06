from __future__ import print_function, absolute_import
import nbformat
import json
from nbconvert import HTMLExporter
import os
from traitlets import HasTraits, Unicode, List, Dict, Bool, default, observe, validate
from inspect import currentframe, getframeinfo
from nbconvert import templateexporter,exporter
import os
import uuid
import json
import warnings
from pathlib import Path

from jupyter_core.paths import jupyter_path
from traitlets import HasTraits, Unicode, List, Dict, Bool, default, observe, validate
from traitlets.config import Config
from traitlets.utils.importstring import import_item
from jupyter_core.paths import jupyter_path
from jinja2 import (
    TemplateNotFound, Environment, ChoiceLoader, FileSystemLoader, BaseLoader,
    DictLoader
)
class CustomExporter(HTMLExporter):
    @default('template_paths')
    def _template_paths(self, prune=True, root_dirs=None):
        paths = []
        root_dirs = self.get_prefix_root_dirs()
        template_names = self.get_template_names()
       
        for template_name in template_names:
            for base_dir in self.extra_template_basedirs:
                path = os.path.join(base_dir, template_name)
                if not prune or os.path.exists(path):
                    paths.append(path)
            for root_dir in root_dirs:
                base_dir = os.path.join(root_dir, 'nbconvert', 'templates')
                path = os.path.join(base_dir, template_name)
                if not prune or os.path.exists(path):
                    paths.append(path)

        for root_dir in root_dirs:
            # we include root_dir for when we want to be very explicit, e.g.
            # {% extends 'nbconvert/templates/classic/base.html' %}
            paths.append(root_dir)
            # we include base_dir for when we want to be explicit, but less than root_dir, e.g.
            # {% extends 'classic/base.html' %}
            base_dir = os.path.join(root_dir, 'nbconvert', 'templates')
            paths.append(base_dir)

            compatibility_dir = os.path.join(root_dir, 'nbconvert', 'templates', 'compatibility')
            paths.append(compatibility_dir)

        additional_paths = []
        for path in self.template_data_paths:
            if not prune or os.path.exists(path):
                additional_paths.append(path)

        
        
        return paths + self.extra_template_paths + additional_paths

    def get_template_names(self):
        # finds a list of template names where each successive template name is the base template
        template_names = []
        root_dirs = self.get_prefix_root_dirs()
        
        base_template = self.template_name
       
        merged_conf = {}  # the configuration once all conf files are merged
        while base_template is not None:
            template_names.append(base_template)
            # print(template_names,template_names)
            conf = {}
            found_at_least_one = False
           
            for base_dir in self.extra_template_basedirs+['/home/aswin/plog_project/postbook/templates/']:
                # base_dir ='/home/aswin/plog_project/postbook/templates/'
                
                template_dir = os.path.join(base_dir, base_template)
                
                if os.path.exists(template_dir):
                    found_at_least_one = True
                conf_file = os.path.join(template_dir, 'conf.json')
                if os.path.exists(conf_file):
                    with open(conf_file) as f:
                        conf = templateexporter.recursive_update(json.load(f), conf)
            for root_dir in root_dirs:
                template_dir = os.path.join(root_dir, 'nbconvert', 'templates', base_template)
                if os.path.exists(template_dir):
                    found_at_least_one = True
                conf_file = os.path.join(template_dir, 'conf.json')
                if os.path.exists(conf_file):
                    with open(conf_file) as f:
                        conf = templateexporter.recursive_update(json.load(f), conf)
            if not found_at_least_one:
                # Check for backwards compatibility template names
                for root_dir in root_dirs:
                    compatibility_file = base_template + '.tpl'
                    compatibility_path = os.path.join(root_dir, 'nbconvert', 'templates', 'compatibility', compatibility_file)
                    if os.path.exists(compatibility_path):
                        found_at_least_one = True
                        warnings.warn(
                            f"5.x template name passed '{self.template_name}'. Use 'lab' or 'classic' for new template usage.",
                            DeprecationWarning)
                        self.template_file = compatibility_file
                        conf = self.get_compatibility_base_template_conf(base_template)
                        self.template_name = conf.get('base_template')
                        break
                if not found_at_least_one:
                    paths = "\n\t".join(root_dirs)

                    raise ValueError('No template sub-directory with name %r found in the following paths:\n\t%s' % (base_template, paths))
            merged_conf = templateexporter.recursive_update(dict(conf), merged_conf)
            base_template = conf.get('base_template')
        conf = merged_conf
        mimetypes = [mimetype for mimetype, enabled in conf.get('mimetypes', {}).items() if enabled]
        if self.output_mimetype and self.output_mimetype not in mimetypes and mimetypes:
            supported_mimetypes = '\n\t'.join(mimetypes)
            raise ValueError('Unsupported mimetype %r for template %r, mimetypes supported are: \n\t%s' %\
                (self.output_mimetype, self.template_name, supported_mimetypes))
        return template_names + ['aswins']

    def from_notebook_node(self, nb, resources={'blog_name':'naari'}, **kw):
        # langinfo = nb.metadata.get('language_info', {})
        # lexer = langinfo.get('pygments_lexer', langinfo.get('name', None))
        # print("myreeeeeeeeee")
        # highlight_code = self.filters.get('highlight_code', Highlight2HTML(pygments_lexer=lexer, parent=self))

        # filter_data_type = WidgetsDataTypeFilter(notebook_metadata=self._nb_metadata, parent=self, resources=resources)

        # self.register_filter('highlight_code', highlight_code)
        # self.register_filter('filter_data_type', filter_data_type)
        return super().from_notebook_node(nb, resources,**kw)  
def write_post(ipynb_file_path):
    f = open(ipynb_file_path)
    html_exporter = CustomExporter(template_name='aswins')
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'posts')
    
    jake_notebook = nbformat.reads(json.dumps(json.loads(f.read())), as_version=4)
    (body, resources) = html_exporter.from_notebook_node(jake_notebook)
    
 
  
   
    
    with open('test.html','w') as f:
        f.write(body)
    

write_html('Lab_0.ipynb')