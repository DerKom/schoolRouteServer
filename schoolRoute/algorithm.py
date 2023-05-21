import psycopg2
import psycopg2.extras
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from k_means_constrained import KMeansConstrained
import math
import itertools
import time
import sys

def get_data_from_database():
    try:
        print("Connecting to the database...")
        conn = psycopg2.connect(
            database="schoolroute",
            user="gerente",
            password="Gerente123498765",
            host="138.68.155.159",
            port="5432"
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print("Fetching data...")
        cur.execute("SELECT id, latitud, longitud FROM centros")
        X = cur.fetchall()
        cur.close()
        conn.close()
        print("Fetched data successfully!")
        return X
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

def distance(point1, point2):
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

def tsp(points, group_number, total_groups):
    print(f"\nStarting TSP algorithm for group {group_number} of {total_groups}...")
    min_distance = float('inf')
    total_permutations = math.factorial(len(points))
    count = 0
    start = time.time()
    for path in itertools.permutations(points):
        count += 1
        if count % 1000 == 0:
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20 * count / total_permutations), int(100 * count / total_permutations)))
            sys.stdout.flush()

        distance_travelled = sum(distance(path[i], path[i + 1]) for i in range(len(path) - 1))
        if distance_travelled < min_distance:
            min_distance = distance_travelled
            best_path = path

    print(f"\nFinished TSP algorithm for group {group_number} of {total_groups} after {time.time() - start} seconds.")
    return best_path

def kmeans_with_constrained(X, size):
    print("Starting K-means clustering with constraints...")
    start = time.time()
    num_clusters = len(X) // size
    kmeans = KMeansConstrained(n_clusters=num_clusters, size_min=size, size_max=size)
    kmeans.fit(X)
    labels = kmeans.labels_
    print(f"Finished K-means clustering with constraints after {time.time() - start} seconds.")
    return labels

X = get_data_from_database()

if X is None:
    print("No data was fetched.")
else:
    num_clusters = len(X) // 10
    remainder = len(X) % 10
    normal_groups_labels = kmeans_with_constrained(np.array(X)[:-remainder, 1:], 10) if num_clusters > 0 else np.array([])
    remainder_group = X[-remainder:] if remainder > 0 else []

    normal_groups = []
    for i in range(max(normal_groups_labels) + 1 if len(normal_groups_labels) > 0 else 0):
        indexes = np.where(normal_groups_labels == i)[0]
        result = []
        for j in indexes:
            result.append(X[j])
        normal_groups += [result]

    colors = [
        '#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
        '#800000', '#008000', '#000080', '#808000', '#800080', '#008080', '#808080',
        '#C00000', '#00C000', '#0000C0', '#C0C000', '#C000C0', '#00C0C0', '#C0C0C0',
        '#400000', '#004000', '#000040', '#404000', '#400040', '#004040', '#404040',
        '#200000', '#002000', '#000020', '#202000', '#200020', '#002020', '#202020',
        '#600000', '#006000', '#000060', '#606000', '#600060', '#006060', '#606060',
        '#A00000', '#00A000', '#0000A0', '#A0A000', '#A000A0', '#00A0A0', '#A0A0A0',
        '#E00000', '#00E000', '#0000E0', '#E0E000', '#E000E0', '#00E0E0', '#E0E0E0',
        '#100000', '#001000', '#000010', '#101000', '#100010', '#001010', '#101010',
        '#700000', '#007000', '#000070', '#707000', '#700070', '#007070', '#707070',
        '#900000', '#009000', '#000090', '#909000', '#900090', '#009090', '#909090',
        '#B00000', '#00B000', '#0000B0', '#B0B000', '#B000B0', '#00B0B0', '#B0B0B0',
    ]

    for i in range(len(np.array(X)[:, 1:])):
        plt.scatter(np.array(X)[:, 1:][i][0], np.array(X)[:, 1:][i][1], c=colors[normal_groups_labels[i] if i < len(normal_groups_labels) else -1])

    plt.show()

    paths = []
    total_groups = len(normal_groups) + (1 if remainder_group else 0)
    for group_number, group in enumerate(normal_groups, 1):
        path = tsp(group, group_number, total_groups)
        paths.append(path)

    if remainder_group:
        path = tsp(remainder_group, len(paths) + 1, total_groups)
        paths.append(path)

    for path in paths:
        x = []
        y = []
        for point in path:
            x.append(point[1])
            y.append(point[2])

        plt.plot(x, y)

    plt.show()