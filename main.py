import os

import discord

import ML_in_game2
import avg
import ML
import ML_in_game
import account
import country_rank
import match_analyze
import track_tl

bot = discord.Bot()
guild = account.guild
admin = account.admin

def code(msg):
    return '```'+msg.replace('`', '\\`')+'```'

def row(msg):
    return msg.replace('_', '\\_')

@bot.slash_command(guild_ids=guild, description='플레이어의 Tetra League 정보를 분석합니다.', name='tetranalyze')
async def tetranalyze(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임', name='nick')):
    await ctx.defer()
    await ctx.respond(tafunc(ctx, nick))


@bot.slash_command(guild_ids=guild, description='플레이어의 Tetra League 정보를 바탕으로 승률을 예측합니다.', name='vs')
async def vs(ctx, player2: discord.Option(str, required=True, description='플레이어2의 닉네임', name='player2')
                , player1: discord.Option(str, required=False, description='플레이어1의 닉네임', name='player1')):
    await ctx.defer()

    if player1 is None:
        p1 = ML.getDiscordPlayerName(str(ctx.author.id))
        if p1 is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
            return
    else:
        p1 = player1.lower()

    try:
        userInfo1 = ML.playerInfo(p1)
        if userInfo1 is None:
            await ctx.respond(f'유저 {row(player1)}를 찾을 수 없습니다.')
            return
        Glicko1 = ML.predictGlicko(userInfo1['apm'], userInfo1['pps'], userInfo1['vs'])
    except:
        await ctx.respond('플레이어 \"' + row(p1) + '\" 는 Tetra League를 플레이한적이 없습니다.')
        return



    p2 = player2.lower()

    try:
        userInfo2 = ML.playerInfo(p2)
        if userInfo2 is None:
            await ctx.respond(f'유저 {row(player2)}를 찾을 수 없습니다.')
            return
        Glicko2 = ML.predictGlicko(userInfo2['apm'], userInfo2['pps'], userInfo2['vs'])
    except:
        await ctx.respond('플레이어 \"' + row(p2) + '\" 는 Tetra League를 플레이한적이 없습니다.')
        return

    wr_glk = 1/(10**((userInfo2['glicko']-userInfo1['glicko'])/400)+1)
    wr_stat = 1/(10**((Glicko2-Glicko1)/400)+1)

    sendStr = f'==========플레이어 {row(p1)}, 플레이어 {row(p2)}간 대결시 플레이어 {row(p1)}의 예상 승률==========\n'
    sendStr += f'Glicko 기반: {wr_glk*100:.2f}%\n'
    sendStr += f'스탯 기반: {wr_stat*100:.2f}%'
    await ctx.respond(sendStr)


@bot.slash_command(name="help", description="도움!!")
async def help(ctx):
    await ctx.defer()
    await ctx.respond(
        'Tetranalyze는 @muse918 이 개발한 Tetra League 분석 봇입니다.\n\ngpm: 분당 깎은 쓰레기줄의 수입니다.\nlpm: 분당 지운 라인의 수입니다.\napl: 라인당 보낸 쓰레기줄의 수입니다.\n'
        'app: 미노당 보낸 라인의 수입니다.\nlpp: 미노당 지운 라인의 수입니다.\ngpl: 지운 라인당 깎은 쓰레기줄의 수입니다.\n\n궁금한 점이 있으면 관리자에게 문의해주세요.')


def tafunc(ctx, nick):
    TR = 0
    player = None
    print(ctx.author, 'Queried')
    if nick is None:
        player = ML.getDiscordPlayerName(str(ctx.author.id))
        if player is None:
            return 'Discord 계정과 TETR.IO 계정을 연결해주세요.'
    else:
        player = nick.lower()

    try:
        userInfo = ML.playerInfo(player)
        if userInfo is None:
            return '유저를 찾을 수 없습니다.'
        TR = ML.predictTR(userInfo['apm'], userInfo['pps'], userInfo['vs'])
        Glicko = ML.predictGlicko(userInfo['apm'], userInfo['pps'], userInfo['vs'])
    except:
        return '플레이어 \"' + row(player) + '\" 는 Tetra League를 플레이한적이 없습니다.'
    info = ML.map_to_predict([userInfo['apm'], userInfo['pps'], userInfo['vs']])[0]
    sendStr = '닉네임 : ' + row(player)
    sendStr += f'\napm : {info[0]:.2f}'
    sendStr += f'\npps : {info[1]:.2f}'
    sendStr += f'\nVS : {info[2]:.2f}'
    sendStr += f'\ngpm : {info[3]:.2f}'
    sendStr += f'\nlpm : {info[4]:.2f}'
    sendStr += f'\napl : {info[5]:.2f}'
    sendStr += f'\napp : {info[6]:.2f}'
    sendStr += f'\nlpp : {info[7]:.2f}'
    sendStr += f'\ngpl : {info[8]:.2f}'
    sendStr += '\n\n==========\n\nTR : ' + str(round(userInfo['rating'], 2))
    sendStr += '\nGlicko : ' + str(round(userInfo['glicko'], 2))
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko, 2))

    return sendStr


