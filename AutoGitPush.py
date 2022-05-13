# This method uses the Github's python API to push the file to the repo.
import base64
import requests
import json
import datetime
from credentials import GITHUB_TOKEN


def push_file(fileName, repo_url, branch, user, token):
    '''
    Push file update to GitHub repo

    // param fileName: the name of the file on the local branch
    // param repo_url: the github repo slug, i.e. "https://api.github.com/repos/{owner}/{repo}"
    // param branch: the name of the branch to push the file to
    // param user: github username
    // param token: github user token
    // return None
    // raises Exception: if file with the specified name cannot be found in the repo
    '''

    message = f"Automated commit/push created for the file {fileName} at {str(datetime.date.today())}"
    url = "https://api.github.com/repos/%s/branches/%s" % (repo_url, branch)

    # get the response of the repo_url/branch
    r = requests.get(url, auth=(user, token))
    if not r.ok:
        print("Error when retrieving branch info from %s" % url)
        print("Reason: %s [%d]" % (r.text, r.status_code))
    rjson = r.json()
    treeurl = rjson['commit']['commit']['tree']['url']
    # get the response of the file insidde the repo_url/branch/tree
    r2 = requests.get(treeurl, auth=(user, token))
    if not r2.ok:
        print("Error when retrieving commit tree from %s" % treeurl)
        print("Reason: %s [%d]" % (r2.text, r2.status_code))
    r2json = r2.json()

    # Set sha as None by default to avoid error if file is not found
    sha = None
    for file in r2json['tree']:
        # If file is found in the repo, set the sha to the file's sha
        if file['path'] == fileName:
            sha = file['sha']

    with open(fileName, 'rb') as data:
        byte_content = data.read()
        content = base64.b64encode(byte_content).decode("ascii")

    # Gather all data to commit and push
    inputdata = {}
    inputdata["branch"] = branch
    inputdata["message"] = message
    inputdata["content"] = content
    if sha:
        inputdata["sha"] = str(sha)
    else:
        print("The files: %s, are not found in repos tree %s \nLet's commit the new file and push it.. \n" %
              (fileName, repo_url))

    # Access the url content of the repo where the file is to be committed and pushed
    updateURL = f"https://api.github.com/repos/{repo_url}/contents/{fileName}"

    #  Finally, commit and push the file
    try:
        rPut = requests.put(updateURL, auth=(user, token),
                            data=json.dumps(inputdata))
        print("Push successful!\n")
        if not rPut.ok:
            print("Error when pushing to %s" % updateURL)
            print("Reason: %s [%d]" % (rPut.text, rPut.status_code))

    except requests.exceptions.RequestException as e:
        print('Something went wrong! I will print all the information that is available so you can figure out what happend!')
        print(rPut)
        print(rPut.headers)
        print(rPut.text)
        print(e)


if __name__ == '__main__':
    fileName = "Files.txt"
    repositoryName = "hassanFDtech/AutoGitPush"
    branch = "main"
    username = "hassanFDtech"
    token = GITHUB_TOKEN  # from credentials.py

    push_file(fileName, repositoryName, branch, username, token)
