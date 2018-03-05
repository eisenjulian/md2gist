#!/usr/bin/env python
# encoding: utf-8

"""
app.py

Install dependencies:
> pip install requests
> pip install gdata

> python app.py username:token url_to_md_file prefix
"""

import requests
import sys
import re

# curl -H "Content-Type: application/json" -d '{"description": "Your XPATHr Gist test","public": true,"files": {"test.xml": {"content": "Paste your XML code.."},"test.xsl": {"content": "Paste your XSL code here.."}}}' 'https://api.github.com/gists'

def upload_gists(auth, mdfile_url, prefix):
    token = tuple(auth.split(':'))
    mdfile = requests.get(mdfile_url).text
    gists = requests.get('https://api.github.com/gists', auth=token).json()
    all_gists = {
        list(gist['files'].keys())[0]: gist['id'] for gist in gists
    }
    regex = re.compile(r"^```([a-z_. ]*)\n([\s\S]*?)\n```", 
                       re.MULTILINE | re.IGNORECASE)
    code_blocks = [(match.group(1).strip(), match.group(2).strip())
        for match in re.finditer(regex, mdfile) 
        if 'mermaid' not in match.group(1)
        and len(match.group(2).strip().split('\n')) > 1]

    unused = {file for file in all_gists.keys() if file.startswith(prefix)}
    counter = 0
    print('These are the {} created gists urls:'.format(len(code_blocks)))
    for header, content in code_blocks:
        lang = header
        if not lang:
            lang = 'text'
        filename = prefix + str(counter)
        if ' ' in header:
            lang = header.split(' ')[0]
            filename = prefix + header.split(' ')[1]
        print(filename)
        payload = {
            'public': True,
            'description': '',
            'files': {
                filename: {
                    'type': 'text/plain',
                    'filename': filename,
                    'language': lang.capitalize(),
                    'content': content
                }
            }
        }
        if filename in all_gists:
            unused -= {filename}
            print('\thttps://gist.github.com/' + all_gists[filename])
            gist_url = 'https://api.github.com/gists/' + all_gists[filename]
            old_content = list(requests.get(gist_url, auth=token).json()['files'].values())[0]['content']
            if old_content == content:
                continue
            url = requests.patch('https://api.github.com/gists/' + all_gists[filename], 
                           json=payload, 
                           auth=token).json()['id']
        else:
            url = requests.post('https://api.github.com/gists', 
                                json=payload, 
                                auth=token).json()['id']
            print('\thttps://gist.github.com/' + url)
        counter += 1



    if len(unused):
        print("\nThere where unused gists with that prefix, consider deleting them:")
        for gist in unused:
            print(all_gists[gists][1])

def main():
    if len(sys.argv) != 4:
        raise ValueError('Invalid argument count. Usage is: python app.py username:token url_to_md_file prefix')
    upload_gists(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()