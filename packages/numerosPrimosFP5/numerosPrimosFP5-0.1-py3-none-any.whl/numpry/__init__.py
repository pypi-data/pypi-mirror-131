def primos(n):
    
   checker = False
   for i in range(2,n):
       if n % i == 0:
            checker = True
        
   if checker == False:
        return "Primo"
   else:
        return "No Primo"
        

def calcula_primos(n):
    u = n+1
    lista = []
    
    for i in range(2,u):

        res = primos(i)
        
        if res == "Primo":
            lista.append(i)
    
    return lista

