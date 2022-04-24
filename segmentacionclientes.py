# -*- coding: utf-8 -*-
"""SegmentacionClientes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rZXMHlQZNGpLkTnx5iwtUNmyhEoIQqs9
"""

pip install dabl

#Para las operaciones matematicas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')
# Para el analisis de Datos
import dabl

# Importar nuestros datos
data = pd.read_csv('/content/Mall_Customers.csv')

"""##Examinar los datos"""

# Checar el shape
print("Shape de los Datos :", data.shape)

# Checar los head
data.head ()

# Checar el tail
data.tail()

# Checar un ejemplo del Dataset
data.sample(3)

# Realizar un pairplot para el Dataset
sns.pairplot(data)
plt.show()

# Examinar la corelacion del Heat Map del Data
sns. heatmap(data.corr(), annot = True, cmap = 'copper')
plt.title('Correlation Heatmap of the Data', fontsize = 15)
plt.show()

# Analizar el data con respecto al Spending Score
dabl.plot(data, target_col = 'Spending Score (1-100)')

# Analizar el data con respecto al Annual Income
dabl.plot(data, target_col = 'Annual Income (k$)')

# Describir el data
data.describe()

# Describir el categorical data
data.describe(include = 'object')

# Checar si hay algun NULL data
data.isnull().any().any()

"""##Visualizar los Datos"""

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (18, 8)

plt.subplot (1, 2, 1)
sns.set(style = 'whitegrid')
sns.distplot(data['Annual Income (k$)'])
plt.title('Distribution of Annual Income', fontsize = 20)
plt.xlabel('Range of Annual Income')
plt.ylabel( 'Count' )

plt.subplot(1, 2, 2)
sns.set(style = 'whitegrid')
sns.distplot(data['Age'], color = 'red')
plt.title('Distribution of Age', fontsize = 20)
plt.xlabel('Range of Age')
plt.ylabel('Count')
plt.show()

labels = ['Female', 'Male']
size = data[ 'Gender'].value_counts()
colors = ['lightgreen', 'orange']
explode = [0, 0.001]

plt.rcParams['figure.figsize'] = (9, 9)
plt.pie(size, colors = colors, explode = explode, labels = labels, shadow = True, startangle = 90, autopct = '%.2f%%')
plt.title('Gender Gap', fontsize = 20)
plt.axis('off')
plt.legend()
plt.show()

plt.rcParams['figure.figsize'] = (15, 8)
sns.countplot(data['Age'], palette = 'hsv')
plt.title('Distribution of Age', fontsize = 20)
plt.show()

# Checar la distribuvion del Annual Income
plt.rcParams['figure.figsize'] = (20, 8)
sns.distplot(data['Annual Income (k$)'], color = 'red')
plt.title('Distribution of Annual Income', fontsize = 20)
plt.show()

# Checar la distribucion del Spending Score
plt.rcParams['figure.figsize']= (20, 8)
sns.distplot(data['Spending Score (1-100)'], color = 'black')
plt.title('Distribution of Spending Score', fontsize = 20)
plt.show()

# Gender vs Spendscore
plt.rcParams['figure.figsize'] = (18, 7)
sns.boxenplot(data[ 'Gender' ], data['Spending Score (1-100)'], palette = 'Blues')
plt.title('Gender vs Spending Score', fontsize = 20)
plt.show()

# Gender vs Annual Income
plt.rcParams['figure.figsize'] = (18, 7)
sns.violinplot (data['Gender'], data[ 'Annual Income (k$)'], palette = 'rainbow')
plt.title('Gender vs Annual Income', fontsize = 20)
plt.show()

# Gender vs Age
plt.rcParams['figure.figsize'] = (18, 7)
sns.stripplot(data[ 'Gender'], data['Age'], palette = 'Purples', size = 10)
plt.title('Gender vs Age', fontsize = 20)
plt.show()

# Annual Income vs Age and Spending Score
x = data['Annual Income (k$)']
y = data['Age']
z = data['Spending Score (1-100)']
sns.lineplot(x, y, color = 'blue')
sns.lineplot(x, z, color = 'pink')
plt.title('Annual Income vs Age and Spending Score', fontsize = 20)
plt.show()

"""##Analisis Cluster"""

# Spending score, yAnnual Income
# Importarla libreria warnings para evitarlos
import warnings
warnings. filterwarnings('ignore')

#Seleccionar las colmunas Spending score, y Annual Income de Data
x = data.loc[:, ['Spending Score (1-100)', 'Annual Income (k$)']].values

# Checar el  shape de x
print(x.shape)

# Checar el data, que vamos a usar para el analisis de clustering
x_data = pd.DataFrame(x)
x_data.head()
# Donde o->Spending Score, y 1->Annual Income

"""##Algoritmo Kmeans"""

from sklearn.cluster import KMeans

wcss = []
for i in range(1, 11):
  km = KMeans (n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
  km.fit(x)
  wcss.append (km.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method', fontsize = 20)
plt.xlabel('No. of Clusters')
plt.ylabel('wcss')
plt.show()

"""##Vizualizar los Clusters"""

# Lets visualize these clusters
plt.style.use('fivethirtyeight')

km = KMeans (n_clusters = 5, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_means = km.fit_predict(x)

plt.scatter(x[y_means == 0, 0], x[y_means == 0, 1], s = 100, c = 'pink', label = 'miser')
plt.scatter(x[y_means == 1, 0], x[y_means == 1, 1], s = 100, c = 'yellow', label = 'general')
plt.scatter(x[y_means == 2, 0], x[y_means == 2, 1], s = 100, c = 'cyan', label = 'target')
plt.scatter(x[y_means == 3, 0], x[y_means == 3, 1], s = 100, c = 'magenta', label = 'spendthrift')
plt.scatter(x[y_means == 4, 0], x[y_means == 4, 1], s = 100, c = 'orange', label = 'careful')
plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:, 1], s = 50, c = 'blue', label = 'centeroid')

plt.style.use('fivethirtyeight')
plt.title('K Means clustering between Annual Income and Spending Score', fontsize = 20)
plt.xlabel('Annual Incone')
plt.ylabel('Spending Score')
plt.legend()
plt.grid()
plt.show()

from sklearn.cluster import KMeans

wcss = []
for i in range(1, 11):
  kmeans = KMeans (n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
  kmeans.fit(x)
  wcss.append(kmeans.inertia_)

plt.rcParams['figure.figsize'] = (15, 5)
plt.plot(range(1, 11), wcss)
plt.title('K-Means Clustering (The Elbow Method)', fontsize = 20)
plt.xlabel('Age')
plt.ylabel('Count')
plt.grid()
plt.show()

kmeans = KMeans (n_clusters = 4, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
ymeans = kmeans.fit_predict(x)

plt.rcParams['figure.figsize'] = (10, 10)
plt.title('Cluster of Ages', fontsize = 30)




plt.scatter(x[ymeans == 0, 0], x[ymeans == 0, 1], s = 100, c = 'pink', label = 'Usual Customers')
plt.scatter(x[ymeans == 1, 0], x[ymeans == 1, 1], s = 100, c = 'orange', label = 'Priority Customers')
plt.scatter(x[ymeans == 2, 0], x[ymeans == 2, 1], s = 100, c = 'lightgreen', label = 'Target Customers (Young)')
plt.scatter(x[ymeans == 3, 0], x[ymeans == 3, 1], s = 100, c = 'red', label = 'Target Customers (0ld)')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black')

plt.style.use('fivethirtyeight')
plt.xlabel('Age')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.grid()
plt.show()