
import nbformat
import json
from nbconvert import HTMLExporter
import os



def write_html(ipynb_file_path,name):
    f = open(ipynb_file_path)
    html_exporter = HTMLExporter()
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'posts')
    html_exporter.template_name = 'classic'
    jake_notebook = nbformat.reads(json.dumps(json.loads(f.read())), as_version=4)
    (body, resources) = html_exporter.from_notebook_node(jake_notebook)
    html_file_location = os.path.join(final_directory, r'{}'.format(name.replace(' ','_')+'.html'))
    with open(html_file_location,'w') as f:
        f.write(body)
    return html_file_location