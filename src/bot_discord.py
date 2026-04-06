"""
Bot Discord que escuta comandos e envia alertas
Execute: python src/bot_discord.py
"""

import discord
from discord.ext import commands
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import datetime

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from utils.logger import configurar_logger

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logger
logger = configurar_logger('bot_discord')

# Configurar intents do bot
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler conteúdo das mensagens

# Criar bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Inicializar database
db = DatabaseManager()


@bot.event
async def on_ready():
    """Executado quando o bot está pronto"""
    logger.info(f'Bot conectado como {bot.user}')
    print(f'✅ Bot Discord conectado como {bot.user}')
    print(f'📊 Pronto para receber comandos!')
    print(f'💡 Digite "alerta" em qualquer canal para receber o status')
    print(f'💡 Ou use comandos: !preco, !status, !btc, !eth')


@bot.event
async def on_message(message):
    """Detecta mensagens no canal"""
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return

    # Detectar palavra "alerta" (case insensitive)
    if 'alerta' in message.content.lower():
        logger.info(f'Comando "alerta" detectado de {message.author}')
        await enviar_status_todos_ativos(message.channel)
        return

    # Processar comandos normais (começados com !)
    await bot.process_commands(message)


@bot.command(name='preco', aliases=['preço', 'p'])
async def comando_preco(ctx, ativo: str = None):
    """Mostra o preço de um ativo
    Uso: !preco BTC ou !preco ETH
    """
    if not ativo:
        await ctx.send("❌ Especifique um ativo! Ex: `!preco BTC`")
        return

    ativo = ativo.upper()

    try:
        ultimo = db.obter_ultimo_preco(ativo)

        if ultimo:
            embed = discord.Embed(
                title=f"💰 Preço Atual - {ativo}",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            embed.add_field(
                name="Preço",
                value=f"${ultimo['preco']:,.2f} {ultimo['moeda']}",
                inline=False
            )

            embed.add_field(
                name="Última Coleta",
                value=ultimo['horario_coleta'],
                inline=False
            )

            embed.set_footer(text="Sistema de Coleta Financeira")

            await ctx.send(embed=embed)
            logger.info(f'Preço de {ativo} enviado para {ctx.author}')
        else:
            await ctx.send(f"❌ Nenhum dado encontrado para {ativo}")

    except Exception as e:
        logger.error(f'Erro ao buscar preço: {e}')
        await ctx.send(f"❌ Erro ao buscar preço: {e}")


@bot.command(name='status', aliases=['s'])
async def comando_status(ctx, ativo: str = None):
    """Mostra status detalhado de um ativo
    Uso: !status BTC ou !status ETH
    """
    if not ativo:
        # Se não especificar ativo, mostra todos
        await enviar_status_todos_ativos(ctx.channel)
        return

    ativo = ativo.upper()

    try:
        ultimo = db.obter_ultimo_preco(ativo)
        stats = db.obter_estatisticas(ativo, dias=7)

        if ultimo and stats:
            variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

            # Determinar cor baseado na variação
            if variacao > 5:
                cor = discord.Color.green()
            elif variacao < -5:
                cor = discord.Color.red()
            else:
                cor = discord.Color.blue()

            embed = discord.Embed(
                title=f"📊 Status Completo - {ativo}",
                color=cor,
                timestamp=datetime.now()
            )

            # Preço atual
            embed.add_field(
                name="💰 Preço Atual",
                value=f"${ultimo['preco']:,.2f} {ultimo['moeda']}",
                inline=True
            )

            # Última coleta
            embed.add_field(
                name="🕐 Última Coleta",
                value=ultimo['horario_coleta'].split()[1][:5],
                inline=True
            )

            # Espaço vazio para quebrar linha
            embed.add_field(name="\u200b", value="\u200b", inline=False)

            # Estatísticas 7 dias
            embed.add_field(
                name="📉 Mínimo (7d)",
                value=f"${stats['preco_minimo']:,.2f}",
                inline=True
            )

            embed.add_field(
                name="📊 Médio (7d)",
                value=f"${stats['preco_medio']:,.2f}",
                inline=True
            )

            embed.add_field(
                name="📈 Máximo (7d)",
                value=f"${stats['preco_maximo']:,.2f}",
                inline=True
            )

            # Variação e registros
            embed.add_field(
                name="📊 Variação (7d)",
                value=f"{variacao:+.2f}%",
                inline=True
            )

            embed.add_field(
                name="📋 Registros",
                value=f"{stats['total_registros']:,}",
                inline=True
            )

            embed.set_footer(text="Sistema de Coleta Financeira")

            await ctx.send(embed=embed)
            logger.info(f'Status de {ativo} enviado para {ctx.author}')
        else:
            await ctx.send(f"❌ Nenhum dado encontrado para {ativo}")

    except Exception as e:
        logger.error(f'Erro ao buscar status: {e}')
        await ctx.send(f"❌ Erro ao buscar status: {e}")


@bot.command(name='btc')
async def comando_btc(ctx):
    """Atalho para status do Bitcoin"""
    await comando_status(ctx, 'BTC')


@bot.command(name='eth')
async def comando_eth(ctx):
    """Atalho para status do Ethereum"""
    await comando_status(ctx, 'ETH')


@bot.command(name='todos', aliases=['all', 'tudo'])
async def comando_todos(ctx):
    """Mostra status de todos os ativos"""
    await enviar_status_todos_ativos(ctx.channel)


@bot.command(name='ajuda', aliases=['help', 'comandos'])
async def comando_ajuda(ctx):
    """Mostra lista de comandos disponíveis"""
    embed = discord.Embed(
        title="📋 Comandos Disponíveis",
        description="Lista de comandos do bot de alertas financeiros",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="💬 Mensagem Automática",
        value="`alerta` - Digite 'alerta' em qualquer mensagem para receber status de todos os ativos",
        inline=False
    )

    embed.add_field(
        name="💰 Comandos de Preço",
        value=(
            "`!preco BTC` - Preço atual de um ativo\n"
            "`!status BTC` - Status completo de um ativo\n"
            "`!todos` - Status de todos os ativos"
        ),
        inline=False
    )

    embed.add_field(
        name="🚀 Atalhos Rápidos",
        value=(
            "`!btc` - Status do Bitcoin\n"
            "`!eth` - Status do Ethereum"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Outros",
        value="`!ajuda` - Mostra esta mensagem",
        inline=False
    )

    embed.set_footer(text="Sistema de Coleta Financeira")

    await ctx.send(embed=embed)


async def enviar_status_todos_ativos(channel):
    """Envia status de todos os ativos para o canal"""
    try:
        ativos = db.listar_ativos()

        if not ativos:
            await channel.send("❌ Nenhum ativo disponível ainda. Execute uma coleta primeiro!")
            return

        embed = discord.Embed(
            title="📊 Status de Todos os Ativos",
            description=f"Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )

        for ativo_info in ativos:
            ativo = ativo_info['ativo']
            ultimo = db.obter_ultimo_preco(ativo)
            stats = db.obter_estatisticas(ativo, dias=7)

            if ultimo and stats:
                variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

                # Emoji baseado na variação
                if variacao > 5:
                    emoji = "📈"
                elif variacao < -5:
                    emoji = "📉"
                else:
                    emoji = "➡️"

                valor = (
                    f"{emoji} **${ultimo['preco']:,.2f}** {ultimo['moeda']}\n"
                    f"Variação 7d: {variacao:+.2f}%\n"
                    f"Máx: ${stats['preco_maximo']:,.2f} | Mín: ${stats['preco_minimo']:,.2f}"
                )

                embed.add_field(
                    name=f"{ativo}",
                    value=valor,
                    inline=False
                )

        embed.set_footer(text="Sistema de Coleta Financeira")

        await channel.send(embed=embed)
        logger.info(f'Status de todos os ativos enviado')

    except Exception as e:
        logger.error(f'Erro ao enviar status: {e}')
        await channel.send(f"❌ Erro ao buscar dados: {e}")


def main():
    """Função principal para iniciar o bot"""
    # Verificar se o token está configurado
    token = os.getenv('DISCORD_BOT_TOKEN')

    if not token:
        print("❌ ERRO: DISCORD_BOT_TOKEN não configurado!")
        print("\n📝 Para configurar o bot Discord:")
        print("1. Acesse: https://discord.com/developers/applications")
        print("2. Crie uma nova Application")
        print("3. Vá em 'Bot' e clique em 'Add Bot'")
        print("4. Copie o Token")
        print("5. Em 'Privileged Gateway Intents', ative 'Message Content Intent'")
        print("6. Adicione no arquivo .env:")
        print("   DISCORD_BOT_TOKEN=seu_token_aqui")
        print("\n7. Para adicionar o bot ao servidor:")
        print("   - Vá em OAuth2 > URL Generator")
        print("   - Marque: bot")
        print("   - Permissões: Send Messages, Embed Links, Read Message History")
        print("   - Copie a URL gerada e abra no navegador")
        return

    print("\n" + "=" * 60)
    print("🤖 INICIANDO BOT DISCORD")
    print("=" * 60)
    print(f"📊 Sistema de Coleta Financeira")
    print(f"🔑 Token configurado: {'*' * 20}")
    print("=" * 60)

    try:
        bot.run(token)
    except discord.LoginFailure:
        print("\n❌ ERRO: Token inválido!")
        print("Verifique se o DISCORD_BOT_TOKEN está correto no arquivo .env")
    except Exception as e:
        print(f"\n❌ ERRO ao iniciar bot: {e}")
        logger.error(f"Erro ao iniciar bot: {e}")


if __name__ == "__main__":
    main()
