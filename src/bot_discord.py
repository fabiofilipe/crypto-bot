"""
Bot Discord para consultas de criptomoedas
Execute: python -m bot_discord (com PYTHONPATH apontando para src/)
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

from database.db_manager import DatabaseManager
from utils.coinbase_api import CoinbaseAPI
from utils.logger import configurar_logger
from pipeline import ATIVOS_DISPONIVEIS

load_dotenv()
logger = configurar_logger("bot_discord")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
db = DatabaseManager()
api = CoinbaseAPI()


# ── Eventos ────────────────────────────────────────────────

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")
    print(f"✅ Bot conectado como {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "alerta" in message.content.lower():
        await comando_todos(message.channel)
        return
    await bot.process_commands(message)


# ── Helpers ────────────────────────────────────────────────

def _format_num(value: float, decimals: int = 2) -> str:
    """Formata número grande com separadores"""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if value >= 1_000:
        return f"${value:,.{decimals}f}"
    if value < 0.01:
        return f"${value:,.6f}"
    return f"${value:,.{decimals}f}"


def _emoji_variacao(valor: float) -> str:
    if valor > 2:
        return "🟢"
    if valor > 0:
        return "🟩"
    if valor > -2:
        return "🟥"
    return "🔴"


def _cor_variacao(valor: float) -> discord.Color:
    if valor > 0:
        return discord.Color.green()
    if valor < 0:
        return discord.Color.red()
    return discord.Color.greyple()


def _resolver_ativo(ativo: str) -> str:
    """Normaliza entrada para símbolo"""
    ativo = ativo.upper().strip()
    mapa = {
        "BITCOIN": "BTC", "BTC": "BTC",
        "ETHEREUM": "ETH", "ETH": "ETH", "ETHER": "ETH",
        "SOLANA": "SOL", "SOL": "SOL",
        "DOGECOIN": "DOGE", "DOGE": "DOGE", "DOG": "DOGE",
        "RIPPLE": "XRP", "XRP": "XRP",
        "CARDANO": "ADA", "ADA": "ADA",
        "AVALANCHE": "AVAX", "AVAX": "AVAX",
        "POLKADOT": "DOT", "DOT": "DOT",
        "CHAINLINK": "LINK", "LINK": "LINK",
        "POLYGON": "MATIC", "MATIC": "MATIC", "MATIC": "MATIC",
        "LITECOIN": "LTC", "LTC": "LTC",
        "SHIBA": "SHIB", "SHIB": "SHIB", "SHIBAINU": "SHIB",
    }
    return mapa.get(ativo, ativo)


# ── Comandos ───────────────────────────────────────────────

@bot.command(name="crypto", aliases=["c", "cripto"])
async def comando_crypto(ctx, ativo: str = None):
    """Relatório completo de uma criptomoeda
    Uso: !crypto BTC
    """
    if not ativo:
        await ctx.send("❌ Especifique um ativo! Ex: `!crypto BTC`")
        return

    simbolo = _resolver_ativo(ativo)
    ultimo = db.obter_ultimo_preco(simbolo)

    if not ultimo:
        await ctx.send(f"❌ Nenhum dado encontrado para **{simbolo}**.\nExecute uma coleta primeiro!")
        return

    stats_7d = db.obter_estatisticas(simbolo, dias=7)
    stats_24h = db.obter_variacao_24h(simbolo)
    taxa_brl = api.get_rate_to_currency("USD", "BRL")
    info_ativo = db.obter_info_ativo(simbolo)
    nome_ativo = info_ativo["nome"] if info_ativo else simbolo

    preco = float(ultimo["preco"])
    preco_brl = preco * taxa_brl if taxa_brl else None

    # Cores e emojis
    if stats_24h and stats_24h.get("variacao_pct") is not None:
        var_24h = stats_24h["variacao_pct"]
    elif stats_7d:
        var_24h = ((stats_7d["preco_maximo"] - stats_7d["preco_minimo"]) / stats_7d["preco_minimo"]) * 100
    else:
        var_24h = 0

    cor = _cor_variacao(var_24h)
    emoji = _emoji_variacao(var_24h)

    embed = discord.Embed(
        title=f"{emoji} {nome_ativo} ({simbolo})",
        color=cor,
        timestamp=datetime.now(),
    )

    # Preço
    valor_preco = f"**${preco:,.2f}** USD"
    if preco_brl:
        valor_preco += f"\n**R$ {preco_brl:,.2f}** BRL"
    embed.add_field(name="💰 Preço Atual", value=valor_preco, inline=False)

    # Variação 24h
    if stats_24h and stats_24h.get("variacao_pct") is not None:
        embed.add_field(
            name="📊 Variação 24h",
            value=f"{_emoji_variacao(var_24h)} **{var_24h:+.2f}%**",
            inline=True,
        )

    # Spread buy/sell (tempo real)
    market = api.get_market_data(f"{simbolo}-USD")
    if market and "buy_price" in market:
        spread_pct = market.get("spread_pct", 0)
        embed.add_field(
            name="💹 Spread",
            value=f"**{spread_pct:.2f}%**",
            inline=True,
        )

    # 7d stats
    if stats_7d and stats_7d["total_registros"] > 0:
        embed.add_field(
            name="📉 Mín 7d",
            value=_format_num(stats_7d["preco_minimo"]),
            inline=True,
        )
        embed.add_field(
            name="📊 Médio 7d",
            value=_format_num(stats_7d["preco_medio"]),
            inline=True,
        )
        embed.add_field(
            name="📈 Máx 7d",
            value=_format_num(stats_7d["preco_maximo"]),
            inline=True,
        )

        embed.add_field(
            name="📋 Registros 7d",
            value=f"{stats_7d['total_registros']:,}",
            inline=True,
        )

    embed.set_footer(text=f"Última coleta: {ultimo['horario_coleta']}")
    await ctx.send(embed=embed)
    logger.info(f"Relatório de {simbolo} enviado para {ctx.author}")


@bot.command(name="comparar", aliases=["cmp", "compare"])
async def comando_comparar(ctx, ativo1: str = None, ativo2: str = None):
    """Compara duas criptomoedas lado a lado
    Uso: !comparar BTC ETH
    """
    if not ativo1 or not ativo2:
        await ctx.send("❌ Especifique dois ativos! Ex: `!comparar BTC ETH`")
        return

    s1 = _resolver_ativo(ativo1)
    s2 = _resolver_ativo(ativo2)
    u1 = db.obter_ultimo_preco(s1)
    u2 = db.obter_ultimo_preco(s2)

    if not u1 or not u2:
        missing = []
        if not u1:
            missing.append(s1)
        if not u2:
            missing.append(s2)
        await ctx.send(f"❌ Sem dados para: {', '.join(missing)}")
        return

    stats1 = db.obter_estatisticas(s1, dias=7)
    stats2 = db.obter_estatisticas(s2, dias=7)
    taxa_brl = api.get_rate_to_currency("USD", "BRL")

    def campo(ativo, ultimo, stats):
        preco = float(ultimo["preco"])
        brl = f"\nR$ {preco * taxa_brl:,.2f}" if taxa_brl else ""
        var = "N/A"
        if stats and stats["total_registros"] > 0:
            v = ((stats["preco_maximo"] - stats["preco_minimo"]) / stats["preco_minimo"]) * 100
            var = f"{v:+.2f}%"
        return f"**${preco:,.2f}**{brl}\nVar 7d: {var}"

    embed = discord.Embed(
        title=f"⚖️ Comparativo: {s1} vs {s2}",
        color=discord.Color.blue(),
        timestamp=datetime.now(),
    )
    embed.add_field(name=s1, value=campo(s1, u1, stats1), inline=True)
    embed.add_field(name=s2, value=campo(s2, u2, stats2), inline=True)

    # Razão
    if u2["preco"] > 0:
        razao = u1["preco"] / u2["preco"]
        embed.add_field(
            name="Razão",
            value=f"1 {s1} = **{razao:,.4f}** {s2}",
            inline=False,
        )

    embed.set_footer(text=f"Última coleta: {u1['horario_coleta']}")
    await ctx.send(embed=embed)
    logger.info(f"Comparação {s1} vs {s2} enviada para {ctx.author}")


@bot.command(name="top", aliases=["ranking"])
async def comando_top(ctx, n: int = 5):
    """Ranking de criptos por variação
    Uso: !top 5
    """
    n = max(1, min(n, 20))
    ranking = db.obter_ranking_variacao(horas=24, limite=n)

    if not ranking:
        await ctx.send("❌ Sem dados suficientes para ranking.")
        return

    linhas = []
    for i, item in enumerate(ranking, 1):
        emoji = _emoji_variacao(item["variacao_pct"])
        nome = item["ativo"]
        var = f"{item['variacao_pct']:+.2f}%"
        preco = _format_num(item["preco_atual"])
        linhas.append(f"{i}. {emoji} **{nome}** → {var} ({preco})")

    embed = discord.Embed(
        title="🏆 Top Variação 24h",
        description="\n".join(linhas),
        color=discord.Color.gold(),
        timestamp=datetime.now(),
    )
    embed.set_footer(text="Ordenado por maior variação %")
    await ctx.send(embed=embed)


@bot.command(name="btc")
async def comando_btc(ctx):
    await comando_crypto(ctx, "BTC")


@bot.command(name="eth")
async def comando_eth(ctx):
    await comando_crypto(ctx, "ETH")


@bot.command(name="todos", aliases=["all", "tudo"])
async def comando_todos(channel):
    """Status de todos os ativos"""
    resumo = db.obter_resumo_mercado()
    if not resumo:
        if hasattr(channel, "send"):
            await channel.send("❌ Nenhum dado disponível.")
        return

    embed = discord.Embed(
        title="📊 Todas as Criptos",
        description=f"Atualizado: {datetime.now().strftime('%H:%M:%S')}",
        color=discord.Color.gold(),
        timestamp=datetime.now(),
    )

    taxa_brl = api.get_rate_to_currency("USD", "BRL")
    for item in resumo:
        ativo = item["ativo"]
        preco = float(item["preco"])
        brl = f"\nR$ {preco * taxa_brl:,.2f}" if taxa_brl else ""
        stats = db.obter_estatisticas(ativo, dias=7)
        var = "N/A"
        if stats and stats["total_registros"] > 0:
            v = ((stats["preco_maximo"] - stats["preco_minimo"]) / stats["preco_minimo"]) * 100
            var = f"{v:+.2f}%"
            emoji = _emoji_variacao(v)
        else:
            emoji = "⚪"

        embed.add_field(
            name=f"{emoji} {ativo}",
            value=f"**${preco:,.2f}**{brl}\nVar 7d: {var}",
            inline=False,
        )

    embed.set_footer(text="Sistema de Coleta Financeira")
    await channel.send(embed=embed)


@bot.command(name="ativos", aliases=["lista", "assets"])
async def comando_ativos(ctx):
    """Lista todos os ativos monitorados"""
    ativos = db.listar_ativos()
    if not ativos:
        await ctx.send("❌ Nenhum ativo registrado.")
        return

    linhas = []
    for a in ativos:
        info = db.obter_info_ativo(a["ativo"])
        nome = info["nome"] if info else a["ativo"]
        linhas.append(f"• **{a['ativo']}** — {nome}")

    embed = discord.Embed(
        title="📋 Ativos Monitorados",
        description="\n".join(linhas),
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)


@bot.command(name="ajuda", aliases=["comandos"])
async def comando_ajuda(ctx):
    embed = discord.Embed(
        title="📋 Comandos Disponíveis",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="💰 Consultas",
        value=(
            "`!crypto BTC` — Relatório completo\n"
            "`!comparar BTC ETH` — Comparação lado a lado\n"
            "`!top 5` — Ranking por variação 24h\n"
            "`!btc` / `!eth` — Atalhos rápidos\n"
            "`!todos` — Status de todos os ativos\n"
            "`!ativos` — Lista ativos monitorados"
        ),
        inline=False,
    )
    embed.add_field(
        name="💬 Automático",
        value="Digite `alerta` em qualquer canal para ver todos os ativos",
        inline=False,
    )
    embed.add_field(
        name="ℹ️ Atalhos",
        value="`!ajuda` — Esta mensagem",
        inline=False,
    )
    embed.set_footer(text="Sistema de Coleta Financeira")
    await ctx.send(embed=embed)


def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN não configurado!")
        return
    print(f"🤖 Iniciando bot...")
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Token inválido!")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