@bot.slash_command(guild_ids=guild, description='플레이어의 Tetra League 정보를 분석합니다.', name='ta')
async def ta(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임')):
    await ctx.defer()
    await ctx.respond(tafunc(ctx, nick))

@bot.slash_command(guild_ids=guild, description='플레이어 데이터를 분석합니다.', name='analyze_record')
async def analyze_record(ctx, apm: discord.Option(float, required=True, description='분석할 APM', name='apm'),
                         pps: discord.Option(float, required=True, description='분석할 PPS', name='pps'),
                         vs: discord.Option(float, required=True, description='분석할 VS', name='vs')):
    await ctx.defer()
    TR = ML.predictTR(apm, pps, vs)
    Glicko = ML.predictGlicko(apm, pps, vs)
    info = ML.map_to_predict([apm, pps, vs])[0]
    sendStr = '=====분석 결과=====\n'
    sendStr += f'\napm : {info[0]:.2f}'
    sendStr += f'\npps : {info[1]:.2f}'
    sendStr += f'\nVS : {info[2]:.2f}'
    sendStr += f'\ngpm : {info[3]:.2f}'
    sendStr += f'\nlpm : {info[4]:.2f}'
    sendStr += f'\napl : {info[5]:.2f}'
    sendStr += f'\napp : {info[6]:.2f}'
    sendStr += f'\nlpp : {info[7]:.2f}'
    sendStr += f'\ngpl : {info[8]:.2f}'
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko, 2))
    await ctx.respond(sendStr)


@bot.slash_command(guild_ids=guild, description='경기 데이터를 분석합니다.', name='analyze_record_match_legacy')
async def analyze_record_match_legacy(ctx, apm: discord.Option(float, required=True, description='분석할 APM', name='apm'),
                         pps: discord.Option(float, required=True, description='분석할 PPS', name='pps'),
                         vs: discord.Option(float, required=True, description='분석할 VS', name='vs'),
                         time: discord.Option(float, required=True, description='분석할 게임의 길이(초)', name='time')):
    await ctx.defer()
    TR = ML_in_game.predictTR(apm, pps, vs, time)
    Glicko = ML_in_game.predictGlicko(apm, pps, vs, time)
    info = ML_in_game.map_to_predict([apm, pps, vs], time)[0]
    sendStr = '=====분석 결과=====\n'
    sendStr += f'\napm : {info[0]:.2f}'
    sendStr += f'\npps : {info[1]:.2f}'
    sendStr += f'\nVS : {info[2]:.2f}'
    sendStr += f'\ntime : {info[9]:.2f}'
    sendStr += f'\ngpm : {info[3]:.2f}'
    sendStr += f'\nlpm : {info[4]:.2f}'
    sendStr += f'\napl : {info[5]:.2f}'
    sendStr += f'\napp : {info[6]:.2f}'
    sendStr += f'\nlpp : {info[7]:.2f}'
    sendStr += f'\ngpl : {info[8]:.2f}'
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko, 2))
    await ctx.respond(sendStr)


