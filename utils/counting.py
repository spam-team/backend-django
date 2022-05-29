import numpy as np
from sklearn.cluster import DBSCAN


class SegmentCounter:
    """ Класс-помощник для работы с кластерами.
    Уменьшаем входное изображение, чтобы ускорить время работы алгоритмов кластерого анализа.
    Гипотеза заключается в том, что моржи с большой высоты имеют одинаковую площадь в изображениях,
    поэтому производится поиск медианного размера кластера, а затем высчитывается количество моржей
    как отношение общей площади к медианной.
    Далее производится кластерное разбиение на найденное количество моржей.
    """
    DEFAULT_SIZE = (1090, 920)


def walruses_count_by_click(img: np.array, centroids: np.array, x: float, y: float):
    """ Расчет количества моржей рядом с определенной точкой """
    x = x * img.shape[1]
    y = y * img.shape[0]

    cluster_centers = np.array(list(centroids) + [[y, x]])

    dbscan = DBSCAN(eps=20)
    dbscan.fit(cluster_centers)

    point_label = dbscan.labels_[-1]

    if point_label == -1:
        return 0

    return dbscan.labels_[dbscan.labels_ == point_label].shape[0]
