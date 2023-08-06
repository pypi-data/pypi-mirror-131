import os

module_dir = os.path.dirname(__file__)


def main():
    static_folder = module_dir + os.path.join(module_dir, '../frontend/build')
    instance_path = os.getcwd()

    print(f'Starting the notebook static_folder={static_folder}, instance_path={instance_path}')
