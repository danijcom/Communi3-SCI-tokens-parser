import os
import time
import datetime
import requests
import selenium.webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_token_authority(nft_addr: str) -> str:
    """
    Get token authority address from NFT address using solscan.io API
    :param nft_addr: Address of NFT
    :return: NFT authority address
    """
    try:
        req = requests.get(f'https://public-api.solscan.io/token/meta?tokenAddress={nft_addr}')
    except Exception as ex:
        print(f'Exception with solscan: {ex}\nRetry in 5 sec!')
        time.sleep(5)
        return get_token_authority(nft_addr)
    if req.status_code == 200:
        return req.json()['tokenAuthority']
    elif req.status_code == 400:
        print(f'Solscan API: status code {req.status_code} - Bad Request\nRetry in 5 sec!')
    elif req.status_code == 429:
        print(f'Solscan API: status code {req.status_code} - Too Many Requests\nRetry in 5 sec!')
    elif req.status_code == 200:
        print(f'Solscan API: status code {req.status_code} - Internal Server Error\nRetry in 5 sec!')
    time.sleep(5)
    return get_token_authority(nft_addr)


def get_token_amount(nft_authority: str) -> int:
    """
    Get amount of SCI tokens that NFT has using madsci-status.app (because I don't know how to calculate it)...
    :param nft_authority: NFT authority address. NOT TOKEN ADDRESS!
    :return: Amount of SCI left
    """
    try:
        req = requests.post('https://www.madsci-status.app/results', data={'tokenAddress': nft_authority})
    except Exception as ex:
        print(f'Exception with madsci-status: {ex}\nRetry in 5 sec!')
        time.sleep(5)
        return get_token_amount(nft_authority)
    if 'Hmm...' in req.text:
        print(f'madsci-status lag... Retry in 5 sec!')
        time.sleep(5)
        return get_token_amount(nft_authority)
    return int(req.text)


def process_nfts(driver, processed, file, max_price) -> tuple[list, list, bool]:
    """
    Get all NFTs on webpage and process all of them (get info and SCI amount)
    :param driver: Selenium webdriver
    :param processed: List with currently processed NTFs IDs
    :param file: Output file
    :param max_price: Max price for ntf
    :return: Tuple with: list[dict[nft data], list[int[nft_ids]]], bool[is_max_price_exceeded]
    """
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "css-g0fuxu")))
    except Exception as ex:
        print("Can't find NFTs cards. "
              "May be you have to replace its class in script (read ..)")
        driver.quit()
        quit(0)
    all_items = driver.find_elements(By.CLASS_NAME, "css-g0fuxu")

    nfts_data = []
    processed_ids = []
    price_limit = False
    for nft in all_items:
        item_price = float(nft.find_element(By.CLASS_NAME, "css-1jvkpkw").find_element(By.CLASS_NAME,"css-1auo7vn").find_element(By.TAG_NAME, "p").text)
        if item_price > max_price:
            price_limit = True
            break
        item_id = int(nft.find_element(By.CLASS_NAME, "css-1y30grd").find_element(By.CLASS_NAME,"css-1bz28w4").find_element(By.TAG_NAME,"h4").text.replace('#', ''))
        if item_id in processed:
            continue
        item_link = nft.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(f'Processing #{item_id}...')
        nft_authority = get_token_authority(item_link.replace('https://hyperspace.xyz/token/', ''))
        print(f'Authority: {nft_authority}')
        item_tokens = get_token_amount(nft_authority)
        print(f'Tokens: {item_tokens}')
        nfts_data.append({
            'price': item_price,
            'id': item_id,
            'link': item_link,
            'authority': nft_authority,
            'tokens': item_tokens
        })
        print(f'#{item_id:4d}: {item_tokens:5d} $SCI - {item_price:2.2f} $SOL - {item_link} - {nft_authority}\n')

        with open(file, 'a+') as f:
            f.write(f'#{item_id:4d}: {item_tokens:5d} $SCI - {item_price:2.2f} $SOL - {item_link} - {nft_authority}\n')

        processed_ids.append(item_id)

    return nfts_data, processed_ids, price_limit


def find_nfts(driver: selenium.webdriver, file: str, max_price: float) -> list:
    """
    Main function Get NFTs market page - process visible NFTs, scroll page - repeat
    :param driver: Selenium webdriver obj
    :param file: Path to output file
    :param max_price: Max price for NFT to process it
    :return:
    """
    driver.get('https://hyperspace.xyz/collection/communi3madscientists')
    time.sleep(5)

    all_nfts = []
    processed_ids = []

    size_y = driver.get_window_size()['height']
    scroll_y = size_y
    for i in range(6):
        p_nfts, p_ids, is_price_limit = process_nfts(driver, processed_ids, file, max_price)
        all_nfts += p_nfts
        processed_ids += p_ids
        if is_price_limit:
            print('Price limit!')
            break
        driver.execute_script(f"window.scrollTo(0, {scroll_y})")
        scroll_y += size_y
        time.sleep(2)

    print('In total processed {} NTFs!'.format(len(processed_ids)))
    return all_nfts


if __name__ == '__main__':
    # Max price. Script will be stopped, when NFTs price exceeded that amount of SOL.
    MAX_PRICE = 9999

    driver = selenium.webdriver.Chrome(executable_path='chromium\\chromedriver.exe')
    out_file = '{}.txt'.format(datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S'))
    print(f'Starting processing! Output file: {out_file}')
    find_nfts(driver, out_file, MAX_PRICE)
    if os.path.isfile(out_file):
        os.startfile(out_file)
