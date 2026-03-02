import requests
import socket
import threading
import queue
import time
import random
import os
import sys
import re
import datetime
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

class SiteTarayici:
    def __init__(self):
        self.basarili_sayisi = 0
        self.basarisiz_sayisi = 0
        self.kilit = threading.Lock()
        self.durdur = False
        
        try:
            signal.signal(signal.SIGINT, self.sinyal_handler)
            signal.signal(signal.SIGTERM, self.sinyal_handler)
        except:
            pass
    
    def sinyal_handler(self, signum, frame):
        print("\n[!] Program durduruluyor...")
        self.durdur = True
        sys.exit(0)
    
    def site_listesi_olustur(self, kategori):
        siteler = []
        
        if kategori == 1:
            siteler = [
                "rudaw.net", "rudaw.net/turkish", "rudaw.net/english",
                "anfenglish.com", "anfturkce.com", "anfkurdish.com",
                "jinhaber.com", "jinnews.com", "jinnews.net",
                "rojnews.com", "rojnews.net", "rojnews.tv",
                "hawarnews.com", "hawarnews.net", "hawarnews.org",
                "ozgurpolitika.com", "ozgurpolitika.net", "ozgurpolitika.org",
                "rojavaglobal.org", "rojavaglobal.net", "rojavaglobal.com",
                "kurdistan24.net", "kurdistan24.tv", "kurdistan24.news",
                "ekurd.net", "ekurd.org", "ekurd.tv",
                "kurdwatch.org", "kurdwatch.net", "kurdwatch.com",
                "rojhelat.info", "rojhelat.net", "rojhelat.org",
                "nud.org", "nud.net", "nud.com"
            ]
            
            for site in siteler[:]:
                siteler.append("www." + site)
            
            return siteler
            
        elif kategori == 2:
            siteler = [
                "phpinfo.me", "testphp.vulnweb.com", "testfire.net", "demo.testfire.net",
                "zero.webappsecurity.com", "juice-shop.herokuapp.com", "crackme.cf",
                "hack.me", "hackthissite.org", "hackthis.co.uk", "hack-test.com",
                "vulnweb.com", "vulnhub.com", "webscantest.com", "testasp.vulnweb.com",
                "testaspnet.vulnweb.com", "testphp.vulnweb.com", "testasp.acunetix.com",
                "testaspnet.acunetix.com", "testphp.acunetix.com", "testasp.vulnweb.com",
                "altoromutual.com", "altoromutual.net", "altoromutual.org",
                "crackthis.site", "hackthis.site", "hackme.site", "vulnsite.com",
                "webgoat.org", "webgoat.net", "webgoat.com", "webwolf.org",
                "bwapp.net", "bwapp.org", "bwapp.com", "bwapp.io",
                "dvwa.co.uk", "dvwa.net", "dvwa.org", "dvwa.com",
                "mutillidae.net", "mutillidae.org", "mutillidae.com",
                "grinch.secureserver.net", "grinch.secure.com", "grinch.vuln",
                "peruggia.net", "peruggia.org", "peruggia.com",
                "hackademic.net", "hackademic.org", "hackademic.com",
                "wackopicko.com", "wackopicko.net", "wackopicko.org",
                "nowasp.net", "nowasp.org", "nowasp.com",
                "crackme.site", "crackme.net", "crackme.org",
                "vulnlab.com", "vulnlab.net", "vulnlab.org",
                "pentestlab.net", "pentestlab.org", "pentestlab.com",
                "hacklab.net", "hacklab.org", "hacklab.com",
                "testlab.net", "testlab.org", "testlab.com",
                "vulntest.net", "vulntest.org", "vulntest.com",
                "webtest.net", "webtest.org", "webtest.com",
                "cracknet.net", "cracknet.org", "cracknet.com",
                "hacknet.net", "hacknet.org", "hacknet.com"
            ]
            return siteler
            
        elif kategori == 3:
            siteler = [
                "google.com", "youtube.com", "facebook.com", "instagram.com", "twitter.com",
                "linkedin.com", "github.com", "stackoverflow.com", "reddit.com", "amazon.com",
                "netflix.com", "spotify.com", "apple.com", "microsoft.com", "wikipedia.org",
                "yahoo.com", "bing.com", "duckduckgo.com", "telegram.org", "whatsapp.com",
                "tiktok.com", "snapchat.com", "pinterest.com", "twitch.tv", "discord.com",
                "medium.com", "quora.com", "wordpress.com", "blogger.com", "tumblr.com",
                "dropbox.com", "onedrive.com", "box.com", "mega.nz", "mediafire.com",
                "adobe.com", "oracle.com", "ibm.com", "cisco.com", "vmware.com",
                "salesforce.com", "sap.com", "dell.com", "hp.com", "lenovo.com",
                "samsung.com", "xiaomi.com", "huawei.com", "sony.com", "lg.com",
                "nike.com", "adidas.com", "puma.com", "reebok.com", "underarmour.com",
                "coca-cola.com", "pepsi.com", "starbucks.com", "mcdonalds.com", "burgerking.com",
                "tesla.com", "bmw.com", "mercedes.com", "audi.com", "volkswagen.com",
                "toyota.com", "honda.com", "nissan.com", "ford.com", "chevrolet.com",
                "citi.com", "chase.com", "wellsfargo.com", "bankofamerica.com", "hsbc.com",
                "paypal.com", "stripe.com", "square.com", "venmo.com", "cash.app",
                "airbnb.com", "booking.com", "expedia.com", "tripadvisor.com", "kayak.com",
                "uber.com", "lyft.com", "doordash.com", "grubhub.com", "postmates.com",
                "hulu.com", "hbomax.com", "disneyplus.com", "paramount.com", "peacocktv.com"
            ]
            
            return siteler
            
        elif kategori == 4:
            url = input("\n[+] Cloudflare kontrolu icin URL girin (orn: example.com): ").strip()
            url = url.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0]
            return [url]
    
    def cloudflare_kontrol(self, hedef):
        try:
            site = hedef
            if not site.startswith(('http://', 'https://')):
                site = 'https://' + site
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(site, timeout=5, headers=headers, allow_redirects=True, verify=False)
            
            cloudflare_tespit = False
            cloudflare_mesaj = ""
            
            if response.status_code == 503:
                cloudflare_tespit = True
                cloudflare_mesaj = "503 Service Unavailable - Cloudflare aktif olabilir"
            
            headers = response.headers
            server = headers.get('Server', '').lower()
            cf_ray = headers.get('CF-RAY', '')
            cf_cache = headers.get('CF-Cache-Status', '')
            
            if 'cloudflare' in server:
                cloudflare_tespit = True
                cloudflare_mesaj = "Server header'ında Cloudflare tespit edildi"
            elif cf_ray:
                cloudflare_tespit = True
                cloudflare_mesaj = "CF-RAY header'ı tespit edildi"
            elif cf_cache:
                cloudflare_tespit = True
                cloudflare_mesaj = "CF-Cache-Status header'ı tespit edildi"
            
            if "cloudflare" in response.text.lower() or "__cfduid" in response.text:
                cloudflare_tespit = True
                cloudflare_mesaj = "Sayfa içeriğinde Cloudflare izleri tespit edildi"
            
            try:
                ip = socket.gethostbyname(hedef.split('/')[0])
                
                cloudflare_ip_araliklari = [
                    "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "104.16.0.0/12",
                    "108.162.192.0/18", "131.0.72.0/22", "141.101.64.0/18", "162.158.0.0/15",
                    "172.64.0.0/13", "173.245.48.0/20", "188.114.96.0/20", "190.93.240.0/20",
                    "197.234.240.0/22", "198.41.128.0/17", "199.27.128.0/21"
                ]
                
                import ipaddress
                ip_obj = ipaddress.ip_address(ip)
                
                for aralik in cloudflare_ip_araliklari:
                    if ip_obj in ipaddress.ip_network(aralik):
                        cloudflare_tespit = True
                        cloudflare_mesaj = f"IP adresi ({ip}) Cloudflare aralığında"
                        break
                        
            except:
                ip = "Bilinmiyor"
            
            return {
                'site': hedef,
                'url': site,
                'ip': ip,
                'status': response.status_code,
                'cloudflare': cloudflare_tespit,
                'cloudflare_mesaj': cloudflare_mesaj,
                'server': headers.get('Server', 'Bilinmiyor'),
                'durum': 'Basarili'
            }
            
        except Exception as e:
            return {
                'site': hedef,
                'durum': 'Basarisiz',
                'hata': str(e)
            }
    
    def site_kontrol(self, hedef):
        try:
            site = hedef
            if not site.startswith(('http://', 'https://')):
                site = 'https://' + site
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(site, timeout=5, headers=headers, allow_redirects=True, verify=False)
            
            title = "Bulunamadı"
            try:
                title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip()[:100]
            except:
                pass
            
            server = response.headers.get('Server', 'Bilinmiyor')
            
            try:
                ip = socket.gethostbyname(hedef.split('/')[0])
            except:
                ip = "Bilinmiyor"
            
            return {
                'site': hedef,
                'url': site,
                'ip': ip,
                'status': response.status_code,
                'title': title,
                'server': server,
                'durum': 'Basarili'
            }
        except Exception as e:
            return {
                'site': hedef,
                'durum': 'Basarisiz',
                'hata': str(e)
            }
    
    def tarama_baslat(self, hedefler, thread_sayisi=50, cloudflare_modu=False):
        self.basarili_sayisi = 0
        self.basarisiz_sayisi = 0
        
        if cloudflare_modu:
            print(f"\n[+] Cloudflare taramasi baslatiliyor: {len(hedefler)} hedef")
        else:
            print(f"\n[+] Tarama baslatiliyor: {len(hedefler)} hedef")
        
        print(f"[+] Thread sayisi: {thread_sayisi}")
        print("\n" + "="*100)
        
        baslangic_zamani = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_sayisi) as executor:
            if cloudflare_modu:
                future_to_hedef = {
                    executor.submit(self.cloudflare_kontrol, hedef): hedef 
                    for hedef in hedefler
                }
            else:
                future_to_hedef = {
                    executor.submit(self.site_kontrol, hedef): hedef 
                    for hedef in hedefler
                }
            
            for idx, future in enumerate(as_completed(future_to_hedef), 1):
                if self.durdur:
                    break
                    
                try:
                    sonuc = future.result(timeout=10)
                    
                    if sonuc['durum'] == 'Basarili':
                        self.basarili_sayisi += 1
                        print(f"\n[{idx}/{len(hedefler)}] ✅ {sonuc['site']}")
                        print(f"    URL: {sonuc['url']}")
                        print(f"    IP: {sonuc['ip']}")
                        print(f"    Status: {sonuc['status']}")
                        
                        if cloudflare_modu:
                            if sonuc['cloudflare']:
                                print(f"    🔒 CLOUDFLARE: EVET - {sonuc['cloudflare_mesaj']}")
                            else:
                                print(f"    🔓 CLOUDFLARE: HAYIR")
                        
                        if not cloudflare_modu and sonuc.get('title') and sonuc['title'] != "Bulunamadı":
                            print(f"    Title: {sonuc['title']}")
                            
                        print(f"    Server: {sonuc['server']}")
                    else:
                        self.basarisiz_sayisi += 1
                        print(f"\n[{idx}/{len(hedefler)}] ❌ {sonuc['site']} - {sonuc.get('hata', 'Bilinmeyen hata')}")
                    
                except Exception as e:
                    self.basarisiz_sayisi += 1
                    print(f"\n[{idx}/{len(hedefler)}] ❌ {hedefler[idx-1]} - Zaman asimi")
        
        gecen_sure = time.time() - baslangic_zamani
        print("\n" + "="*100)
        print(f"\n[+] TARAMA TAMAMLANDI!")
        print(f"[+] Toplam sure: {gecen_sure:.2f} saniye")
        print(f"[+] Basarili: {self.basarili_sayisi}")
        print(f"[+] Basarisiz: {self.basarisiz_sayisi}")
        if len(hedefler) > 0:
            print(f"[+] Basari orani: %{(self.basarili_sayisi/len(hedefler)*100):.1f}")
        print("\n" + "="*100)

