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
    CATEGORIES = ["blogs","portfolios","leatherworking"]

    output = "---\n"
    output += "layout: post\n"

    title = input("Title: ")
    output += f"title: {title}\n"

    datestr = current_date_time()
    output += f"date: {datestr}\n"

    while True:
        category = input(f"Category ({'/'.join(CATEGORIES)}): ")
        if category.lower() in CATEGORIES:
            output += f"category: {category.lower()}\n"
            break
        else:
            print("Please enter the category name in parentheses.")
    
    while True:
        tags = input("Tags (comma separated, end with '$' to re-enter): ")
        tags = tags.replace(", ", ",") # remove all spaces
        if tags.endswith('$'):
            continue
        elif not tags: # if no tags are entered:
            break
        else:
            tags_split = tags.split(',')
            output += f"tags: {repr(tags_split)}\n"
            break

    output += "---"
    
    today = date.today()
    d = today.strftime("%Y-%m-%d")
    t = '-'.join(title.lower().split(' '))
    md_filename = f"{d}-{t}.md"
    
    cwd = os.getcwd().split('/')[-1]

    print()
    
    if cwd != 'website':
        print("Failed to create the markdown file. Please run the program in the root directory.")
        print("Your YAML title has been generated and copied to your clipboard. Or you can copy it here:")
        pyperclip.copy(output)
        print(output)
    else: 
        with open(os.path.join(os.getcwd(), category, "_posts", md_filename), 'w') as f:
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