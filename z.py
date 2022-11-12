import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")
iris = sns.load_dataset("iris")
print(type(iris))

# Set up the figure
f, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")

# Draw a contour plot to represent each bivariate density
# sns.kdeplot(
#     data=iris,
#     x="sepal_width",
#     # y="sepal_length",
#     hue="species",
#     thresh=.1,
# )
sns.histplot(
    d,
    x="price", hue="cut",
    multiple="stack",
    palette="light:m_r",
    edgecolor=".3",
    linewidth=.5,
    log_scale=True,
)
plt.show()