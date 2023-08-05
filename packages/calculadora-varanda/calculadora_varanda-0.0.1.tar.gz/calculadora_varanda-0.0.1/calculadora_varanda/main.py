print('Bem vindo a uma calculadora!')

def recebe_numero(texto):
  numero = input(texto)
  try:
    numero = int(numero)
  except ValueError:
    try:
      numero = float(numero)
    except ValueError as e:
      print('O programa falhou, não conseguimos identificar um número digitado.')
      raise e
  return numero


def recebe_operacao():
  operacao = input(
    'Qual operação você deseja realizar? (+ | - | x | /) '
    )
  lista_operacoes_disponiveis = ['+', '-', 'x', '/']
  if operacao not in lista_operacoes_disponiveis:
    print(
      'Digite uma operação válida.'
      )
    raise ValueError(
      'Operação não disponível!'
      )
  else:
    return operacao


def somar(lista_de_numeros):
  resultado = 0
  for numero in lista_de_numeros:
    resultado = resultado + numero
  return resultado

def subtrair(lista_de_numeros):
  resultado = 0
  for numero in lista_de_numeros:
    resultado = resultado - numero
  return resultado

def multiplicar(lista_de_numeros):
  resultado = lista_de_numeros[0]
  for numero in lista_de_numeros[1:]:
    resultado = resultado * numero
  return resultado

def dividir(lista_de_numeros):
  resultado = lista_de_numeros[0]
  for numero in lista_de_numeros[1:]:
    resultado = resultado / numero
  return resultado

# Pergunta quantos números quer usar
quantos_numeros = recebe_numero(
  'Quantos números você quer usar? '
  )

# Criando a lista de números e colocando um número temporário desejado
lista_de_numeros = list()
lista_de_numeros = []
for i in range(quantos_numeros):
  numero_temporario = recebe_numero(
    'Digite o valor do número desejado: '
    )
  lista_de_numeros.append(numero_temporario)

# Recebendo operacao desejada
operacao = recebe_operacao()


# Realiza operação deseja com a lista de números informados
if operacao == '+':
  resultado = somar(lista_de_numeros)
elif operacao == '-':
  resultado = subtrair(lista_de_numeros)
elif operacao == 'x':
  resultado = multiplicar(lista_de_numeros)
elif operacao == '/':
  resultado = dividir(lista_de_numeros)

print(resultado)