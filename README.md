# md2gist

> A Python script to create a gist for each code block in a markdown file to be embedded in a Medium post

If you ever had to migrate an `.md` file to a Medium post you know very well that code blocks are not going to be rendered very nicely, and the only way to fix it is to create a gist for each and every one of them.

This short script will download your markdown file from the web and create gists for each code block. You can specity the filename after the language declaration in the beginning of the code block like the following snippet.

    ```mylanguage file.ml
    Some beatiful code you want to show off
    ```

### Requirements
Just the `requests` package which can be installed from `pip`.

### To run it
Get a [personal access token](https://github.com/settings/tokens) with `gist` scope to use inside the script and decide a prefix to add to all of your gists.

Then just do
```bash
> python app.py github_user_name:personal_token url_to_md_file prefix
```
