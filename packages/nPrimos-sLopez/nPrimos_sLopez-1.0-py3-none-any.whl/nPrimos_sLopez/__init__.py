def primo(n):
	for i in range(2, n):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es primo")
primo(25)

def funcion_primos(n):
    for i in range (2, n):
        aux = 0
        for j in range(2,i):
            if (i%j==0):
                aux = 1
                break
        if(aux == 0):
            print(i, "Es un número primo")
funcion_primos(25)