@bot.slash_command(guild_ids=guild, description='경기 데이터를 분석합니다.', name='analyze_record_match')
async def analyze_record_match(ctx, apm1: discord.Option(float, required=True, description='분석할 APM(나)', name='apm1'),
                         pps1: discord.Option(float, required=True, description='분석할 PPS(나)', name='pps1'),
                         vs1: discord.Option(float, required=True, description='분석할 VS(나)', name='vs1'),
                         apm2: discord.Option(float, required=True, description='분석할 APM(나)', name='apm2'),
                         pps2: discord.Option(float, required=True, description='분석할 PPS(나)', name='pps2'),
                         vs2: discord.Option(float, required=True, description='분석할 VS(나)', name='vs2'),
                         time: discord.Option(float, required=True, description='분석할 게임의 길이(초)', name='time')):
    await ctx.defer()
    TR1 = ML_in_game2.predictTR(apm1, pps1, vs1, apm2, pps2, vs2, time)
    Glicko1 = ML_in_game2.predictGlicko(apm1, pps1, vs1, apm2, pps2, vs2, time)
    TR2 = ML_in_game2.predictTR(apm2, pps2, vs2, apm1, pps1, vs1, time)
    Glicko2 = ML_in_game2.predictGlicko(apm2, pps2, vs2, apm1, pps1, vs1, time)
    info1 = ML_in_game.map_to_predict([apm1, pps1, vs1], time)[0]
    info2 = ML_in_game.map_to_predict([apm2, pps2, vs2], time)[0]
    sendStr = '=====나의 분석 결과=====\n'
    sendStr += f'\napm : {info1[0]:.2f}'
    sendStr += f'\npps : {info1[1]:.2f}'
    sendStr += f'\nVS : {info1[2]:.2f}'
    sendStr += f'\ntime : {info1[9]:.2f}'
    sendStr += f'\ngpm : {info1[3]:.2f}'
    sendStr += f'\nlpm : {info1[4]:.2f}'
    sendStr += f'\napl : {info1[5]:.2f}'
    sendStr += f'\napp : {info1[6]:.2f}'
    sendStr += f'\nlpp : {info1[7]:.2f}'
    sendStr += f'\ngpl : {info1[8]:.2f}'
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR1, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko1, 2)) + '\n\n\n'
    sendStr = '=====.상대의 분석 결과=====\n'
    sendStr += f'\napm : {info2[0]:.2f}'
    sendStr += f'\npps : {info2[1]:.2f}'
    sendStr += f'\nVS : {info2[2]:.2f}'
    sendStr += f'\ntime : {info2[9]:.2f}'
    sendStr += f'\ngpm : {info2[3]:.2f}'
    sendStr += f'\nlpm : {info2[4]:.2f}'
    sendStr += f'\napl : {info2[5]:.2f}'
    sendStr += f'\napp : {info2[6]:.2f}'
    sendStr += f'\nlpp : {info2[7]:.2f}'
    sendStr += f'\ngpl : {info2[8]:.2f}'
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR2, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko2, 2))
    await ctx.respond(sendStr)


def moreData(apm, pps, vs):
    info = ML.map_to_predict([apm, pps, vs])[0]
    TR = ML.predictTR(apm, pps, vs)
    Glicko = ML.predictGlicko(apm, pps, vs)
    sendStr = ''
    sendStr += f'\napm : {info[0]:.2f}'
    sendStr += f'\npps : {info[1]:.2f}'
    sendStr += f'\nVS : {info[2]:.2f}'
    sendStr += f'\ngpm : {info[3]:.2f}'
    sendStr += f'\nlpm : {info[4]:.2f}'
    sendStr += f'\napl : {info[5]:.2f}'
    sendStr += f'\napp : {info[6]:.2f}'
    sendStr += f'\nlpp : {info[7]:.2f}'
    sendStr += f'\ngpl : {info[8]:.2f}'
    sendStr += '\n\n=====봇의 예측=====\n\nTR : ' + str(round(TR, 2))
    sendStr += '\nGlicko : ' + str(round(Glicko, 2))
    return sendStr


@bot.slash_command(guild_ids=guild, description='Tetra League 경기를 분석합니다.', name='analyze_match')
async def analyze_match(ctx, user_name: discord.Option(str, required=False, description='플레이어의 닉네임', name='username')):
    await ctx.defer()
    if user_name is None:
        player = ML.getDiscordPlayerId(ctx.author.id)
        if player is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
            return
    else:
        player = ML.playerId(user_name)
        if player is None:
            await ctx.respond('플레이어가 존재하지 않습니다.')
            return
    match = ML.getLatestMatch(player)
    if match is None:
        await ctx.respond('이 플레이어의 마지막 매치를 찾을 수 없습니다.')
        return
    sendStr = f'리플레이 ID : {match[0]}\n' \
              f'{match[1][0][0]} VS {match[1][1][0]}\n' \
              f'\n======={match[1][0][0]} : {match[1][0][1]}점=======\n' \
              f'{moreData(match[1][0][2], match[1][0][3], match[1][0][4])}\n\n' \
              f'\n======={match[1][1][0]} : {match[1][1][1]}점=======\n' \
              f'{moreData(match[1][1][2], match[1][1][3], match[1][1][4])}'
    await ctx.respond(sendStr)\

