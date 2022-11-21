import numpy as np # linear algebra
import faiss

class Reranking1_Shoppe():
  def __init__(self,):
      pass

  def l2norm_numpy(self,x):
      return x / np.linalg.norm(x, ord=2, axis=1, keepdims=True)

  def neighborhood_search(self,emb,thresh,k_neighbors):
      index = faiss.IndexFlatIP(emb.shape[1])
      faiss.normalize_L2(emb)
      index.add(emb)
      sim, I = index.search(emb, k_neighbors)
      pred_index=[]
      pred_sim=[]
      for i in range(emb.shape[0]):
          cut_index=0
          for j in sim[i]:
              if(j>thresh):
                  cut_index+=1
              else:
                  break                        
          pred_index.append(I[i][:(cut_index)])
          pred_sim.append(sim[i][:(cut_index)])
          
      return pred_index,pred_sim
    
  def blend_neighborhood(self,emb, match_index_lst, similarities_lst):
      new_emb = emb.copy()
      for i in range(emb.shape[0]):
          cur_emb = emb[match_index_lst[i]]
          weights = np.expand_dims(similarities_lst[i], 1)
          new_emb[i] = (cur_emb * weights).sum(axis=0)
      new_emb = self.l2norm_numpy(new_emb)
    
      return new_emb

  def iterative_neighborhood_blending(self,emb, threshes,k_neighbors):
      for thresh in threshes:
          match_index_lst, similarities_lst = self.neighborhood_search(emb, thresh,k_neighbors)
          emb = self.blend_neighborhood(emb, match_index_lst, similarities_lst)
      return emb, match_index_lst

