# NightVision
Vision proccessing codes for FRC 2020 by FRC 7839


Bu repo şu anda geliştirme aşamasındadır. Her sistemde çalışmama ihitmali var. Çıkan her problemi belirtmeyi unutmayın. Elimden geldiğince rookieler için anlaşılabilir yapmaya çalıştım ama ben de çok profesyonel değilim.

Görüntü işleme konusunda daha detaylı açıklamalar için https://docs.wpilib.org/en/latest/docs/software/vision-processing/raspberry-pi/index.html

  İhtiyacınız olan şeyler:
  Raspberry pi (Ben 3b+ kullanıyorum): https://market.samm.com/raspberry-pi-3-b-plus

  Raspberry pi için micro sd kart (16 gb öneririm ama 8 gb da olur): https://market.samm.com/toshiba-16-gb-micro-sdhc-hafiza-karti

  Raspberry pi için 5" ekran (Zorunlu değil): https://www.direnc.net/raspberry-5inch-hdmi-lcd-800480-waveshare?language=tr&h=13a1ff21&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gBmeehrhJSXjY6Sz5K1PcAOPMcgBhNZfwbGUMXMS1bif4VEx_g9jkAaAjwrEALw_wcB

  Raspberry pi için micro usb kablosu

  Ethernet kablosu veya wifi adaptörü

  12'li led ring (16 veya farklı sayılarda da olur) :
  https://www.f1depo.com/urun/neopixel-12li-halka

  Arduino Nano (Arduino nano, micro veya pro mini de kullanılabilir ama nano öneririm): https://www.direnc.net/arduino-nano-usb-chip-ch340-usb-kablo-dahil?language=tr&h=2ef1190d&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gC7qaeETEafGkdqWlcDeEYIMpmfsQ-50ygmyPwUwib78QWhGOusjBEaAkxyEALw_wcB

  10K'lık potansiyometre:

  Push button

  Yaklaşık 100 tane dişi header

  Lehim konusunda yetenekli olduğunuza inanıyorsanız delikli pertinaks (Biraz kablo ve lehim teli de gerekebilir): https://www.hepsiburada.com/diyotlab-4x6-cm-cift-yuzlu-delikli-pertinaks-pm-HB00000NAQUN

  Yeniyseniz breadboard ve jumper kablo: https://www.robotistan.com/orta-boy-breadboard?language=tr&h=04cbdb53&gclid=Cj0KCQiA4NTxBRDxARIsAHyp6gCfZXgLMqwqVf2fgMvt6EE4CcCSFUfkiYC35L4hbObrY0w49vFkOZgaAg25EALw_wcB https://www.robotistan.com/40-pin-ayrilabilen-erkek-erkek-m-m-jumper-kablo-200-mm?OM.zn=CategoryPage%20-%20CatTopSeller-w21&OM.zpc=11958

