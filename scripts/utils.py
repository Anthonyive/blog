import datetime
from datetime import date
import time
from email import utils
import pyperclip
import os
import argparse

def current_date_time():
    """Generate current date and time for posts"""
    nowdt = datetime.datetime.now()
    output = utils.format_datetime(nowdt)
    pyperclip.copy(output)
    print(output)
    return output

def new_post_helper():
    """A helper function for generating YAML title for posts"""

    output = "---\n"
    output += "layout: post\n"

    title = input("Title: ")
    output += f"title: {title}\n"

    datestr = current_date_time()
    output += f"date: {datestr}\n"

    author = input("Author(s) [default: Yuchen Zhang, sep: comma]: ")
    if not author:
       output += f"author: Yuchen Zhang\n"
    elif ',' in author:
        authors = author.split(',')
        authors = [a.strip() for a in authors]
        output += 'author: \n'
        for a in authors:
            output += f'  - {a}\n'
    else:
        output += f"author: {author}\n"

    category = input(f"Category [only one category]: ")
    if category:
        output += f"categories: {category}\n"

    tag = input("Tag(s) [default: None, sep: comma]: ")
    if not tag:
       pass
    elif ',' in tag:
        tags = tag.split(',')
        tags = [t.strip() for t in tags]
        output += 'tags: \n'
        for t in tags:
            output += f'  - {t}\n'
    else:
        output += f"tags: {tag}\n"

    output += "---"
    
    today = date.today()
    d = today.strftime("%Y-%m-%d")
    t = '-'.join(title.lower().split(' '))
    md_filename = f"{d}-{t}.md"
    
    cwd = os.getcwd().split('/')[-1]

    print()
    
    if cwd != 'blog':
        print("Failed to create the markdown file. Please run the program in the root directory.")
        print("Your YAML title has been generated and copied to your clipboard. Or you can copy it here:")
        pyperclip.copy(output)
        print(output)
    else: 
        with open(os.path.join(os.getcwd(), "_posts", md_filename), 'w') as f:
            f.write(output)
        print("\N{party popper} Hooray! Your markdown file with YAML title is properly created.")

if __name__=="__main__":

    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {'current': current_date_time,
                    'helper': new_post_helper }
    
    parser.add_argument('command', choices=FUNCTION_MAP.keys())

    args = parser.parse_args()

    func = FUNCTION_MAP[args.command]
    func()