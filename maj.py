import subprocess
import jr_data_science

update_pypi = ['python3','setup.py','sdist','bdist_wheel']
git_add     = ['git','add',  '.']
git_commit  = ['git','commit', '-m', "\'{version}\'".format(version=jr_data_science.__version__)]
git_push    = ['git', 'push', 'origin']
twine       = ['twine', 'upload', '--skip-existing', 'dist/*']
pip_upgrade = ['pip','install','--ignore-installed','--no-cache-dir','jr_data_science']
commands = [update_pypi, git_add, git_commit,  git_push, twine, pip_upgrade ]
for bash_command in commands :
    print ("== =="*10)
    print(" ".join(bash_command))
    print ("== ==" * 10)
    if bash_command == twine:
        print("user ?")
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("output = ")
    to_print ="\n".join(str(output).split("\\n"))
    print(to_print )
    if error:
        print("error = ")
        to_print = "\n".join(str(error ).split("\\n"))
        print(to_print)