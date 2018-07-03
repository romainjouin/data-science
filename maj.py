import subprocess
import jr_data_science

update_pypi = ['python3','setup.py','sdist','bdist_wheel']
git_add     = ['git','add',  '.']
git_commit  = ['git','commit', '-m', "\'{version}\'".format(version=jr_data_science.__version__)]
git_push    = ['git', 'push', 'origin']
twine       = ['twine', 'upload', '--skip-existing', 'dist/*']

for bash_command in [update_pypi, git_add, git_commit, git_push, twine]:
    print(" ".join(bash_command))
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("output = %s"%output)
    print("error = %s" %error )