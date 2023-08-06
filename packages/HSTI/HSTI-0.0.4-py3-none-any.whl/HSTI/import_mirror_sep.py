import numpy as np
def form_mirror_sep_axis(path, number_of_bands):
    t = np.arange(0,number_of_bands,1)
    p = np.poly1d(np.load(path))
    mirror_sep = p(t)
    return mirror_sep*1e-6
