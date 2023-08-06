from jinja2 import Template, Environment, FileSystemLoader
from postbook.get_list_of_files import get_files
import os
import pickle
import paramiko
class HtmlChapter:
    def __init__(self, title: str):
        self.title = title.split('.')[0]
        self.path = self.get_chapter_path()

    def get_chapter_path(self):
        current_directory = os.getcwd()
        with open(f"{current_directory}/.plog","rb") as f:
            meta_data = pickle.load(f)
        if(meta_data['domain']):
            path = f"http://{meta_data['domain']}/" + self.title+'.html'
        else:
            path = f"http://{meta_data['ip_address']}/" + self.title+'.html'
        return path

    def __str__(self):
        return self.path
def update_index():
    current_directory = os.getcwd()
    file_path_list = os.path.realpath(__file__).split('/')[:-1]
    file_path = '/'.join(file_path_list)
    template_location  = file_path+'/templates/'
    print(template_location)
    posts = [HtmlChapter(x) for x in get_files(current_directory+'/posts/')] 
    print(posts)
    # load templates folder to environment (security measure)
    env = Environment(loader=FileSystemLoader(template_location))
    print(env)
    with open(f"{current_directory}/.plog","rb") as f:
        meta_data = pickle.load(f)
    print(meta_data)
    # load the `index.jinja` template
    print("read the pickle file")
    index_template = env.get_template('index.jinja')
    output_from_parsed_template = index_template.render(posts=posts, blog_name=meta_data['name'])
    
        
    # write the parsed template
    with open("index.html", "w") as chap_page:
        chap_page.write(output_from_parsed_template)