from dparse import parse, filetypes

content = """
-e common/lib/calc
South==1.0.1 --hash==abcdefghijklmno
pycrypto>=2.6
git+https://github.com/pmitros/pyfs.git@96e1922348bfe6d99201b9512a9ed946c87b7e0b
distribute>=0.6.28, <0.7
# bogus comment
-e .
pdfminer==20140328
-r production/requirements.txt
--requirement test.txt
"""

df = parse(content, filetype=filetypes.requirements_txt)

print(df.dependencies[0])
print(df.json())

print("---")

content = """
name: my_env
dependencies:
  - gevent=1.2.1
  - pip:
    - beautifulsoup4==1.2.3
    - requests>=2.3
"""
df = parse(content, path="conda.yml")

print(df.dependencies[0])
print(df.json())

print("---")

content = """
[testenv:bandit]
commands =
    bandit --ini setup.cfg -ii -l --recursive project_directory
deps =
    bandit==1.4.0
[testenv:manifest]
commands =
    check-manifest --verbose
"""
df = parse(content, path="tox.ini")

print(df.dependencies[0])
print(df.json())
