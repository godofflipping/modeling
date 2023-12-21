import numpy as np
import matplotlib as mpl

def fadeColor(color1 = '#00FF00', color2 = '#0000FF', mix = 0):
        mix = min(max(0, mix), 1)
        color1 = np.array(mpl.colors.to_rgb(color1))
        color2 = np.array(mpl.colors.to_rgb(color2))
        return mpl.colors.to_hex((1 - mix) * color1 + mix * color2)