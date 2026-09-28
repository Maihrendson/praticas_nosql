import redis
import threading
import time

# Script para gerar o arquivo .txt exigido para entrega
comandos_txt = """-- 1. Strings (Manipulação Básica de Chaves)
-- Exercício 01: Crie uma chave sistema:nome com o valor "DataPlatform" e recupere o valor salvo.
SET sistema:nome "DataPlatform"
GET sistema:nome

-- Exercício 02: Grave três variáveis de ambiente no mesmo comando: env:db=postgres, env:cache=redis e env:queue=rabbitmq. Em seguida, busque apenas env:db e env:cache.
MSET env:db "postgres" env:cache "redis" env:queue "rabbitmq"
MGET env:db env:cache

-- Exercício 03: Defina um token de sessão sessao:usuario:101 com o valor "xyz123" que expire automaticamente em 30 segundos. Em seguida, verifique quanto tempo resta antes da expiração.
SETEX sessao:usuario:101 30 "xyz123"
TTL sessao:usuario:101

-- Exercício 04: Crie um contador de acessos para a página principal pageviews:home. Incremente-o em 1 unidade, depois em mais 5 unidades, e por fim decremente 2 unidades.
INCR pageviews:home
INCRBY pageviews:home 5
DECRBY pageviews:home 2

-- 2. Hashes (Objetos e Dicionários)
-- Exercício 05: Crie um perfil de usuário usuario:201 contendo os campos nome ("Carlos"), email ("carlos@email.com") e nivel ("admin").
HSET usuario:201 nome "Carlos" email "carlos@email.com" nivel "admin"

-- Exercício 06: Recupere apenas o campo email do usuario:201. Em seguida, recupere todos os campos e valores armazenados para esse usuário.
HGET usuario:201 email
HGETALL usuario:201

-- Exercício 07: No mesmo usuario:201, incremente um novo campo tentativas_login em 1. Em seguida, liste apenas os nomes de todas as chaves (campos) presentes nesse hash.
HINCRBY usuario:201 tentativas_login 1
HKEYS usuario:201

-- 3. Lists (Filas e Pilhas)
-- Exercício 08: Crie uma fila de tarefas fila:email. Adicione no final da fila os itens "email_1", "email_2" e "email_3".
RPUSH fila:email "email_1" "email_2" "email_3"

-- Exercício 09: Remova e retorne o primeiro elemento da fila fila:email (simulando um consumidor FIFO).
LPOP fila:email

-- Exercício 10: Liste todos os elementos restantes na fila fila:email sem removê-los.
LRANGE fila:email 0 -1

-- 4. Sets (Conjuntos Não Ordenados e Sem Duplicatas)
-- Exercício 11: Crie um conjunto tags:post:1 e adicione as tags "dados", "redis", "nosql" e novamente "redis". Verifique quantos elementos existem no conjunto.
SADD tags:post:1 "dados" "redis" "nosql" "redis"
SCARD tags:post:1

-- Exercício 12: Crie um segundo conjunto tags:post:2 com as tags "redis", "python" e "backend". Execute o comando para encontrar as tags que aparecem em ambos os posts (interseção).
SADD tags:post:2 "redis" "python" "backend"
SINTER tags:post:1 tags:post:2

-- Exercício 13: Verifique se a tag "python" pertence ao conjunto tags:post:1.
SISMEMBER tags:post:1 "python"

-- 5. Sorted Sets (Conjuntos Ordenados por Score)
-- Exercício 14: Crie um leaderboard de jogo placar:game inserindo: "alice" (score 1500), "bob" (score 2200) e "carol" (score 1800).
ZADD placar:game 1500 "alice" 2200 "bob" 1800 "carol"

-- Exercício 15: Liste o ranking completo do placar:game em ordem decrescente (do maior score para o menor), incluindo os valores dos scores na exibição.
ZREVRANGE placar:game 0 -1 WITHSCORES

-- Exercício 16: Aumente a pontuação de "alice" em 800 pontos e verifique a sua nova posição no ranking.
ZINCRBY placar:game 800 "alice"
ZREVRANK placar:game "alice"

-- 6. Pub/Sub, Transações e Administração
-- Exercício 17 (Pub/Sub): No terminal 1, inscreva-se no canal notificacoes. No terminal 2, publique a mensagem "Novo relatório disponível".
-- (No Terminal 1)
SUBSCRIBE notificacoes
-- (No Terminal 2)
PUBLISH notificacoes "Novo relatorio disponivel"

-- Exercício 18 (Transações): Inicie um bloco de transação para transferir R$ 50 da conta:A para a conta:B atomicamente.
MULTI
DECRBY conta:A 50
INCRBY conta:B 50
EXEC

-- Exercício 19 (Gerenciamento de Chaves): Verifique se a chave sistema:nome existe no banco. Se existir, altere o nome da chave para sistema:app e depois remova-a.
EXISTS sistema:nome
RENAME sistema:nome sistema:app
DEL sistema:app

-- Exercício 20 (Inspeção do Servidor): Execute um comando para visualizar informações gerais e estatísticas de memória do servidor Redis. Em seguida, limpe apenas os dados do banco de dados atual.
INFO memory
FLUSHDB
"""

