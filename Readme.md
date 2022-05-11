# AutoGitPush
This project is for creating or updating a file on GitHub repository.


## Install all the required libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Get a GitHub Token steps
1. Go to Settings.
2. Click **Developer settings** > **Personal access tokens** > **Generate new token**
3. Give your token a descriptive name.
4. Under **scopes**, select all.
5. Click **Generate token**.
6. Copy it before you leave the page!

## Use of the token

Open the credentials.py and replace the generated token with the string in the quotes.

Note. credentials.py should be included in .gitignore

## Run the backup.py file to create the model

```
python AutoGitPush.py
```