import numpy as np

class KMedoidsWeighted():

    def __init__(self, n_clusters=3):

        self.n_clusters = n_clusters

    def dist_function(self, m, o):
        '''
        Calcula distancia euclidiana utilizando como peso a população da cidade que não é meoide
        '''
        return np.sqrt((m[0]-o[0])**2+(m[1]-o[1])**2)*o[2]

    def _generate_dist_matrix(self, X):
        m = len(X)
        self.dist_matrix = np.zeros(shape=(m,m))
        for i in range(m):
            for j in range(m):
                self.dist_matrix[i][j] = self.dist_function(X[i], X[j])
    
    def _compute_loss(self, X, medoids_idxs):
        '''
        Calucla a função perda para essa configuração de meoides
        '''
        loss = 0
        m = len(X)
        for i in range(m):
            min_medoid_dist = np.inf
            for j in medoids_idxs:
                min_medoid_dist = min(min_medoid_dist, self.dist_matrix[j][i])
            
            loss+=min_medoid_dist

        return loss

    def _get_clusters(self, X, medoids_idxs):
        '''
        Retorna os clusters para essa configuração de meoides
        '''
        m = len(X)
        clusters = [[] for _ in range(len(medoids_idxs))]
        for i in range(m):
            min_medoid_dist = np.inf
            cluster = -1
            for idx, j in enumerate(medoids_idxs):
                if self.dist_matrix[j][i]<min_medoid_dist:
                    min_medoid_dist = self.dist_matrix[j][i]
                    cluster = idx
                    
            clusters[cluster].append(i)
                
        return clusters
    
    def fit(self, X, max_itr=1000, verbose=0):
        '''
        Minimiza a função perda achando a melhor configuração de meoides.
        
        X é uma lista de lista da forma (latitude, longitude, população)
        '''
        m = len(X)  
        self._generate_dist_matrix(X)
        medoids_idxs = set(np.random.choice(np.arange(len(X)), self.n_clusters, replace=False))
        loss = self._compute_loss(X, medoids_idxs)
        for itr in range(max_itr):
            if verbose:
                print("Iteration: {} ... loss: {}".format(itr, loss))
            swaps = False
            for i in range(m):
                for j in medoids_idxs:

                    if i in medoids_idxs:
                        continue
                    
                    medoids_idxs.remove(j)
                    medoids_idxs.add(i)
                    
                    if self._compute_loss(X, medoids_idxs)<loss:
                        swaps = True
                        loss = self._compute_loss(X, medoids_idxs)
                    
                    else:
                        medoids_idxs.remove(i)
                        medoids_idxs.add(j)
                        
            if not swaps:
                break
                
        return list(medoids_idxs), self._get_clusters(X, medoids_idxs)