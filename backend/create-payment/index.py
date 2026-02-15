import json
import os
import uuid
import base64
import urllib.request


def handler(event, context):
    """Создание платежа в ЮKassa для тарифов VIP и Премиум"""

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id',
                'Access-Control-Max-Age': '86400',
            },
            'body': '',
        }

    body = json.loads(event.get('body', '{}'))
    plan = body.get('plan')

    plans = {
        'vip': {'amount': '10.00', 'description': 'SellUp — тариф VIP'},
        'premium': {'amount': '50.00', 'description': 'SellUp — тариф Премиум'},
    }

    if plan not in plans:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Неверный тариф. Используйте vip или premium'}),
        }

    selected = plans[plan]
    shop_id = os.environ['YUKASSA_SHOP_ID']
    secret_key = os.environ['YUKASSA_SECRET_KEY']

    return_url = body.get('return_url', 'https://sellup.poehali.dev')

    payment_data = {
        'amount': {
            'value': selected['amount'],
            'currency': 'RUB',
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': return_url,
        },
        'capture': True,
        'description': selected['description'],
    }

    credentials = base64.b64encode(f'{shop_id}:{secret_key}'.encode()).decode()
    idempotence_key = str(uuid.uuid4())

    req = urllib.request.Request(
        'https://api.yookassa.ru/v3/payments',
        data=json.dumps(payment_data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
            'Idempotence-Key': idempotence_key,
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            'statusCode': e.code,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Ошибка создания платежа', 'details': error_body}),
        }

    confirmation_url = result.get('confirmation', {}).get('confirmation_url', '')

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'payment_id': result.get('id'),
            'confirmation_url': confirmation_url,
            'status': result.get('status'),
        }),
    }
