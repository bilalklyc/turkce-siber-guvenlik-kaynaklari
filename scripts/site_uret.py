#!/usr/bin/env python3
"""README.md'deki kaynak tablolarından docs/ altındaki siteyi üretir.

Kaynak gerçeği (source of truth) README.md'dir: katkıcılar yalnızca README'ye
PR atar; bu script her merge'de siteyi, llms.txt'yi ve kaynak sayacını günceller.
Çalıştır: python3 scripts/site_uret.py
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
README = KOK / "README.md"
DOCS = KOK / "docs"
SITE_URL = "https://fevziegeyurtsevenler.github.io/turkce-siber-guvenlik-kaynaklari"
REPO_URL = "https://github.com/fevziegeyurtsevenler/turkce-siber-guvenlik-kaynaklari"

BASLIK_RE = re.compile(r"^## (\S+) (.+?)\s*$")
SATIR_RE = re.compile(r"^\|\s*\[(.+?)\]\((\S+?)\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


def readme_ayristir(metin: str):
    """README'den [(emoji, kategori, açıklama, [kaynak,...]), ...] çıkarır."""
    kategoriler = []
    aktif = None
    for satir in metin.splitlines():
        b = BASLIK_RE.match(satir)
        if b:
            emoji, ad = b.group(1), b.group(2)
            if ad.lower().startswith(("katkı", "lisans", "içindekiler")):
                aktif = None
                continue
            aktif = {"emoji": emoji, "ad": ad, "tanim": "", "kaynaklar": []}
            kategoriler.append(aktif)
            continue
        if aktif is None:
            continue
        if satir.startswith("> ") and not aktif["kaynaklar"]:
            aktif["tanim"] = (aktif["tanim"] + " " + satir[2:].strip()).strip()
            continue
        s = SATIR_RE.match(satir)
        if s:
            baslik, url, aciklama, tur = s.groups()
            if baslik.strip().lower() == "kaynak":
                continue
            aktif["kaynaklar"].append(
                {"baslik": baslik.strip(), "url": url.strip(),
                 "aciklama": aciklama.strip(), "tur": tur.strip().lower()}
            )
    return [k for k in kategoriler if k["kaynaklar"]]


def sayac_guncelle(metin: str, toplam: int) -> str:
    return re.sub(
        r"kaynak-\d+-1C2957",
        f"kaynak-{toplam}-1C2957",
        metin,
    )


def kart(k):
    tur = html.escape(k["tur"])
    return (
        f'<a class="kart" href="{html.escape(k["url"])}" target="_blank" rel="noopener">'
        f'<div class="kart-ust"><h3>{html.escape(k["baslik"])}</h3>'
        f'<span class="tur tur-{tur}">{tur}</span></div>'
        f'<p>{html.escape(k["aciklama"])}</p>'
        f'<span class="git">ziyaret et →</span></a>'
    )


def uret():
    metin = README.read_text(encoding="utf-8")
    kategoriler = readme_ayristir(metin)
    toplam = sum(len(k["kaynaklar"]) for k in kategoriler)
    if toplam == 0:
        sys.exit("HATA: README'den hiç kaynak ayrıştırılamadı; tablo formatı bozulmuş olabilir.")

    README.write_text(sayac_guncelle(metin, toplam), encoding="utf-8")

    # ---- kategori bölümleri ----
    bolumler, cipler = [], []
    for i, kat in enumerate(kategoriler):
        kid = f"kat-{i}"
        cipler.append(
            f'<button class="cip" data-hedef="{kid}">{kat["emoji"]} '
            f'{html.escape(kat["ad"])} <b>{len(kat["kaynaklar"])}</b></button>'
        )
        kartlar = "\n".join(kart(k) for k in kat["kaynaklar"])
        bolumler.append(
            f'<section class="kategori" id="{kid}">'
            f'<h2>{kat["emoji"]} {html.escape(kat["ad"])}</h2>'
            f'<p class="kat-tanim">{html.escape(kat["tanim"])}</p>'
            f'<div class="izgara">{kartlar}</div></section>'
        )

    # ---- JSON-LD (GEO) ----
    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Türkçe Siber Güvenlik Kaynakları",
        "description": "Türkçe siber güvenlik kaynaklarının topluluk eliyle derlenen, doğrulanmış ve kategorilenmiş dizini.",
        "url": SITE_URL,
        "inLanguage": "tr",
        "dateModified": date.today().isoformat(),
        "publisher": {"@type": "Organization", "name": "TÜGA Siber Güvenlik Komitesi"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": toplam,
            "itemListElement": [
                {"@type": "ListItem", "position": p + 1,
                 "name": k["baslik"], "url": k["url"], "description": k["aciklama"]}
                for p, k in enumerate(x for kat in kategoriler for x in kat["kaynaklar"])
            ],
        },
    }

    sablon = (DOCS / "sablon.html").read_text(encoding="utf-8")
    sayfa = (
        sablon
        .replace("@@TOPLAM@@", str(toplam))
        .replace("@@KATEGORI_SAYI@@", str(len(kategoriler)))
        .replace("@@CIPLER@@", "\n".join(cipler))
        .replace("@@BOLUMLER@@", "\n".join(bolumler))
        .replace("@@JSONLD@@", json.dumps(jsonld, ensure_ascii=False))
        .replace("@@TARIH@@", date.today().strftime("%d.%m.%Y"))
    )
    (DOCS / "index.html").write_text(sayfa, encoding="utf-8")

    # ---- llms.txt + llms-full.txt (GEO) ----
    llms = [
        "# Türkçe Siber Güvenlik Kaynakları",
        "",
        "> Türkçe siber güvenlik kaynaklarının topluluk eliyle derlenen, doğrulanmış dizini. "
        "TÜGA Siber Güvenlik Komitesi yürütür; her kaynak eklemeden önce canlılık ve Türkçe içerik "
        "kontrolünden geçer.",
        "",
        f"- Site: {SITE_URL}",
        f"- Repo: {REPO_URL}",
        f"- Kaynak sayısı: {toplam} | Kategori: {len(kategoriler)}",
        "",
        "## Kategoriler",
    ]
    llms += [f"- {k['emoji']} {k['ad']} ({len(k['kaynaklar'])} kaynak)" for k in kategoriler]
    (DOCS / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

    tam = ["# Türkçe Siber Güvenlik Kaynakları — tam liste", ""]
    for kat in kategoriler:
        tam.append(f"## {kat['emoji']} {kat['ad']}")
        tam += [f"- [{k['baslik']}]({k['url']}) — {k['aciklama']}" for k in kat["kaynaklar"]]
        tam.append("")
    (DOCS / "llms-full.txt").write_text("\n".join(tam), encoding="utf-8")

    # ---- sitemap ----
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}/</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )

    print(f"OK: {toplam} kaynak, {len(kategoriler)} kategori → docs/ güncellendi")


if __name__ == "__main__":
    uret()
