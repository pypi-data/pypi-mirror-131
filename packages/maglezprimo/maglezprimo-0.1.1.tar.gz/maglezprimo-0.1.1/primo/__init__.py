"""
Auth: Miguel A. Gonzalez Ruiz
App: Calculo de numeros primos usando R
"""

from rpy2.robjects import r

r('''
n <- 100
for (i in 1:n){
    if(i%%2==0)
        print(i)
}
''')