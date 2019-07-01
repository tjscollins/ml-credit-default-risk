from io import BytesIO

import numpy as np
from matplotlib import pyplot as plt

from webapp.cdm import get_feature_importances, exp_variances, test_data, predictions

def most_important_features_chart():
    importances = list(reversed(get_feature_importances(50)))
    imp_names = [item[0] for item in importances]
    imp_vals = [item[1] for item in importances]
    mif_fig = plt.figure(figsize=(18,3))
    chart = mif_fig.add_subplot()
    chart.bar(imp_names, imp_vals, align='center')
    chart.tick_params('x', labelrotation=90)
    chart.set_yscale('log')
    chart.set_title('50 Most Important Features')
    chart.set_ylabel('Relative Importance')
    chart.set_position([0, 0, 0.5, 1])
    chart.set_xlabel('Application Field')
    chart.set_xmargin(0)
    chart.set_ymargin(0)
    img = BytesIO()
    plt.savefig(img,  bbox_inches='tight')
    img.seek(0)
    return img

def explained_variance_chart():
    fig_evc = plt.figure(figsize=(10,5))
    chart = fig_evc.add_subplot()
    chart.plot(range(1, len(exp_variances) + 1), np.cumsum(exp_variances), label='Total explained variance')
    chart.set_title('Cumulative Explained Variance of First 256 Features by PCA')
    chart.set_ylabel('Cumulative Explained Variance')
    chart.set_xlabel('Number of Features')
    fig_evc.tight_layout()
    img = BytesIO()
    fig_evc.savefig(img,  bbox_inches='tight')
    img.seek(0)
    return img

def top_correlations_chart():
    figure = plt.figure(num=3)
    ax_list = figure.subplots(5, 2)
    figure.suptitle('Correlations of 10 Most Importance Application Features', x=2, y=7.5, fontsize=28)
    top_ten_features = list(reversed(get_feature_importances(10)))
    for index in range(len(top_ten_features)):
        coords = [index // 2, index % 2]
        feature_name = top_ten_features[index][0]
        ax = ax_list[coords[0]][coords[1]]
        ax.scatter(test_data[feature_name], predictions)
        ax.set_title(feature_name)

        xmargin = 0.25
        ymargin = 0.25
        dx = 2
        dy = 1
        x0 = coords[1] * (dx + xmargin)
        y0 = (5 - coords[0]) * (dy + ymargin)
        x1 = dx
        y1 = dy
        ax.set_position([x0, y0, x1, y1])
        ax.set_aspect(0.5)
        ax.margins(x=0, y=0)
        ax.set_ylim(bottom=0)
    
    img = BytesIO()
    figure.savefig(img,  bbox_inches='tight')
    img.seek(0)
    return img



