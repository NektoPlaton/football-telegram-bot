# data_api.py
# Implements wrappers over football-data.org API.
# You need to sign up at https://www.football-data.org/ and set X-Auth-Token in config.py

import requests
from datetime import datetime

BASE = 'https://api.football-data.org/v4'

def _get(path, api_key=None, params=None):
    if not api_key:
        return None, 'NO_API_KEY'
    headers = {'X-Auth-Token': api_key}
    url = BASE + path
    r = requests.get(url, headers=headers, params=params, timeout=10)
    if r.status_code != 200:
        return None, f'HTTP {r.status_code}: {r.text}'
    return r.json(), None

def get_next_matches(team_id, api_key, limit=5):
    data, err = _get(f'/teams/{team_id}/matches', api_key, params={'status':'SCHEDULED','limit':limit})
    if err:
        return f'Ошибка получения матчей: {err}\n(Проверьте, что в config.py указан корректный FOOTBALL_API_KEY)'
    matches = data.get('matches', [])
    if not matches:
        return 'Ближайших матчей не найдено.'
    lines = ['Ближайшие матчи:']
    for m in matches:
        dt = m.get('utcDate')
        when = datetime.fromisoformat(dt.replace('Z','+00:00')).strftime('%Y-%m-%d %H:%M UTC') if dt else '—'
        lines.append(f"{when} — {m['homeTeam']['name']} vs {m['awayTeam']['name']} ({m['competition']['name']})")
    return '\n'.join(lines)

def get_last_results(team_id, api_key, limit=5):
    data, err = _get(f'/teams/{team_id}/matches', api_key, params={'status':'FINISHED','limit':limit})
    if err:
        return f'Ошибка получения результатов: {err}\n(Проверьте, что в config.py указан корректный FOOTBALL_API_KEY)'
    matches = data.get('matches', [])
    if not matches:
        return 'Результатов не найдено.'
    lines = ['Последние игры:']
    for m in matches:
        dt = m.get('utcDate')
        when = datetime.fromisoformat(dt.replace('Z','+00:00')).strftime('%Y-%m-%d') if dt else '—'
        score = m.get('score', {})
        full = score.get('fullTime', {})
        lines.append(f"{when} — {m['homeTeam']['name']} {full.get('home', '?')}:{full.get('away','?')} {m['awayTeam']['name']}")
    return '\n'.join(lines)

def get_tournament_table(competition_code, api_key):
    data, err = _get(f'/competitions/{competition_code}/standings', api_key)
    if err:
        return f'Ошибка получения таблицы: {err}\n(Проверьте, что в config.py указан корректный FOOTBALL_API_KEY)'
    # We will show the first (TOTAL) table if present
    standings = data.get('standings', [])
    for s in standings:
        if s.get('type') == 'TOTAL':
            table = s.get('table', [])
            lines = [f"Турнир: {data.get('competition',{}).get('name','—')}", "Таблица:"]
            for row in table[:10]:
                pos = row.get('position')
                team = row.get('team',{}).get('name')
                pts = row.get('points')
                played = row.get('playedGames')
                lines.append(f"{pos}. {team} — {pts} очк. ({played} игр)")
            return '\n'.join(lines)
    return 'Таблица не найдена.'

def get_team_squad(team_id, api_key):
    data, err = _get(f'/teams/{team_id}', api_key)
    if err:
        return f'Ошибка получения состава: {err}\n(Проверьте, что в config.py указан корректный FOOTBALL_API_KEY)'

    team_name = data.get('name', 'Команда')
    coach = data.get('coach', {})
    squad = data.get('squad', [])

    lines = [f"Состав команды: {team_name}"]

    # Добавляем главного тренера
    if coach and coach.get('name'):
        nationality = coach.get('nationality', '—')
        lines.append(f"\nГлавный тренер: {coach['name']} ({nationality})")
    else:
        lines.append("\nГлавный тренер: не указан")

    lines.append("\nИгроки:")

    # Сортируем игроков по позиции, чтобы было красиво
    position_order = {'Goalkeeper': 1, 'Defence': 2, 'Midfield': 3, 'Offence': 4}
    squad_sorted = sorted(squad, key=lambda x: position_order.get(x.get('position', ''), 5))

    for p in squad_sorted:
        name = p.get('name', 'Без имени')
        position = p.get('position', '—')
        nationality = p.get('nationality', '—')
        lines.append(f"• {name} — {position} — {nationality}")

    return '\n'.join(lines)

def get_events():
    # Local/static events — you can edit this function or connect to your own DB
    events = [
        {'date':'2025-11-25','title':'Фан-встреча в фан-зоне'},
        {'date':'2025-12-10','title':'Автограф-сессия с игроками'}
    ]
    lines = ['Ближайшие события:']
    for e in events:
        lines.append(f"{e['date']} — {e['title']}")
    return '\n'.join(lines)