@bot.slash_command(guild_ids=guild, description='Tetra League 경기를 분석합니다.', name='analyze_match_id')
async def analyze_match_id(ctx, match_id: discord.Option(str, required=True, description='매치의 ID', name='id')):
    await ctx.defer()
    match = ML.getMatchId(match_id)
    if match is None:
        await ctx.respond('유효하지 않은 리플레이이거나 1 VS 1 리플레이가 아닙니다.')
        return
    sendStr = f'리플레이 ID : {match[0]}\n' \
              f'{match[1][0][0]} VS {match[1][1][0]}\n' \
              f'\n======={match[1][0][0]} : {match[1][0][1]}점=======\n' \
              f'{moreData(match[1][0][2], match[1][0][3], match[1][0][4])}\n\n' \
              f'\n======={match[1][1][0]} : {match[1][1][1]}점=======\n' \
              f'{moreData(match[1][1][2], match[1][1][3], match[1][1][4])}'
    await ctx.respond(sendStr)


@bot.slash_command(guild_ids=guild, description='Tetra League 경기별 퍼포먼스를 분석합니다.', name='analyze_match_more')
async def analyze_match_more(ctx, user_name: discord.Option(str, required=False, description='플레이어의 닉네임', name='username')):
    await ctx.defer()
    if user_name is None:
        player = ML.getDiscordPlayerId(ctx.author.id)
        if player is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
            return
    else:
        player = ML.playerId(user_name)
        if player is None:
            await ctx.respond('플레이어가 존재하지 않습니다.')
            return
    match = ML.getFullLatestMatch(player)
    if match is None:
        await ctx.respond('이 플레이어의 마지막 매치를 찾을 수 없습니다.')
        return
    path = match_analyze.analyze(match)
    await ctx.respond('', file=discord.File(path))
    os.remove(path)

@bot.slash_command(guild_ids=guild, description='Tetra League 경기별 퍼포먼스를 분석합니다.', name='analyze_match_more_legacy')
async def analyze_match_more_legacy(ctx, user_name: discord.Option(str, required=False, description='플레이어의 닉네임',
                                                            name='username')):
    await ctx.defer()
    if user_name is None:
        player = ML.getDiscordPlayerId(ctx.author.id)
        if player is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
            return
    else:
        player = ML.playerId(user_name)
        if player is None:
            await ctx.respond('플레이어가 존재하지 않습니다.')
            return
    match = ML.getFullLatestMatch(player)
    if match is None:
        await ctx.respond('이 플레이어의 마지막 매치를 찾을 수 없습니다.')
        return
    path = match_analyze.analyze_legacy(match)
    await ctx.respond('', file=discord.File(path))
    os.remove(path)

@bot.slash_command(guild_ids=guild, description='Tetra League 경기별 퍼포먼스를 분석합니다.', name='analyze_match_more_id')
async def analyze_match_more_id(ctx, match_id: discord.Option(str, required=True, description='매치의 ID', name='id')):
    await ctx.defer()
    match = ML.getFullMatchId(match_id)
    if match is None:
        await ctx.respond('유효하지 않은 리플레이이거나 1 VS 1 리플레이가 아닙니다.')
        return
    path = match_analyze.analyze(match)
    await ctx.respond('', file=discord.File(path))
    os.remove(path)\


@bot.slash_command(guild_ids=guild, description='Tetra League 경기별 퍼포먼스를 분석합니다.', name='analyze_match_more_id_legacy')
async def analyze_match_more_id_legacy(ctx, match_id: discord.Option(str, required=True, description='매치의 ID', name='id')):
    await ctx.defer()
    match = ML.getFullMatchId(match_id)
    if match is None:
        await ctx.respond('유효하지 않은 리플레이이거나 1 VS 1 리플레이가 아닙니다.')
        return
    path = match_analyze.analyze_legacy(match)
    await ctx.respond('', file=discord.File(path))
    os.remove(path)



