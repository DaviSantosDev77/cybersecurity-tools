atrasos = int(input('Quantas faltas voce tem? '))
if atrasos >= 3:
    print('voce está suspenso!')
elif atrasos == 2:
    print('mais uma falta estará suspenso!')
elif atrasos == 1:
    print('mais duas faltas e estará suspenso!')
else:
    print('pode entrar')