def main():
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
       

            print("""
            ██╗     ██╗   ██╗ ███╗   ██╗ █████╗ ██████╗ 
            ██║     ██║   ██║ ████╗  ██║██╔══██╗██╔══██╗
            ██║     ██║   ██║ ██╔██╗ ██║███████║██████╔╝
            ██║     ██║   ██║ ██║╚██╗██║██╔══██║██╔══██╗
            ███████╗╚██████╔╝ ██║ ╚████║██║  ██║██║  ██║
            ╚══════╝ ╚═════╝  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                       
                """)
            print("="*60)
            print("SITE TARAMA ARACI")
            print("="*60)
            print("\nLutfen bir secenek girin:")
            print("-"*40)
            print("[1] Kurt Haber Siteleri")
            print("[2] Zayif Guvenlik Testleri (Vuln siteler)")
            print("[3] Elit Siteler")
            print("[4] CloudFlare Tarama (URL gir)")
            print("[5] Cikis")
            print("-"*40)
            
            secim = input("\nSeciminiz (1-5): ").strip()
            
            if secim == "5":
                print("\n[+] Program sonlandiriliyor...")
                break
            
            if secim not in ["1", "2", "3", "4"]:
                print("\n[-] Gecersiz secim!")
                input("\nDevam etmek icin Enter'a basin...")
                continue
            
            secim = int(secim)
            
            print("\n" + "="*40)
            print("TARAMA KATEGORISI SECILDI")
            print("="*40)
            
            cloudflare_modu = False
            
            if secim == 1:
                print("[1] Kurt Haber Siteleri")
                kategori = 1
            elif secim == 2:
                print("[2] Zayif Guvenlik Testleri (Vuln siteler)")
                kategori = 2
            elif secim == 3:
                print("[3] Elit Siteler")
                kategori = 3
            elif secim == 4:
                print("[4] CloudFlare Tarama")
                kategori = 4
                cloudflare_modu = True
            
            if not cloudflare_modu:
                print("\nTarama miktari secin:")
                print("-"*40)
                print("[1] 1 Site")
                print("[2] 10 Site")
                print("[3] 100 Site")
                print("-"*40)
                
                miktar = input("\nSeciminiz (1-3): ").strip()
                
                if miktar == "1":
                    site_sayisi = 1
                elif miktar == "2":
                    site_sayisi = 10
                elif miktar == "3":
                    site_sayisi = 100
                else:
                    print("\n[-] Gecersiz secim!")
                    input("\nDevam etmek icin Enter'a basin...")
                    continue
                
                print(f"\n[+] {site_sayisi} site taranacak...")
            
            tarayici = SiteTarayici()
            
            print("\n[+] Site listesi hazirlaniyor...")
            tum_siteler = tarayici.site_listesi_olustur(kategori)
            
            if not cloudflare_modu:
                if site_sayisi <= len(tum_siteler):
                    tarama_listesi = random.sample(tum_siteler, site_sayisi)
                else:
                    tarama_listesi = tum_siteler
            else:
                tarama_listesi = tum_siteler
            
            print(f"[+] {len(tarama_listesi)} site tarama listesine eklendi")
            
            if not cloudflare_modu:
                print("\n[+] Taranacak URL'ler:")
                for idx, site in enumerate(tarama_listesi, 1):
                    print(f"    {idx}. {site}")
            
            input("\n[+] Taramaya baslamak icin Enter'a basin...")
            
            tarayici.tarama_baslat(tarama_listesi, thread_sayisi=50, cloudflare_modu=cloudflare_modu)
            
            print("\n[+] Yeni bir tarama yapmak istiyor musunuz?")
            print("-"*40)
            print("[1] Evet")
            print("[2] Hayir")
            print("-"*40)
            
            tekrar = input("\nSeciminiz (1-2): ").strip()
            if tekrar == "2":
                print("\n[+] Program sonlandiriliyor...")
                break
            
    except KeyboardInterrupt:
        print("\n\n[!] Program kullanici tarafindan durduruldu!")
        input("\nCikmak icin Enter'a basin...")
    except Exception as e:
        print(f"\n[!] Beklenmeyen hata: {e}")
        input("\nCikmak icin Enter'a basin...")

if __name__ == "__main__":
    main()