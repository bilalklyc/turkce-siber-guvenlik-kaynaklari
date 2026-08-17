# Katkı Rehberi 🤝

Katkılar pull request ile alınır. GitHub arayüzünden ya da terminalden — iki yol da aşağıda anlatılıyor.

## Katkı Sözleşmesi (kabul kriterleri)

Her eklenen kaynak şu 4 şartı sağlamalı:

| # | Kural | Neden |
|---|-------|-------|
| 1 | **İçerik Türkçe olmalı** | Reponun tek amacı bu: Türkçe kaynakları tek yerde toplamak |
| 2 | **Link canlı ve erişilebilir olmalı** | Ölü link ekleyen PR'lar otomatik kontrolde yakalanır |
| 3 | **Tek cümlelik somut Türkçe açıklama yazılmalı** | "Faydalı bir site" ❌ → "Web zafiyetlerini Türkçe lab'larla anlatan ücretsiz platform" ✅ |
| 4 | **Yasal içerik olmalı** | Korsan kitap PDF'i, crack'li kurs, izinsiz kopyalanmış içerik **kabul edilmez** |

> Bir kaynak birden fazla kategoriye uyuyorsa en çok uyduğu **tek** kategoriye ekle. Her alana katkı serbest — istediğin kategoriye, istediğin kadar PR atabilirsin.

> ⚙️ Rozetteki kaynak sayısını ve İçindekiler'deki kategori sayaçlarını **elle güncelleme** — her merge'den sonra otomatik yeniden hesaplanıyor. Senin tek işin tabloya satır eklemek.

## GitHub Arayüzünden (5 adım)

1. **Fork'la:** Bu sayfanın sağ üstündeki **Fork** düğmesine bas. Reponun senin hesabında bir kopyası oluşur.
2. **Düzenle:** Kendi kopyanda `README.md` dosyasını aç, kalem (✏️ **Edit**) simgesine bas.
3. **Ekle:** Kaynağını ilgili kategorinin tablosuna **en alt satır** olarak ekle. Satır formatı:
   ```
   | [Kaynak Adı](https://link) | Tek cümlelik Türkçe açıklama | Tür |
   ```
   Tür şunlardan biri: `site` `youtube` `blog` `repo` `kurs` `platform` `topluluk` `podcast` `doküman`
4. **Commit'le:** Sayfanın üstündeki **Commit changes** düğmesine bas. Mesaj olarak `kaynak: <kaynak adı> eklendi` yaz.
5. **PR aç:** GitHub sana "Contribute → Open pull request" önerecek. Aç, şablondaki kutucukları işaretle, gönder. 🎉

Takıldığın yerde komite grubunda sorabilirsin — ilk PR herkes için ilktir.

## Terminalden

```bash
git clone https://github.com/KULLANICI_ADIN/turkce-siber-guvenlik-kaynaklari.git
cd turkce-siber-guvenlik-kaynaklari
git checkout -b kaynak/yeni-kaynak-adi
# README.md'yi düzenle
git add README.md
git commit -m "kaynak: <kaynak adı> eklendi"
git push origin kaynak/yeni-kaynak-adi
# GitHub'da PR aç
```

## PR'ın nasıl değerlendirilir?

- Maintainer ekibi (İçerik Takımı) 72 saat içinde bakar.
- 4 kurala uyuyorsa merge edilir; eksik varsa yorum yazılır, düzeltip aynı PR'ı güncellersin (yeni PR açmana gerek yok).
- Otomatik link kontrolü ölü linki işaretlerse düzeltmen istenir.

## Kaynak silme / güncelleme

- Ölü link fark ettiysen PR ile silebilir ya da [🔗 Ölü Link Bildir](../../issues/new?template=olu-link.yml) issue'su açabilirsin.
- Açıklamayı iyileştiren, kategoriyi düzelten PR'lar da katkıdır.

## Davranış

Kısa ve net: saygılı ol, emeğe saygı duy, tartışmayı kaynak kalitesi üzerinden yap. Bu repo hepimizin vitrini.
