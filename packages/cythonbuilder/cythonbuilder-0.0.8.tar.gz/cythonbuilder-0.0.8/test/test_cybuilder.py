import os.path
import shutil
import unittest

import cythonbuilder
import cythonbuilder as cybuilder
from dataclasses import dataclass

def do():
    cybuilder.init()
    cybuilder.build(targetfilenames=["gigya"], debugmode=False)

    from ext import gigya

    gigya.vld_gigya_types('test')




@dataclass
class AppConfig:
    appname:str = "CythonBuilder"
    appcmd:str = os.path.splitext(os.path.basename(__file__))[0]

@dataclass
class LoggingConfig:
    logginName:str = 'cybuilderlogger'

@dataclass
class DirectoryConfig:
    dirname_extensions:str = "ext"
    dirname_pyxfiles:str = "pyxfiles"
    dirname_annotations:str = "annotations"

    path_root_dir:str = os.path.realpath(os.curdir)
    path_extensions_dir:str = os.path.join(path_root_dir, dirname_extensions)
    path_pyx_dir:str = os.path.join(path_extensions_dir, dirname_pyxfiles)
    path_annotations_dir:str = os.path.join(path_extensions_dir, dirname_annotations)
    path_setuppy_build_dir:str = os.path.join(path_root_dir, 'build')


class TestCyBuilder(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCyBuilder, self).__init__(*args, **kwargs)

    def test_init(self):
        # Arrange; remove ext folder
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass

        # Act - init to create all required folders
        cythonbuilder.init()

        # Assert - All folders created?
        ext_folder = os.path.isdir(DirectoryConfig.path_extensions_dir)
        pyx_folder = os.path.isdir(DirectoryConfig.path_pyx_dir)
        anno_folder = os.path.isdir(DirectoryConfig.path_annotations_dir)
        self.assertTrue(ext_folder)
        self.assertTrue(pyx_folder)
        self.assertTrue(anno_folder)

    def test_build_numpy_not_required(self):
        # Arrange - write a file that we are going to try to build
        cython_function = """cpdef double add_two_number(double a, double b): return a + b 
        """
        file_name = 'test_no_np'
        file_path = os.path.join(DirectoryConfig.path_pyx_dir, f'{file_name}.pyx')
        with open(file_path, 'w') as f:
            f.write(cython_function)
        print(os.path.isfile(file_path))

        # Act - build the file
        cythonbuilder.build(numpy_required=False, debugmode=False)
        cythonbuilder.clean()

        # Assert - Have we built the file?
        print(DirectoryConfig.path_extensions_dir)
        print(os.listdir(DirectoryConfig.path_extensions_dir))
        pyd_path = os.path.join(DirectoryConfig.path_extensions_dir, f"{file_name}.pyd")
        print(f"{pyd_path=}")
        pyd_file_created = os.path.isfile(pyd_path)
        self.assertTrue(pyd_file_created)



if __name__ == '__main__':
    unittest.main()
