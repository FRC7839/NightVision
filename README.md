# NightVision
***Vision proccessing codes for FRC 2020 by FRC 7839***

Bu repo şu anda geliştirme aşamasındadır. Yazıyı yazma amacım her ne kadar NightVision programının kurulumunu anlatmak olsa da elimden geldiğince evrensel olmaya çalıştım ve yeni şeyler öğrenmek isteyenler için güzel bir yazı olduğunu düşünüyorum. Her sistemde çalışmama ihitmali var. Çıkan her problemi belirtmeyi unutmayın. Elimden geldiğince rookieler için anlaşılabilir yapmaya çalıştım ama ben de çok profesyonel değilim.

Görüntü işleme konusunda daha detaylı açıklamalar için https://docs.wpilib.org/en/latest/docs/software/vision-processing/raspberry-pi/index.html

  #### Gereksinimler:
  1. Elektronik Gereksinimler

    * [Raspberry Pi](https://market.samm.com/raspberry-pi-3-b-plus) (Ben 3b+ kullanıyorum) 
    
    * Microsoft Lifecam HD 3000 (Yazılım diğer web kameralar üzerinde test edilmemiştir.)

    * Raspberry Pi için [micro sd kart](https://market.samm.com/toshiba-16-gb-micro-sdhc-hafiza-karti) (16 gb öneririm ama 8 gb da olur)
    
    * [Raspberry Pi için 5" ekran](https://www.direnc.net/raspberry-5inch-hdmi-lcd-800480-waveshare?language=tr&h=13a1ff21&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gBmeehrhJSXjY6Sz5K1PcAOPMcgBhNZfwbGUMXMS1bif4VEx_g9jkAaAjwrEALw_wcB) (Arayüz kullanacaklar için)
    
    * Raspberry Pi için micro usb kablosu
    
    * Ethernet kablosu veya WiFi adaptörü
    
    * [12'li led ring](https://www.f1depo.com/urun/neopixel-12li-halka) (16 veya farklı sayılarda da olur)
    
    * [Arduino Nano](https://www.direnc.net/arduino-nano-usb-chip-ch340-usb-kablo-dahil?language=tr&h=2ef1190d&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gC7qaeETEafGkdqWlcDeEYIMpmfsQ-50ygmyPwUwib78QWhGOusjBEaAkxyEALw_wcB) (Arduino uno, micro veya pro mini ya da serial konusunda sıkıntı çıkarmayacak herhangi bir arduino da kullanılabilir ama nano öneririm)
    
    * 10K'lık potansiyometre (Arayüz kullanacaklar için)

    * 1 tane switch (Arayüz kullanacaklar için)

    * 3 tane led (Kırmızı, Yeşil ve Mavi olması önerilir ve yine arayüz kullanacaklar için)

    * 2 tane Push button (Arayüz kullanacaklar için)

    * Lehim konusunda yetenekli olduğunuza inanıyorsanız yaklaşık 100 tane dişi header ve [delikli pertinaks](https://www.hepsiburada.com/diyotlab-4x6-cm-cift-yuzlu-delikli-pertinaks-pm-HB00000NAQUN) (Biraz kablo ve lehim teli de gerekebilir)

    * Yeniyseniz [Breadboard](https://www.robotistan.com/orta-boy-breadboard?language=tr&h=04cbdb53&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gCfZXgLMqwqVf2fgMvt6EE4CcCSFUfkiYC35L4hbObrY0w49vFkOZgaAg25EALw_wcB)  ve [jumper kablo](https://www.robotistan.com/40-pin-ayrilabilen-erkek-erkek-m-m-jumper-kablo-200-mm?OM.zn=CategoryPage%20-%20CatTopSeller-w21&OM.zpc=11958)
 
  2. Yazılımsal Gereksinimler
    * [FRCVision](https://github.com/wpilibsuite/FRCVision-pi-gen/releases)
    
    * [Python 3](https://www.python.org/downloads/)
    
    * [Putty](https://www.putty.org/) (Windows üzerinde SSH bağlantısı kurmamız için gerekli program. İsteğinize göre farklı bir program da kullanabilirsiniz.)
    
    * [balenaEtcher](https://www.balena.io/etcher/) (FRCVision işletim sistemini Raspberry Pi üzerine yüklemek için gerekli olan program.)
    
    
<br>
# Raspberry Pi'a FRCVision'ı Kurma

FRCVision, Raspberry pi için yayınlanmış ve görüntü işleme için hazırlanmış bir işletim sistemidir. İşletim sistemini Raspberry Pi'a yüklemek için [Balena Etcher'ı](https://www.balena.io/etcher/) kullancağız. Eğer linux tabanlı bir işletim sistemine sahipseniz `dd` komutunu da kullanbilirsiniz.

Öncelikle frcvision dosyasını bilgisayarınıza indirin: https://github.com/wpilibsuite/FRCVision-pi-gen/releases

#### Balena etcher ile: 

  1. Select Image tuşuna bastıktan sonra indirdiğiniz fcrvision dosyasını seçin. 
  2. Sd kartı bilgisayarınıza takın ve Select Drive kısmından Sd kartınız seçin. 
  3. Son olarak <kbd>Flash!</kbd> tuşuna basın.

#### Linux üzerinde `dd` komudu ile: 

Öncelikle sd kartın `/dev` klasörü içinde nerede olduğunu bulmanız gerekiyor. En basit yöntem sd kartı takmadan önce `lsblk` komutunu girin. Sd kartı taktıktan sonra tekrar `lsblk` komutunu girip yeni gelen şeyleri görebilirsiniz. Burada önemli bir nokta var. Sd kartın unmounted olması gerekiyor. Bunun için `umount /dev/sdX` komutunu kullanabilirsiniz. Sonrasında şu komutu çalıştırınız:

```shell
dd bs=4M if=frcvision-dosyasının-konumu of=/dev/sd-kart-konumu conv=fsync status=progress
```
<br>
# FRCVision ve Raspberry Pi'a Python Kodlarını Yükleme

### Ağ bağlantısının yapılması

Rpi'a bilgisayardan bağlanmak için onunla aynı ağ üzerinde olmamız gerekiyor. Fakat FRCVision işletim sistemi FRC sahasında robot bağlantılarında kesinti yaşanmasını önlemek için raspberry'nin WiFi özelliğini kapatıyor. Bu nedenle kurulum yaparken bir WiFi adaptörü kullanmak kullanışlı oluyor. Fakat ethernet kablosu da kullanabilirsiniz. Raspberry'yi ethernet kablosuyla bilgisayara bağlayabilirsiniz fakat bu her zaman çalışmayabilir ayrıca birkaç programın kurulumunu yapmak için internete ihtiyacımız olacak. Bu nedenle Raspberry'yi ethernet kablosuyla internete bağladıktan sonra bilgisayarınızı da aynı ağa bağlayın. 

### FRCVision arayüzüne ulaşma

http://frcvision.local adresine gidin ve sistem üzerinde değişiklik yapabilmek için Writable butonuna basın. frcvision.local adresi her zaman çalışmayabilir. Aynı internet üzerinde ağ taraması yaparak ([Nmap](https://nmap.org/download.html) veya [Advanced Ip Scanner](https://www.advanced-ip-scanner.com/tr/) gibi programlarla) Raspberry'nin local ip adresini bulup direkt o ip adresini tarayıcınızın URL kısmına o ip adresini yapıştırarak düzenlemeleir yapmak için FRCVision sisteminin arayüzüne girebilirsiniz.

### SSH aracılığıyla Raspberry Pi'a bağlanma

Rpi'a SSH ile bağlanmak için [Putty](https://www.putty.org/) kullanıyorum. Hostname kısmına `pi@frcvision.local` (Eğer tarayıcınızda frcvision.local çalışmadıysa pi@tarayıcıda-kullandığınız-ip-adresi) yazdıktan sonra opena basın. Açılan ekranda SSH bağlantısı için şifreyi soracak. Varsayılan şifre `raspberry`' dir. `sudo raspi-config` komutu yardımıyla şifre değiştirme dahil çoğu işlemi gerçekleştireceğiz.

![Putty Configuration](https://i.ibb.co/m6Ccwzd/2.png)
<br>

# Raspi-config menüsü ve Kullanımı

### Change User Password 
Kullanıcı şifresini değiştirmek için sizi terminale yönlendirir. (Linux, şifreyi korumak için sizin yazdığınız karakterleri göstermiyor.)

### Network Options 
Bu bölümde kullanışlı olabileceğni düşündüğüm tek şey WiFi bölümü. WiFi bölümü de eğer bir WiFi adaptörü satın almadıysanız anlamsız. Ama aldıysanız SSID kısmına ağın adını, passphrase kısmına da şifreyi yazın.  Kaydettiğiniz WiFi ssid ve şifrelerini `cat /etc/wpa_supplicant/wpa_supplicant.conf` komutuyla görüntüyleyebilir, sistem Writeable konumundayken `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` komutuyla da düzenleyebilirsiniz. (Nano üzerinde bir dosyayı kaydedip çıkmak için <kbd>Ctrl</kbd> + <kbd>X</kbd> , daha sonra <kbd>y</kbd>, daha sonra da ,<kbd>Enter</kbd> )

&#10071; **FRCVision yazılımının WiFi özelliğini kapatmasının bir sebebi var, lütfen yarışma sırasında WiFi adaptörü kullanmayın**.

### Boot Options 
Önyükleme ayarlarının yapılacağı menüdür. Desktop / CLI bölümünü seçin ve Raspberry pi açıldığında şifre girmekle uğraşmamak için Console Autologin seçeneğini seçin.

### Interfacing Options 
Öncelikle SSH'i seçerek enable etmeniz gerekiyor. Ekran satın almadıysanız ve arayüz kullanmayacaksınız bile kamera etrafına yerleştireceğiniz ledleri açıp kapatabilmek için bir arduino kullanmanız gerekiyor. Eğer ledi kapatmayı düşünmüyorsanız Arduino ile Raspberry arasında bir iletişime ihtiyacınız olmuyor ve Serial seçeneğini etkinleştirmek de anlamsız kalıyor. Fakat arayüz yapmayı hedefliyorsanız veya ledi kapatıp açmayı istiyorsanız Serial seçeneğini etkinleştirmeniz gerekiyor.

Eğer Rpi için 5"lik ekran aldıysanız `/boot/config.txt` dosyasında birkaç değişiklik yapmamız gerekecek. Ekranın tamamını kullanmak için `/boot/config.txt` dosyanın içinde `#hdmi_driver=2` kısmının altına şunları ekleyin:
```shell
hdmi_group=2
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
```
Bunları ekledikten sonra raspberry'yi yeniden başlatırsanız ekranın tamamını kullanabilirsiniz.

# Gerekli Kodları Rasberry Pi'a Yüklemek

Öncelikle python için kurmamız gereken birkaç kütüphane var. Bu kütüphaneleri Raspberry'ye kurmak için `pip3 install -r requirements.txt` kodunu terminale girebilirsiniz. 

Kodları hem bilgisayarınıza hem de Raspberry'ye yüklemeniz gerekiyor.

 ** 1. Raspberry'ye kurmak için: ** 
```
git clone https://github.com/FRC7839/NightVision
```
 ** 2. Windows'a yüklemek için: ** 
  Kodların hemen yukarısında `Clone or Download` yazısına tıklayarak veya [buradan](https://github.com/FRC7839/NightVision/archive/test.zip) zip uzantısında sıkıştırılmış halde indirebilirsiniz.
<br>
# Arayüzün Otomatik Olarak Çalışmasını Sağlamak
Raspberry Pi her çalıştığında arayüzün de çalışmasını sağlamak için `/home/pi` klasörü içinde bulunan `.bashrc` dosyasında değişiklik yapmamız gerekiyor. Dosyanın sonuna:
  
```shell
sleep 10 
python3 NightVision/InputP.py
```

kodlarını ekleyin. Bu kodları `.bashrc` dosyasına eklemek her SSH bağlantısı yaptığınızda da bu programın çalışacağı anlamına geliyor. 
Tabii ki bu bizim istemediğimiz bir şey fakat SSH sürekli kullandığımız bir şey olmadığından çözme gereği duymadık. SSH bağlantılarını açtığınızda <kbd>Ctrl</kbd> + <kbd>c</kbd> tuşlarına basmak programın çalışmasını önleyecektir 

# Görüntü İşleme Algoritmasını Yüklemek

Görüntü işleme algoritmasını yüklemek için yukarıdaki gibi aynı internette olmanız gerekiyor. Internet tarayıcınız üzerinden http://frcvision.local adresine gidin. (**Sistem üzerinde değişiklik yapabilmek için <kbd>Writeable</kbd> özelliğini aktif ettiğinizden emin olun.**). Buranın devamını yarın okulda paylaşacağım

![Uploading Algorithm](https://i.ibb.co/B6hknnJ/1.png?v=4&s)

# Bilgisayar Testleri İçin Görüntü İşleme Algoritmasının Kullanımı (Biz bitirene kadar kullanıp test etmek çok yardımcı olabilir)

Bilgisayarda görüntü işleme algoritmasını kullanabilmek için NightVision kütüphanesini zip halinde yukarıdan indirip içindeki dosyaları çıkarmalısınız. Bizim kullanacağımız kod NightVision.py olmasına rağmen bu kod frc_lib7839.py kodundan da fonksiyon kullandığı için sadece NightVision.py kodunun yerini değiştiriseniz hata almaya başlarsınız. 

Kodu indirdikten sonra windows + r 'ye basıp çalıştırı açtıktan sonra cmd yazın ve Enter'a basın. Cmd'den NightVision dosyalarını çıkarttığınız yere geçmeniz gerekiyor.
pwd komutu aktif olarak bulunduğunuz klasörü gösterir. dir komudu o klasör içindeki dosyaları ve klasörleri gösterir. cd komutu da belirttiğiniz klasörün içine girmenizi sağlar (cd Documents gibi) eğer dir komutunu girdiğinizde cmd'nin size verdiği çıktının içinde NightVision.py ve frc_lib7839.py'yi görebiliyorsanız doğru yere gelmişsiniz demektir.

Python kodlarının çalışması için gerekli kütüphaneleri bilgisayara da kurmamız gerekiyor. py -3 -m pip install -r requirements1.txt kodunu cmd'ye girin.

Argümanlar

Programı çalıştırıken ek olarak girdiğimiz argümanlar program tarafından işleniyor. Argümanların temel kullanım şekli şu şekildedir: 

py -3 NightVision.py 
veya
py -3 NightVision.py --örnek-argüman eğer-varsa-argüman-değeri

--pc-mode (kamera-numarası) bu argüman bilgisayar için test modunu açar. Eğer laptop kullanıyorsanız kamera numarası için 0 laptopun builtin kamerasını ifade eder. Eğer ek kamera taktıysanız argüman olarak muhtemelen --pc-mode 1 girmelisiniz.

--test-image (resim-konumu) bu argüman bilgisayar için resim üzerinden test modunu açar. Eğer yüklemek istediğiniz örnek bir fotoğraf varsa fotoğrafın konumunu (resim-konumu) kısmına girerek algoritmayı test edebilirsiniz.

--team-number (takım-numarası) bu argüman radionun dağıttığı ip adreslerine dayanarak radioya bağlı olup olmadığımızı anlamak için yazılmış fonksiyonların çalışmasını sağlar. Radio'nun verilen takım numarasına göre konfigüre edilmiş olması gerekmektedir. Raspberry pi üzerinde bu argümanı giremediğimiz için bu argümanı kullanma ihtiyacınız yok.











