from lunespy.server import Node
from lunespy.utils import unes_to_lunes
from lunespy.utils import export_json
from requests import get


def address_associated_with_an_alias(alias: str, node_url: str = None) -> dict:
    if node_url == None:
       full_url = f'{Node.mainnet_url.value}/addresses/alias/by-alias/{alias}'

    else:
        full_url = f'https://{node_url}/addresses/alias/by-alias/{alias}'
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def asset_distribution(asset_id: str, node_url: str == None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/assets/{asset_id}/distribution'
    else: 
        full_url = f'http://{node_url}/assets/{asset_id}/distribution'
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def balance_all_assets_of_address(address: str, node_url: str == None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/assets/balance/{address}'
    else:
        full_url = f'https://{node_url}/assets/balance/{address}'
    
    response = get(full_url)
    
    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def balance_for_especify_asset_of_address(address: str, asset_id: str, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/assets/balance/{address}/{asset_id}'
    else:
        full_url = f'{node_url}/assets/balance/{address}/{asset_id}'
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def balance_of_all_address(node_ip: str, node_api_key: str) -> dict:    
    full_url = f"http://{node_ip}/debug/state"
    header = {"X-API-key": node_api_key}
    response = get(full_url, headers=header)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def balance_of_address(address: str, node_url: str = None) -> int:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/addresses/balance/{address}'
    else:
        full_url = f'http://{node_url}/addresses/balance/{address}'
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def list_of_rich(**kargs: dict) -> dict:
    """
    Example:
        quantity=30,
        node_ip_port="127.0.0.1:555",
        net="mainnet" or "testnet"
        node_api_key="",
        export=True or False,
        path='./data/'
    """
    def percent(amount: float) -> float:
        return round((amount / supply) * 100, 5)

    def percent_total(wallets: list) -> float:
        total = sum([
            i['amount']
            for i in wallets
        ])
        return percent(total)
    
    response = balance_of_all_address(kargs['node_ip'], kargs['node_api_key'])
    supply = Node.mainnet_total_supply.value if kargs['net'] == 'mainnet' else Node.testnet_total_supply.value
    link = Node.mainnet_blockexplorer.value if kargs['net'] == 'mainnet' else Node.testnet_blockexplorer.value

    if response['status'] != 'ok':
        return  {
            'status': 'error',
            'response': response['response']
        }
    else:
        wallets_lunes = dict(zip(
            response['response'],
            list(map(
                lambda item: unes_to_lunes(item),
                response['response'].values()
            ))
        ))

        wallets = sorted(
            [
                {
                    'address': address,
                    'amount': amount,
                    'percent': percent(amount),
                    'link': f'{link}/address/{address}'
                }
                for address, amount in list(
                    wallets_lunes.items()
                )
            ],
            key = lambda item: item.get('amount'),
            reverse = True
        )[:kargs.get('quantity')]

        report = {
            "total_supply": supply,
            "network": kargs['net'],
            "total_percent": percent_total(wallets),
            "wallet_list": wallets
        }

        if kargs.get('export', False):
            export_json(
                report,
                "rich_list",
                kargs.get('path', './data/')
            )

        return  {
            'status': 'ok',
            'response': report
        }


def leasing_active_by_address(address: str, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/leasing/active/{address}'
    else:
        full_url = f'https://{node_url}/leasing/active/{address}'

    response = get(full_url)
    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': 
                {
                    full_url.replace('/addresses',''): response.json()
                }
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def address_of_node_from_url(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/addresses'

    else:
        full_url = f'https://{node_url}/addresses'
            
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def aliases_associated_with_an_address(address: str, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}addresses/alias/by-address/{address}'
    else:
        full_url = f'https://{node_url}/addresses/alias/by-address/{address}'

    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else: 
        return {
            'status': 'error',
            'response': response.text
        }
