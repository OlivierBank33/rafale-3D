import os; os.environ['VF'] = 'vf16'
from nv_render import *
if __name__ == '__main__':
    import runpy, sys; runpy.run_module('nv_render', run_name='__main__')
