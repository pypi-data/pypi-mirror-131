#!/usr/bin/env python
# coding: utf-8

# ```{try_on_binder}
# ```

# In[1]:


from IPython import get_ipython

ip = get_ipython()
if ip is not None:
    # ip.run_line_magic('load_ext', 'pymor.discretizers.builtin.gui.jupyter')
    ip.run_line_magic("matplotlib", "inline")

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch")


# # Tutorial:
# 
# Some text.

# In[2]:


from dune.xt import *
from dune.gdt import *
import dune.gdt
dune.gdt.__version__

