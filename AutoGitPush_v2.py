# this method uses PyGithub to push to github
import base64
from github import Github
from github import InputGitTreeElement
from credentials import GITHUB_TOKEN

token = GITHUB_TOKEN
g = Github(token)
repoName = "AutoGitPush"
branch = "new_branch"

repo = g.get_user().get_repo(repoName)
file_list = ['Files.txt']
commit_message = 'Automated Git Push'

master_ref = repo.get_git_ref(branch)
master_sha = master_ref.object.sha
base_tree = repo.get_git_tree(master_sha)

element_list = list()
for entry in file_list:
    with open(entry, 'rb') as input_file:
        data = input_file.read()
    if entry.endswith('.txt'):
        data = base64.b64encode(data)
    element = InputGitTreeElement(entry, '100644', 'blob', data)
    element_list.append(element)

tree = repo.create_git_tree(element_list, base_tree)
parent = repo.get_git_commit(master_sha)
commit = repo.create_git_commit(commit_message, tree, [parent])
master_ref.edit(commit.sha)

""" An egregious hack to change the txt contents after the commit """
for entry in file_list:
    with open(entry, 'rb') as input_file:
        data = input_file.read()
    if entry.endswith('.png'):
        old_file = repo.get_contents(entry)
        commit = repo.update_file(
            '/' + entry, 'Update PNG content', data, old_file.sha)