# Raspberry Pi'a FrcVision'ı Kurma
FrcVision, Raspberry pi için yayınlanmış ve görüntü işleme için hazırlanmış bir işletim sistemidir. İşletim sistemini Raspberry Pi'a yüklemek için Balena Etcher'ı (https://www.balena.io/etcher/) kullancağız. Eğer linux varsa dd komutunu da kullanbilirsiniz.

Öncelikle frcvision dosyasını bilgisayarınıza indirin. https://github.com/wpilibsuite/FRCVision-pi-gen/releases

Balena etcher ile: Select Image tuşuna bastıktan sonra indirdiğiniz fcrvision dosyasını seçin. Sd kartı bilgisayarınıza takın ve Select Drive kısmından Sd kartınız seçin. Son olarak Flash! tuşuna basın.

Linux üzerinde dd komudu ile: Öncelikle sd kartın /dev klasörü içinde nerede olduğunu bulmanız gerekiyor. En basit yöntem sd kartı takmadan önce lsblk komutunu girin. Sd kartı taktıktan sonra tekrar lsblk komutunu girip yeni gelen şeyleri görebilirsiniz. Burada önemli bir nokta var. Sd kartın unmounted olması gerekiyor. Bunun için umount /dev/sdX komutunu kullanabilirsiniz.dd bs=4M if=frcvision_dosyası of=sd_kart conv=fsync status=progress

# FrcVision ve Raspberry Pi'a Python Kodlarını Yükleme
Rpi'a bilgisayardan bağlanmak için onunla aynı ağ üzerinde olmamız gerekiyor. Fakat FrcVision frc sahasında robot bağlantılarında kesinti yaşanmasını önlemek için rpi'ın wifi özelliğini kapatıyor. Bu nedenle kurulum yaparken bir wifi adaptörü kullanmak kullanışlı oluyor. Fakat frc'nin gönderdiği ethernet kablosunu da kullanabilirsiniz. Rpi'ı ethernet kablosuyla bilgisayara bağlayabilirsiniz fakat bu her zaman çalışmayabilir ayrıca birkaç programın kurulumunu yapmak için internete ihtiyacımız olacak. Bu nedenle Rpi'ı ethernet kablosuyla internete bağlamanız gerekiyor. Siz de aynı ağa bağlanın. http://frcvision.local adresine gidin ve sistem üzerinde değişiklik yapabilmek için Writable butonuna basın.

Rpi'a ssh ile bağlanmak için putty kullanıyorum. https://www.putty.org/ buradan indirebilirsiniz. Hostname kısmına pi@frcvision.local yazdıktan sonra opena basın. Açılan ekranda ssh bağlantısı için şifreyi soracak. Eğer değiştirmediyseniz şifre raspberry. sudo raspi-config şifreyi değiştirmek dahil çoğu ayarı bu komut yardımıyla yapacağız.

Change User Password kullanıcı şifresini değiştiriyor. :-P

Network Options kısmında kullanışlı olabileceğni düşündüğüm tek şey wifi bölümü. Wifi bölümü de eğer bir wifi adaptörü satın almadıysanız anlamsız. Ama aldıysanız SSID kısmına ağın adını, passphrase kısmına da şifreyi yazın. AYRICA FRCVISION'IN WIFI ÖZELLİĞİNİ KAPATMASININ BİR SEBEBİ VAR, LÜTFEN YARIŞMA SIRASINDA WİFİ ADAPTÖRÜ KULLANMAYIN. Kaydettiğiniz wifi ssid ve şifrelerini cat /etc/wpa_supplicant/wpa_supplicant.conf komutuyla görüntüyleyebilir, nano /etc/wpa_supplicant/wpa_supplicant.conf komutuyla da düzenleyebilirsiniz. (nano üzerinde bir dosyayı kaydedip çıkmak için Ctrl + X , daha sonra y, daha sonra da Enter)

Boot Options kısmından Desktop / CLI bölümünü seçin ve Raspberry pi açıldığında şifre girmekle uğraşmamak için Console Autologin seçeneğini seçin.

Interfacing Options SSH

Eğer Rpi için 5"lik ekran aldıysanız /boot/config.txt dosyasında birkaç değişiklik yapmamız gerekecek. Ekranın tamamını kullanmak için /boot/config.txt dosyanın içinde   #hdmi_driver=2 kısmının altına şunları ekleyin:
  
  hdmi_group=2
  hdmi_mode=87
  hdmi_cvt 800 480 60 6 0 0 0

Bunları ekledikten sonra raspberry'yi yeniden başlatırsanız ekranın tamamını kullanabilirsiniz.

Aktif olan versiyon 2 buton 1 switch 1 led ve 1 tane de potansiyometre gerektiriyor fakat kodu baştan yazıp sadece switch ve encoder gerektirecek şekilde yazmayı düşünüyoruz. 

# Kodları Rasberry'ye Yüklemek

Öncelikle python için kurmamız gereken birkaç kütüphane var. Bu kütüphaneleri Raspberry'ye kurmak için "pip3 install -r requirements.txt" kodunu terminale girebilirsiniz. 

Kodları hem bilgisayarınıza hem de Raspberry'ye yüklemeniz gerekiyor. Raspberry'ye kurmak için "git clone https://github.com/FRC7839/NightVision" kodunu terminale girin. Windows'a yüklemek için kodalrın hemen yukarısında clone or download yazısına tıklayarak zip uzantısında sıkıştırılmış halde indirebilirsiniz.

Raspberry pi her çalıştığında arayüzün de çalışmasını sağlamak için /home/pi klasörü içinde bulunan .bashrc dosyasında değişiklik yapmamız gerekiyor. Dosyanın sonuna:
  
  sleep 10 
  python3 NightVision/InputP.py

kodlarını ekleyin. BU kodları .bashrc dosyasına eklemek her ssh bağlantısı yaptığınızda da bu programın çalışacağı anlamına geliyor. 

























  
  
