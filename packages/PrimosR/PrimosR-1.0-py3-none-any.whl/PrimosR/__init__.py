import rpy2.robjects as ro

primos_r = """
primos <- function(x){
  i = 2
  while (i<=x){
    creciente = 2
    Primo = TRUE
    while(Primo && creciente<i)
    {
      if(i%%creciente==0){
        Primo=FALSE
      }
      else
      {
        creciente=creciente+1
      }
    }
    if(Primo==TRUE){
      print(i)
    }
    i=i+1
  }
  }
"""
ro.r(primos_r)

primos_py = ro.globalenv['primos']


