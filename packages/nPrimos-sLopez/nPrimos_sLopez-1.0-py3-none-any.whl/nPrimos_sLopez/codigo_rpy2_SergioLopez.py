import rpy2.robjects as ro
from rpy2.robjects import r
codigo_r = """
fPrimos_r <- function(n){
    for (i in 2:(n-1)){
        aux_r <-0
        for (j in 2:(i-1)){
            if(i%%j == 0){
                aux_r <- 1
                break}
                }
    if (aux_r == 0){
      (cat(i, "es un número primo\n"))}
      }
      }
"""
ro.r(codigo_r)
primos_py = ro.globalenv['fPrimos_r']
primos_py(50)