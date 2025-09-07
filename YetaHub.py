#!/usr/bin/python
# -*- coding: utf-8 -*-
print("Halo, dunia! こんにちは世界")
import os, sys
import requests
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import re
import getpass

# Inisialisasi colorama
init(autoreset=True)

def is_valid(url):
    """
    Memeriksa apakah URL valid (memiliki skema dan domain).
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url):
    """
    Mengambil semua link halaman yang mengandung 'php?id=' dari URL yang diberikan.
    Pencarian diperluas ke seluruh teks halaman dan atribut lain.
    """
    print(Fore.YELLOW + "[*] Searching for php?id= links..." + Style.RESET_ALL)
    urls = set()
    domain_name = urlparse(url).netloc

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error saat mengakses {url}: {e}" + Style.RESET_ALL)
        return urls

    # 1. Cari link di tag <a>
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        if not href:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        if not is_valid(href):
            continue
        if domain_name not in parsed_href.netloc:
            continue

        # Cek apakah path berakhiran .php dan query string mengandung parameter 'id'
        if parsed_href.path.endswith(".php"):
            query_params = parse_qs(parsed_href.query)
            if 'id' in query_params:
                full_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + "?" + parsed_href.query
                urls.add(full_url)

    # 2. Cari link di atribut lain yang mungkin mengandung URL dengan php?id=
    # Contoh: onclick="location.href='page.php?id=123'"
    # Cari semua atribut yang mengandung 'php?id=' menggunakan regex
    pattern = re.compile(r"(https?://[^\s'\"<>]+php\?[^'\"<>]*id=[^'\"<>]+|[^\s'\"<>]+php\?[^'\"<>]*id=[^'\"<>]+)", re.IGNORECASE)
    matches = pattern.findall(response.text)
    for match in matches:
        # Jika link relatif, gabungkan dengan base url
        full_link = urljoin(url, match)
        parsed_link = urlparse(full_link)
        if not is_valid(full_link):
            continue
        if domain_name not in parsed_link.netloc:
            continue
        urls.add(full_link)

    # 3. Cari link di form action yang mengandung php?id=
    for form in soup.find_all("form"):
        action = form.attrs.get("action")
        if not action:
            continue
        action = urljoin(url, action)
        parsed_action = urlparse(action)
        if not is_valid(action):
            continue
        if domain_name not in parsed_action.netloc:
            continue
        if parsed_action.path.endswith(".php"):
            query_params = parse_qs(parsed_action.query)
            if 'id' in query_params:
                urls.add(action)

    print(Fore.GREEN + f"[+] Found {len(urls)} php?id= links." + Style.RESET_ALL)
    return urls

def find_admin_login_pages(base_url):
    """
    Mencari halaman login admin yang umum pada domain yang sama.
    Mengembalikan set URL yang aktif (status 200).
    """
    common_admin_paths = [
        "admin/",
        "administrator/",
        "admin.php",
        "admin.html",
        "login/",
        "login.php",
        "login.html",
        "user/login",
        "wp-login.php",
        "cpanel/",
        "adminpanel/",
        "adminarea/",
        "admin_login.php",
        "admin1.php",
        "admin2.php",
        "admin3.php",
        "admin4.php",
        "admin5.php",
        "admin-login.php",
        "admin_area/",
        "panel-administracion/",
        "instadmin/",
        "memberadmin/",
        "administratorlogin/",
        "adm/",
        "admin/account.php",
        "admin/index.php",
        "admin/login.html",
        "admin/admin_login.html",
        "admin_login.html",
        "admin/admin.html",
    ]

    found_admin_pages = set()
    domain_name = urlparse(base_url).netloc
    scheme = urlparse(base_url).scheme

    for path in common_admin_paths:
        url = f"{scheme}://{domain_name}/{path}"
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                content_lower = response.text.lower()
                if any(keyword in content_lower for keyword in ["login", "password", "username"]):
                    found_admin_pages.add(url)
        except requests.RequestException:
            continue

    return found_admin_pages

def print_colorful_ascii():
    ascii_art = [
        # Bisa ditambahkan ASCII art jika ingin
    ]
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA]

    for line, color in zip(ascii_art, colors):
        print(color + line + Style.RESET_ALL)

if __name__ == "__main__":

    PASSWORD = "Yetazy123"  # Ganti password sesuai keinginan Anda
    input_password = getpass.getpass("Enter password to access the script: ")

    if input_password != PASSWORD:
        print(Fore.RED + "Incorrect password. Exiting..." + Style.RESET_ALL)
        exit(1)

    print_colorful_ascii()
    print(Fore.YELLOW + "Creator: YetaHubXpoilt")
    print(Fore.YELLOW + "Github: https://github.com/yetazyyy")
    print(Fore.YELLOW + "Script creation date: 6/9/2025")
    print(Fore.RED + "Script: Extract Links |  like DH Hackbar " + Style.RESET_ALL)
    print(Fore.RED + "Note: Coming Soon = Public" + Style.RESET_ALL)
    print(Fore.YELLOW + "\nPage links | Admin Page Login\n")

    while True:
        target_url = input("Enter Website URL |  type 'Exit'  to go out : ").strip()
        if target_url.lower() in ("exit", "quit"):
            print(Fore.YELLOW + "Exit the program. Thank you | See you later" + Style.RESET_ALL)
            break

        if not target_url.startswith(("http://", "https://")):
            print(Fore.RED + "The URL must begin with http:// or https://" + Style.RESET_ALL)
            continue

        page_links = get_all_links(target_url)
        print(Fore.YELLOW + "[*] Searching for admin login pages..." + Style.RESET_ALL)
        admin_pages = find_admin_login_pages(target_url)
        print(Fore.GREEN + f"[+] Found {len(admin_pages)} admin login pages." + Style.RESET_ALL)

        print("\n---Page Links containing php?id=---")
        if page_links:
            for i, link in enumerate(sorted(page_links), 1):
                print(Fore.GREEN + f"{i}. {link}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No link found containing php?id=" + Style.RESET_ALL)

        print("\n---Admin Login Pages Found---")
        if admin_pages:
            for i, link in enumerate(sorted(admin_pages), 1):
                print(Fore.MAGENTA + f"{i}. {link}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No active admin login pages found." + Style.RESET_ALL)

        print("\n")  # Tambah baris kosong sebelum input berikut