@bot.slash_command(guild_ids=guild, description='일정 랭크에 속한 사람들의 평균을 출력합니다.', name='tetrank')
async def tetrank(ctx, rank: discord.Option(str, required=True, description='랭크',
                                            choices=['d', 'd+', 'c-', 'c', 'c+', 'b-', 'b', 'b+', 'a-', 'a', 'a+', 's-',
                                                     's', 's', 's+', 'ss', 'u', 'x'])):
    await ctx.defer()
    await ctx.respond(avg.avg_rank(rank))


@bot.slash_command(guild_ids=guild, description='일정 구간에 속한 사람들의 평균을 출력합니다.', name='tetrange')
async def tetrange(ctx,
                   rangetype: discord.Option(str, required=True, description='범위의 종류', choices=['rating', 'glicko']),
                   start: discord.Option(float, required=True, description='시작 범위'),
                   end: discord.Option(float, required=True, description='종료 범위')):
    await ctx.defer()
    if rangetype == 'rating':
        await ctx.respond(avg.avg_range_TR(start, end))
    elif rangetype == 'glicko':
        await ctx.respond(avg.avg_range_Glicko(start, end))


@bot.slash_command(guild_ids=guild, description='플레이어와 점수가 비슷한 사람들의 평균을 출력합니다.', name='tetravg')
async def tetravg(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임', name='nick'),
                  rng: discord.Option(float, required=False, description='주변 Glicko 범위', name='range') = 100):
    await ctx.defer()
    await ctx.respond(avgfunc(ctx, nick, rng))


def avgfunc(ctx, nick, rng):
    TR = 0
    player = None
    print(ctx.author, 'Queried')
    if nick is None:
        player = ML.getDiscordPlayerName(str(ctx.author.id))
        if player is None:
            return 'Discord 계정과 TETR.IO 계정을 연결해주세요.'

    else:
        player = nick.lower()

    try:
        userInfo = ML.playerInfo(player)
        if userInfo is None:
            return '유저를 찾을 수 없습니다.'
        TR = ML.predictTR(userInfo['apm'], userInfo['pps'], userInfo['vs'])
        Glicko = ML.predictGlicko(userInfo['apm'], userInfo['pps'], userInfo['vs'])
    except:
        return '플레이어 \"' + row(player) + '\" 는 Tetra League를 플레이한적이 없습니다.'
    info = ML.map_to_predict([userInfo['apm'], userInfo['pps'], userInfo['vs']])[0]
    sendStr = '닉네임 : ' + row(player)
    sendStr += f'\napm : {info[0]:.2f}'
    sendStr += f'\npps : {info[1]:.2f}'
    sendStr += f'\nVS : {info[2]:.2f}'
    sendStr += f'\ngpm : {info[3]:.2f}'
    sendStr += f'\nlpm : {info[4]:.2f}'
    sendStr += f'\napl : {info[5]:.2f}'
    sendStr += f'\napp : {info[6]:.2f}'
    sendStr += f'\nlpp : {info[7]:.2f}'
    sendStr += f'\ngpl : {info[8]:.2f}'
    sendStr += '\n\n==========\n\nTR : ' + str(round(userInfo['rating'], 2))
    sendStr += '\nGlicko : ' + str(round(userInfo['glicko'], 2))
    glk = userInfo['glicko']
    sendStr += f'\n\n=====주위 플레이어들의 평균=====\n\nTR 범위 : {ML.glicko_to_tr(glk - rng):.2f} - {ML.glicko_to_tr(glk + rng):.2f}\n' + avg.avg_range_Glicko(
        glk - rng, glk + rng)

    return sendStr


@bot.slash_command(guild_ids=guild, description='플레이어와 점수가 비슷한 사람들의 평균을 출력합니다.', name='tavg')
async def tavg(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임'),
               rng: discord.Option(float, required=False, description='주변 Glicko 범위', name='range') = 100):
    await ctx.defer()
    await ctx.respond(avgfunc(ctx, nick, rng))