# Gerando o arquivo de entrega
with open("lista01_redis_comandos.txt", "w", encoding="utf-8") as f:
    f.write(comandos_txt)
print("Arquivo 'lista01_redis_comandos.txt' gerado com sucesso para entrega!")


# =========================================================
# EXECUÇÃO PRÁTICA NO CONTAINER REDIS UTILIZANDO PYTHON
# =========================================================

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("\n--- 1. STRINGS ---")
r.set("sistema:nome", "DataPlatform")
print(f"Ex 01 - GET sistema:nome -> {r.get('sistema:nome')}")

r.mset({"env:db": "postgres", "env:cache": "redis", "env:queue": "rabbitmq"})
print(f"Ex 02 - MGET -> {r.mget(['env:db', 'env:cache'])}")

r.setex("sessao:usuario:101", 30, "xyz123")
print(f"Ex 03 - TTL sessao:usuario:101 -> {r.ttl('sessao:usuario:101')} segundos restantes")

r.incr("pageviews:home")
r.incrby("pageviews:home", 5)
r.decrby("pageviews:home", 2)
print(f"Ex 04 - Contador pageviews:home -> {r.get('pageviews:home')}")


print("\n--- 2. HASHES ---")
r.hset("usuario:201", mapping={"nome": "Carlos", "email": "carlos@email.com", "nivel": "admin"})
print(f"Ex 06 - GET email -> {r.hget('usuario:201', 'email')}")
print(f"Ex 06 - HGETALL -> {r.hgetall('usuario:201')}")

r.hincrby("usuario:201", "tentativas_login", 1)
print(f"Ex 07 - HKEYS -> {r.hkeys('usuario:201')}")


print("\n--- 3. LISTS ---")
r.delete("fila:email") # Limpando caso rode o script 2x
r.rpush("fila:email", "email_1", "email_2", "email_3")
print(f"Ex 09 - LPOP -> Removido: {r.lpop('fila:email')}")
print(f"Ex 10 - LRANGE -> Restantes: {r.lrange('fila:email', 0, -1)}")


print("\n--- 4. SETS ---")
r.delete("tags:post:1", "tags:post:2")
r.sadd("tags:post:1", "dados", "redis", "nosql", "redis")
print(f"Ex 11 - SCARD tags:post:1 -> {r.scard('tags:post:1')} elementos")

r.sadd("tags:post:2", "redis", "python", "backend")
print(f"Ex 12 - Interseção SINTER -> {r.sinter('tags:post:1', 'tags:post:2')}")
print(f"Ex 13 - 'python' pertence a tags:post:1? -> {r.sismember('tags:post:1', 'python')}")


print("\n--- 5. SORTED SETS ---")
r.delete("placar:game")
r.zadd("placar:game", {"alice": 1500, "bob": 2200, "carol": 1800})
print(f"Ex 15 - Ranking Completo -> {r.zrevrange('placar:game', 0, -1, withscores=True)}")

r.zincrby("placar:game", 800, "alice")
print(f"Ex 16 - Nova posição da Alice (ZREVRANK) -> {r.zrevrank('placar:game', 'alice')}")


print("\n--- 6. PUB/SUB, TRANSAÇÕES E ADMINISTRAÇÃO ---")
# Ex 17: Pub/Sub usando Thread para simular 2 terminais no Python
def listener():
    pubsub = r.pubsub()
    pubsub.subscribe('notificacoes')
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Ex 17 - Terminal 1 (Recebido): {message['data']}")
            break

thread = threading.Thread(target=listener)
thread.start()
time.sleep(1) # Aguarda o listener iniciar
r.publish('notificacoes', 'Novo relatorio disponivel')
thread.join()

# Ex 18: Transação (Pipeline)
r.set("conta:A", 100)
r.set("conta:B", 100)
pipe = r.pipeline()
pipe.decrby("conta:A", 50)
pipe.incrby("conta:B", 50)
pipe.execute()
print(f"Ex 18 - Transação finalizada. Saldo Conta B: {r.get('conta:B')}")

# Ex 19 e 20: Administração
if r.exists("sistema:nome"):
    r.rename("sistema:nome", "sistema:app")
    r.delete("sistema:app")
    print("Ex 19 - Chave renomeada e deletada com sucesso.")

memoria = r.info('memory')
print(f"Ex 20 - Uso de memória atual (human readable): {memoria.get('used_memory_human')}")
r.flushdb()
print("Ex 20 - Banco limpo com FLUSHDB.")