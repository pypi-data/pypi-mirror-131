import typer
import os
import pickle
app = typer.Typer()
from postbook.get_list_of_files import get_files
from postbook.write_html import write_html
from postbook.send_files import send_files
from postbook.update_index import update_index
from postbook.setting_the_host import host_setup

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")

@app.command()
def start(name: str):
    current_directory = os.getcwd()
    
    


    final_directory = os.path.join(current_directory, r'{}'.format(name))
    final_directory_with_posts = os.path.join(final_directory, r'posts')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        os.makedirs(final_directory_with_posts)
    
    email = typer.prompt("What's your email ?")
    ip_address = typer.prompt("Whats'your host ip ?")
    username = typer.prompt("What's your host username ?")
    password = typer.prompt("What's your host password ?")
    domain_flag = typer.prompt("Do you have a domain name ? (y/n)")

    domain = None
    if(domain_flag=='y' or domain_flag=='Y'):
        domain = typer.prompt("What's your domain address ? ")
    with open(f"{final_directory}/.plog","wb") as f:
        pickle.dump({'name':name,'email':email,'ip_address':ip_address,'username':username,'password':password,'domain':domain},f)

    
@app.command()
def getfiles():
    current_directory = os.getcwd()
    html_files = [x for x in get_files(current_directory+'/posts/') if '.html' in x ]
    return html_files

@app.command()
def writehtml(path_to_file:str):
    post_title = 'My first blog'
    write_html(path_to_file,post_title)
    current_directory = os.getcwd()
    with open(f"{current_directory}/.plog","rb") as f:
        meta_data = pickle.load(f)
    
    final_directory = os.path.join(current_directory, r'{}'.format(meta_data['name']))
    #send_files(path_to_file,)

@app.command()
def refresh():
    list_of_files = getfiles()
    
    print(list_of_files)


@app.command()
def publish(path_to_file:str, post_title:str):
    html_file_location = write_html(path_to_file,post_title)
    print(html_file_location)
    send_files(html_file_location,'/root/blog/{}.html'.format(post_title.replace(' ','_')))
    
    update_index()
    send_files('index.html','/root/blog/index.html')
@app.command()
def setup():
    current_directory = os.getcwd()
    with open(f"{current_directory}/.plog","rb") as f:
        meta_data = pickle.load(f)
    host_setup(meta_data['ip_address'],meta_data['username'],meta_data['password'])
    

def main():
    app()
    
    