@bot.slash_command(guild_ids=guild, description='40L의 지역 랭킹을 확인합니다.', name='country_rank_40l')
async def country_rank_40l(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임')):
    await ctx.defer()

    if nick is None:
        player = ML.getDiscordPlayerName(str(ctx.author.id))
        if player is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
    else:
        player = nick.lower()
    rank = country_rank.sprint(player)
    if rank is None:
        await ctx.respond('플레이어를 찾을 수 없습니다.')
        return
    if rank == -1:
        await ctx.respond('지역 설정이 되어있지 않습니다.')
        return
    if rank == -2:
        await ctx.respond('Global #1000 미만의 플레이어는 검색할 수 없습니다.')
        return
    else:
        await ctx.respond(f'플레이어 {row(player)}의 40L 지역 랭크는 {rank[1]} #{rank[0]} 입니다.')


@bot.slash_command(guild_ids=guild, description='Blitz의 지역 랭킹을 확인합니다.', name='country_rank_blitz')
async def country_rank_blitz(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임')):
    await ctx.defer()

    if nick is None:
        player = ML.getDiscordPlayerName(str(ctx.author.id))
        if player is None:
            await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
            return
    else:
        player = nick.lower()
    rank = country_rank.blitz(player)
    if rank is None:
        await ctx.respond('플레이어를 찾을 수 없습니다.')
        return
    if rank == -1:
        await ctx.respond('지역 설정이 되어있지 않습니다.')
        return
    if rank == -2:
        await ctx.respond('Global #1000 미만의 플레이어는 검색할 수 없습니다.')
        return
    else:
        await ctx.respond(f'플레이어 {row(player)}의 Blitz 지역 랭크는 {rank[1]} #{rank[0]} 입니다.')


# @bot.slash_command(guild_ids=guild, description='유저의 Tetra League 기록을 추적을 시작합니다.', name='track')
# async def track(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임')):
#     await ctx.defer()
#
#     if nick is None:
#         player = ML.getDiscordPlayerName(str(ctx.author.id))
#         if player is None:
#             await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
#             return
#     else:
#         player = nick.lower()
#     if track_tl.track(player):
#         await ctx.respond(f'플레이어 {row(player)}의 TL 추적을 시작합니다.')
#     else:
#         await ctx.respond(f'플레이어 {row(player)}의 TL 추적을 시작하지 못했습니다.(이미 추적중이거나 플레이어를 찾을 수 없습니다.)')
#
#
#
# @bot.slash_command(guild_ids=guild, description='Tetra League 기록을 추적중인 유저들을 표시합니다.', name='track_list')
# async def track_list(ctx):
#     await ctx.defer(ephemeral=True)
#
#     if ctx.author.id in admin:
#         await ctx.respond('======list======\n' + '\n'.join(track_tl.list_track()), ephemeral=True)
#     else:
#         await ctx.respond('이 명령어를 사용할 권한이 없습니다.', ephemeral=True)
#
#
# @bot.slash_command(guild_ids=guild, description='유저의 Tetra League 기록을 추적을 중단합니다.', name='untrack')
# async def untrack(ctx, nick: discord.Option(str, required=True, description='플레이어의 닉네임')):
#     await ctx.defer(ephemeral=True)
#
#     player = nick.lower()
#     if ctx.author.id in admin:
#         if track_tl.untrack(player):
#             await ctx.respond(f'플레이어 {row(player)}의 TL 추적을 종료합니다.')
#         else:
#             await ctx.respond(f'플레이어 {row(player)}의 TL 추적을 종료하지 못했습니다.(추적중이 아니거나 플레이어를 찾을 수 없습니다.)')
#
#     else:
#         await ctx.respond('이 명령어를 사용할 권한이 없습니다.', ephemeral=True)
#
# @bot.slash_command(guild_ids=guild, description='유저의 Tetra League 기록을 추적을 확인합니다.', name='show_track')
# async def show_track(ctx, nick: discord.Option(str, required=False, description='플레이어의 닉네임'), num: discord.Option(int, required=False, description='확인할 개수') = 5):
#     await ctx.defer()
#
#     if nick is None:
#         player = ML.getDiscordPlayerName(str(ctx.author.id))
#         if player is None:
#             await ctx.respond('Discord 계정과 TETR.IO 계정을 연결해주세요.')
#             return
#     else:
#         player = nick.lower()
#     ans = track_tl.show(player, num)
#     if ans is None:
#         await ctx.respond(f'플레이어 {row(player)}의 TL 추적을 확인하지 못했습니다.')
#     else:
#         await ctx.respond(ans)

@bot.slash_command(guild_ids=guild, description='분석에 사용하는 유저 DB를 최신으로 업데이트합니다.', name='update_db')
async def update_db(ctx):
    await ctx.defer(ephemeral=True)
    avg.update()
    country_rank.update()
    await ctx.respond('성공적으로 업데이트되었습니다.', ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('TETR.IO를 분석'))


bot.run(account.token)



