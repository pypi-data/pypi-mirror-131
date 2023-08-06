import os
from shutil import copyfile
from pathlib import Path



path = os.path.join('..', os.path.join('bootstrap', os.path.join('templates', 'bootstrap')))
path = os.path.abspath(path)
print(Path(path))
# dest = os.path.join('..', os.path.join('dist', 'del_templates'))
# dest = os.path.abspath(dest)
# print(Path(dest))

for i in os.walk(path):
    for j in i[2]:
        count = 1
        #print(f"""[{j.split('.')[0].upper()}, '{j}'],""")


        print(f"""{j.split('.')[0].upper()} = [""")
        with open(Path(os.path.abspath(os.path.join(path, j))), 'r') as f:
            for a, z in enumerate(f.readlines()):
                fill = z.replace('\n', '')
                if a == len(f.readlines()) - 1:
                    print(f"""\t['''{fill}''', False]""")
                else:
                    print(f"""\t['''{fill}''', False],""")
                count += 1
        print(']\n\n')


        # copyfile(Path(os.path.abspath(os.path.join(path, j))), dest)


        # if '_' in j:
        #     name = ' '.join([k.capitalize() for k in j.split('.')[0].split('_')])
        # else:
        #     name = j.split('.')[0].capitalize()
        #
        #
        # url = f"""{'{{'} url_for('templates', filename='{j}') {'}}'}"""
        # tag = f"""<p><a href="{url}"><b>{name}</b></a></p>"""
        #
        # add = f"\t{count}: ['''{tag}''', False],"""
        #
        # print(add)


        count += 1