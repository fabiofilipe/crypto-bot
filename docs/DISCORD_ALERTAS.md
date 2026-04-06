# Sistema de Alertas no Discord

Este documento explica como configurar e usar o sistema de alertas do Discord para receber notificações sobre variações de preço de criptomoedas.

## Configuração Inicial

### 1. Criar um Webhook no Discord

1. Abra o Discord e acesse as configurações do seu servidor
2. Vá em **Integrações** > **Webhooks**
3. Clique em **Novo Webhook**
4. Configure:
   - Nome: Por exemplo, "Alertas Financeiros"
   - Canal: Escolha o canal onde deseja receber os alertas
5. Copie a URL do webhook

### 2. Configurar a URL do Webhook

Edite o arquivo `.env` na raiz do projeto e adicione a URL do webhook:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_ID/SEU_TOKEN
```

### 3. Testar a Conexão

Execute o script de teste para verificar se tudo está funcionando:

```bash
.venv/bin/python3 testar_discord.py
```

Você deve receber 6 mensagens de teste no seu canal do Discord.

## Como Funciona

O sistema envia automaticamente alertas para o Discord quando:

1. **Variação Percentual**: O preço de um ativo varia mais que um limite definido
   - Alertas de ALTA (📈) em verde
   - Alertas de BAIXA (📉) em vermelho

2. **Limites de Preço**: O preço ultrapassa limites mínimos ou máximos definidos
   - Abaixo do mínimo (⚠️) em vermelho
   - Acima do máximo (⚠️) em laranja

## Uso Programático

### Exemplo Básico

```python
from src.alertas import SistemaAlertas

# Criar instância do sistema de alertas
# Discord está habilitado por padrão
alertas = SistemaAlertas()

# Verificar variações em todos os ativos (limite de 3%)
alertas_gerados = alertas.verificar_todos_ativos(limite_percentual=3.0)

# Verificar se Bitcoin está dentro dos limites
alertas.verificar_limite_preco('BTC', preco_minimo=50000, preco_maximo=70000)
```

### Desabilitar Discord

Se quiser usar apenas alertas no terminal/log, sem Discord:

```python
alertas = SistemaAlertas(discord_habilitado=False)
```

### Enviar Mensagem Customizada

Você também pode enviar mensagens customizadas diretamente:

```python
from src.utils.discord_notifier import DiscordNotifier

notifier = DiscordNotifier()

# Mensagem simples
notifier.enviar_mensagem_simples("Sistema iniciado com sucesso!")

# Mensagem urgente (menciona @everyone)
notifier.enviar_mensagem_simples("Atenção: Grande variação detectada!", urgente=True)
```

## Formato das Notificações

As notificações no Discord incluem:

- **Título**: Tipo de alerta e ativo
- **Campos**: Informações detalhadas (variação, preços, limites)
- **Timestamp**: Hora da notificação
- **Cores**: Visual para identificar rapidamente o tipo de alerta
- **Emojis**: Facilitam a identificação visual

## Integração com Pipeline

O sistema de alertas funciona automaticamente com o pipeline de coleta:

```python
from src.pipeline import Pipeline

# O pipeline verifica alertas após cada coleta
pipeline = Pipeline()
pipeline.executar_ciclo()  # Coleta dados e verifica alertas automaticamente
```

## Troubleshooting

### Webhook não configurado

Se você ver a mensagem "Discord notifier não configurado", verifique:
- O arquivo `.env` existe na raiz do projeto
- A variável `DISCORD_WEBHOOK_URL` está configurada
- A URL do webhook está correta

### Erro ao enviar mensagem

Se as mensagens não chegam no Discord:
- Verifique se o webhook ainda existe no Discord
- Teste a conexão com `testar_discord.py`
- Verifique os logs em `logs/alertas.log`

### Mensagens duplicadas

Se receber mensagens duplicadas:
- Certifique-se de não estar executando múltiplas instâncias do sistema
- Verifique o scheduler para evitar sobreposição de execuções

## Customização

Você pode customizar o comportamento dos alertas editando os arquivos:

- `src/alertas.py`: Lógica de detecção de alertas
- `src/utils/discord_notifier.py`: Formatação e envio das mensagens

## Segurança

- O arquivo `.env` está no `.gitignore` e não será commitado
- Nunca compartilhe sua URL de webhook publicamente
- Se a URL for exposta, delete o webhook no Discord e crie um novo
