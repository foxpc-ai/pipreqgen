import ast
from importlib.metadata import version, PackageNotFoundError
import argparse
import json

def extract_imports(filename):
    try:
        with open(filename, 'r') as file:
            tree = ast.parse(file.read())
    
        imports = [name.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for name in node.names]

        imports = list(dict.fromkeys(imports))
        return imports
    except FileNotFoundError:
        print(f'Unable to locate {filename} file')
        raise
    except Exception as e:
        print(f'Unexpected exception occured. Exception type:- {e}')
        raise

def extract_imports_from_ipynb(filename):
    try:
        with open(filename, 'r') as file:
            notebook = json.load(file)
            imports = []
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    code = ''.join(cell['source'])
                    tree = ast.parse(code)
                    imports.extend([name.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for name in node.names])
            imports = list(dict.fromkeys(imports))
        return imports
    except FileNotFoundError:
        print(f'Unable to locate {filename} file')
        raise
    except Exception as e:
        print(f'Unexpected exception occured. Exception type:- {e}')
        raise

    

def get_versions(modules, append):
    versions = {}
    for module in modules:
        try:
            versions[module] = version(module)
        except PackageNotFoundError:
            versions[module] = f"{module} not found"
    mode = 'a' if append else 'w'
    with open('requirements.txt', mode) as f:
        for k in versions:
            f.write(k+"=="+versions[k]+'\n')
    return versions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',type=str,help='filepath of the file for which requirements.txt needs to be generated for')
    parser.add_argument('--append', action='store_true', help='append to requirements.txt if flag is set, otherwise create a new file')
    args = parser.parse_args()

    if args.filename.endswith('.ipynb'):
        module = extract_imports_from_ipynb(args.filename)
    else:
        module = extract_imports(args.filename)

    #module = list(dict.fromkeys(module))
    get_versions(module,args.append)

if __name__ == '__main__':
    main()
