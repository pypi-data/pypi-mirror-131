
def comprobacion(n):
    lista_primos=[]
    if n<2:
        print("El número introducido es menor de 2")
    else:
        for i in range(2,n+1):
            for x in range(2,i):
                if i % x == 0:
                    break
            else:
                lista_primos.append(i)        
    print(lista_primos)

            

      