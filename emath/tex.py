import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = "#ffeecc"

def render_latex_to_png(expression, filename):
    """
    renders a LaTeX formatted string into an image, and saves it at the
    desired file location
    """
    fig, ax = plt.subplots(figsize=(6,3))
    ax.text(0.5, 0.5, expression, fontsize='50', ha='center', va='center')
    ax.axis('off')

    plt.savefig(
        filename,
        dpi=150,
        bbox_inches='tight',
        transparent=True
    )
    plt.close()
