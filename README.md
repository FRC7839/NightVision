```shell
TO DO
RC.LOCAL DOSAYSININ KOMUTLARINI DÜZENLEME
STATIC IP ALIMI
FILE UPLOAD fotoğraflar 
ARAYÜZ kullanım
Network Tables ile birleştirme
.gitignore düzenleme
devreleri yenileme
```


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


# Raspberry Pi'a FRCVision'ı Kurma

FRCVision, Raspberry Pi için yayınlanmış ve görüntü işleme için hazırlanmış bir işletim sistemidir. İşletim sistemini Raspberry Pi'a yüklemek için [Balena Etcher'ı](https://www.balena.io/etcher/) kullancağız. Eğer linux tabanlı bir işletim sistemine sahipseniz `dd` komutunu da kullanbilirsiniz.

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
# FRCVision ve Raspberry Pi'a Python Kodlarını Yükleme

### Ağ bağlantısının yapılması

Raspberry Pi'a bilgisayardan bağlanmak için onunla aynı ağ üzerinde olmamız gerekiyor. Fakat FRCVision işletim sistemi FRC sahasında robot bağlantılarında kesinti yaşanmasını önlemek için raspberry'nin WiFi özelliğini kapatıyor. Bu nedenle kurulum yaparken bir WiFi adaptörü kullanmak kullanışlı oluyor. Fakat ethernet kablosu da kullanabilirsiniz. Raspberry'yi ethernet kablosuyla bilgisayara bağlayabilirsiniz fakat bu her zaman çalışmayabilir ayrıca birkaç programın kurulumunu yapmak için internete ihtiyacımız olacak. Bu nedenle Raspberry'yi ethernet kablosuyla internete bağladıktan sonra bilgisayarınızı da aynı ağa bağlayın.

### FRCVision arayüzüne ulaşma

http://frcvision.local adresine gidin ve sistem üzerinde değişiklik yapabilmek için <kbd>Writable</kbd> butonuna basın. http://frcvision.local adresi her zaman çalışmayabilir. Aynı internet üzerinde ağ taraması yaparak ([Nmap](https://nmap.org/download.html) veya [Advanced Ip Scanner](https://www.advanced-ip-scanner.com/tr/) gibi programlarla) Raspberry'nin local ip adresini bulup direkt o ip adresini tarayıcınızın URL kısmına o ip adresini yapıştırarak düzenlemeleir yapmak için FRCVision sisteminin arayüzüne girebilirsiniz.

### SSH aracılığıyla Raspberry Pi'a bağlanma

Rpi'a SSH ile bağlanmak için [Putty](https://www.putty.org/) kullanıyorum. Hostname kısmına `pi@frcvision.local` (Eğer tarayıcınızda frcvision.local çalışmadıysa pi@tarayıcıda-kullandığınız-ip-adresi) yazdıktan sonra opena basın. Açılan ekranda SSH bağlantısı için şifreyi soracak. Varsayılan şifre `raspberry`' dir. `sudo raspi-config` komutu yardımıyla şifre değiştirme dahil çoğu işlemi gerçekleştireceğiz.

![Putty Configuration](https://i.ibb.co/m6Ccwzd/2.png)

# Raspi-config menüsü ve Kullanımı

### Change User Password 
Kullanıcı şifresini değiştirmek için sizi terminale yönlendirir. (Linux, şifreyi korumak için sizin yazdığınız karakterleri göstermiyor.)

### Network Options 
Bu bölümde kullanışlı olabileceğni düşündüğüm tek şey WiFi bölümü. WiFi bölümü de eğer bir WiFi adaptörü satın almadıysanız anlamsız. Ama aldıysanız SSID kısmına ağın adını, passphrase kısmına da şifreyi yazın.  Kaydettiğiniz WiFi ssid ve şifrelerini `cat /etc/wpa_supplicant/wpa_supplicant.conf` komutuyla görüntüyleyebilir, sistem Writeable konumundayken `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` komutuyla da düzenleyebilirsiniz. (Nano üzerinde bir dosyayı kaydedip çıkmak için <kbd>Ctrl</kbd> + <kbd>X</kbd> , daha sonra <kbd>Y</kbd>, daha sonra da <kbd>Enter</kbd>)

&#10071; **FRCVision yazılımının WiFi özelliğini kapatmasının bir sebebi var, lütfen yarışma sırasında WiFi adaptörü kullanmayın**.

### Boot Options 
Önyükleme ayarlarının yapılacağı menüdür. Desktop / CLI bölümünü seçin ve Raspberry Pi açıldığında şifre girmekle uğraşmamak için Console Autologin seçeneğini seçin.

### Interfacing Options 
Öncelikle SSH'i seçerek enable etmeniz gerekiyor. Ekran satın almadıysanız ve arayüz kullanmayacaksınız bile kamera etrafına yerleştireceğiniz ledleri açıp kapatabilmek için bir arduino kullanmanız gerekiyor. Eğer ledi kapatmayı düşünmüyorsanız Arduino ile Raspberry arasında bir iletişime ihtiyacınız olmuyor ve Serial seçeneğini etkinleştirmek de anlamsız kalıyor. Fakat arayüz yapmayı hedefliyorsanız veya ledi kapatıp açmayı istiyorsanız Serial seçeneğini etkinleştirmeniz gerekiyor.

Eğer Rpi için 5"lik ekran aldıysanız `/boot/config.txt` dosyasında birkaç değişiklik yapmamız gerekecek. Ekranın tamamını kullanmak için `/boot/config.txt` dosyanın içinde `#hdmi_driver=2` kısmının altına şunları ekleyin:
```shell
hdmi_group=2
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
```
Bunları ekledikten sonra raspberry'yi yeniden başlatırsanız ekranın tamamını kullanabilirsiniz.

# Gerekli Python Librarylerinin Kurulumu

Öncelikle python için kurmamız gereken birkaç kütüphane var. Bu kütüphaneleri Raspberry'ye kurmak için `pip3 install -r requirements.txt` kodunu terminale girebilirsiniz. 

# Arayüz Kodlarını Rasberry Pi'a Yüklemek

Kodları Raspberry pi'a yüklemek içi frcvision işletim sisteminin file upload özelliğini kullanacağız.
 
 **Kodları Windows'a indirmek için:** 
 
 Kodların hemen yukarısında `Clone or Download` yazısına tıklayarak veya [buradan](https://github.com/FRC7839/NightVision/archive/test.zip) zip uzantısında sıkıştırılmış halde indirebilirsiniz.

frcvision.local adresinden file upload seçeneğini kullanarak frc_lib7839.py ve InputPlus.py dosyasını Raspberry pi'ınıza yükleyin

# Arayüzün Otomatik Olarak Çalışmasını Sağlamak
Raspberry Pi her çalıştığında arayüzün de çalışmasını sağlamak için `/home/pi` klasörü içinde bulunan `.bashrc` dosyasında değişiklik yapmamız gerekiyor. Dosyanın sonuna:
  
```shell
sleep 10 
python3 NightVision/InputP.py
```

kodlarını ekleyin. Bu kodları `.bashrc` dosyasına eklemek her SSH bağlantısı yaptığınızda da bu programın çalışacağı anlamına geliyor. 
Tabii ki bu bizim istemediğimiz bir şey fakat SSH sürekli kullandığımız bir şey olmadığından çözme gereği duymadık. SSH bağlantılarını açtığınızda <kbd>Ctrl</kbd> + <kbd>c</kbd> tuşlarına basmak programın çalışmasını önleyecektir 

Arayüz ile Kamera kodunun iletişim kurabilmesi için JSON dosyalarını kullanıyoruz. Fakat frcvision Raspberry'yi read-only modunda çalıştırıyor. Bunu önlemek için
`sudo nano /etc/rc.local` komutunu girerek rc.local dosyasında exit komutunun üstüne şu komutları ekleyelim:

```shell
echo TUNA'YI ÇOK KISKANIYORUM
```

# Görüntü İşleme Algoritmasını Yüklemek

Görüntü işleme algoritmasını yüklemek için yukarıdaki gibi aynı internette olmanız gerekiyor. Internet tarayıcınız üzerinden http://frcvision.local adresine gidin. (**Sistem üzerinde değişiklik yapabilmek için <kbd>Writeable</kbd> özelliğini aktif ettiğinizden emin olun**)

![Uploading Algorithm](https://i.ibb.co/B6hknnJ/1.png?v=4&s)

Görüntü işleme algoritması, eğer bilgisayar modu açık değilse ve işletim sistemimiz linux ise Arayüzden gelen ayarları settings.json dosyası aracılığıyla elde ederek NetworkTables yardımıyla paylaşır.  

# Bilgisayar Testleri İçin Görüntü İşleme Algoritmasının Kullanımı 
#### NOT: Biz bitirene kadar kullanıp test etmek çok yardımcı olabilir

Bilgisayarda görüntü işleme algoritmasını kullanabilmek için NightVision kütüphanesini zip halinde yukarıdan indirip içindeki dosyaları çıkarmalısınız. Bizim kullanacağımız kod `NightVision.py` olmasına rağmen bu kod `frc_lib7839.py` modülünden de fonksiyon kullandığı için sadece `NightVision.py` kodunun yerini değiştiriseniz hata almaya başlarsınız. 

Kodu indirdikten sonra <kbd>Windows</kbd> + <kbd>R</kbd> tuş kombinasyonuna basıp Çalıştır'ı açtıktan sonra `cmd` yazın ve <kbd>Enter</kbd> tuşuna basın. Açılan komut satırından NightVision dosyalarını çıkarttığınız yere geçmeniz gerekiyor. Bulunduğunuz yeri öğrenmek için `pwd` komutunu kullanabilirsiniz. Bulunduğunuz klasör içindeki dosya ve klasörleri görmek için ise `dir` komutunu kullanın. Belirttiğiniz klasörün içine girmenizi sağlayan komut ise `cd` komududur. Eğer `dir` komutunu girdiğinizde cmd'nin size verdiği çıktının içinde `NightVision.py` ve `frc_lib7839.py` dosyalarını görebiliyorsanız doğru yere gelmişsiniz demektir.

Python kodlarının çalışması için gerekli kütüphaneleri bilgisayara da kurmamız gerekiyor. Bunun için ise aşağıdaki kodları komut konsoluna (cmd) girmeniz yeterli. Eğer farklı bir python environmentı kullanıyorsanız (conda gibi) önce yüklemek istediğiniz environmente girmeyi unutmayın.

```
py -3 -m pip install -r requirements1.txt
```

### Argümanlar

Programı çalıştırıken ek olarak girdiğimiz argümanlar program tarafından işleniyor. Argümanların temel kullanım şekli şu şekildedir: 

```
py -3 NightVision.py
```

veya

```
py -3 NightVision.py --örnek-argüman eğer-varsa-argüman-değeri
```

**--pc-mode (kamera-numarası)**:

Bu argüman bilgisayar için test modunu açar. Eğer laptop kullanıyorsanız kamera numarası için 0 kullandığınız laptopun gömülü kamerasını ifade eder. Eğer ek kamera taktıysanız argüman olarak muhtemelen `--pc-mode 1` girmelisiniz.

Örnek Kullanım: `py -3 NightVision.py --pc-mode 1`

**--test-image (resim-konumu)**:

Bu argüman bilgisayar için resim üzerinden test modunu açar. Eğer yüklemek istediğiniz örnek bir fotoğraf varsa fotoğrafın konumunu (resim-konumu) kısmına girerek algoritmayı test edebilirsiniz.

Örnek Kullanım: `py -3 NightVision.py --test-image "C:/Users/blackshadow/Pictures/1.jpg"`

**--team-number (takım-numarası)**:

Bu argüman modemin dağıttığı ip adreslerine dayanarak modeme bağlı olup olmadığımızı anlamak için yazılmış fonksiyonların çalışmasını sağlar. Modemin verilen takım numarasına göre konfigüre edilmiş olması gerekmektedir. Raspberry Pi üzerinde bu argümanı giremediğimiz için bu argümanı kullanma ihtiyacınız yok. Arayüz kullanan kişiler bu ayarı "SETTINGS" menüsünden yapabilirler

Örnek Kullanım: `py -3 NightVision.py --team-number "7839"`

# InputPlus.py Arayüzünün Kullanımı

`InputPlus.py`, robotun maçtaki konumunu, kameranın hata toleransını, otonom modunu, diğer robotlarla çarpışmamak için bekleme süresini, takım numarasını ve eğer kullanıyorsanız uzaklık sensörü ile kamera arasındaki farkı Roborio'ya networktables yardımıyla göndermek için hazırlanmış bir yazılımdır. Eğer tüm ayarlar doğru yapılmışsa arayüzün Raspberry üzerinde otomatik olaraak başlaması gerekmektedir. 

&#10071; **Modeminize doğru bir şekilde bağlandığınız halde `Not Connected To Radio` hatası alıyorsanız SETTINGS menüsünden takım numaranızı, modeminizi konfigüre ederken girdiğinizle aynı şekilde girdiğinize emin olun**

# Roborio Üzerinden NetworkTables ile Verilerin Alınması

NetworkTables genel olarak **Python-Roborio-SmartDashboard** haberleşmesi üzerine yazılmış kullanımı kolay bir modüldür. NightVision yazılımında Roborio'ya veriler NetworkTables ile gönderilmektedir. Ancak bu verilerin Roborio üzerinden yakalanabilmesi için bazı ayarların yapılması gerekmekte. Basit bir otonom uygulaması ile bu ayarların nasıl yapılması gerektiğini anlatacağım.

```Java
package edu.wpi.first.wpilibj.templates;

import edu.wpi.first.wpilij.TimedRobot;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;

public class NetworkTablesOrnegi extends TimedRobot {

    NetworkTable table = inst.getTable("imgProc");

    NetworkTableEntry robotLocation;
    NetworkTableEntry cameraTolerance;
    NetworkTableEntry waitingPeriod;
    NetworkTableEntry autonomousMode;
    NetworkTableEntry yError;
    NetworkTableEntry cam_offset;        
                                                     

    public void robotInit() {
        NetworkTableInstance inst = NetworkTableInstance.getDefault();

        NetworkTable table = inst.getTable("imgProc");

        private final DifferentialDrive robotDrive = new DifferentialDrive(new PWMVictorSPX(kLeftMotorPort), new PWMVictorSPX(kRightMotorPort));
    }

    public void teleopPeriodic() {
    }
                                                     
    public void autonomousPeriodic() {        
    }
                                                     
    public void autonomousInit() {
    }
                                                     
    public void autonomousPeriodic() {
        cameraTolerance = visionTable.getEntry("Cam Tol");
        yError = visionTable.getEntry("yerror");
                                          
        if (!yError.contains("NF")) {
            i_yError = Integer.parseInt(yError);
            i_camTol = Integer.parseInt(camTol);

            double max_speed = 60;
            double min_speed = 45;

            double left_cur_turn = ((i_yError - i_camTol) * (max_speed - min_speed) / (320 - i_camTol) + min_speed) / -100;
            double right_cur_turn = ((i_yError + i_camTol) * (max_speed - min_speed) / (-320 + i_camTol) + min_speed) / 100;

            if (i_yError >= i_camTol) {
                robotDrive.arcadeDrive(0, left_cur_turn); // Hedef solda 
            }

            else if (i_yError <= -i_camTol) { 
                robotDrive.arcadeDrive(0, right_cur_turn); // Hedef sağda
            }
        
            else {
                robotDrive.arcadeDrive(0, 0); // Hedef ortalandı
            }
        }
    
        else { // Hedef bulunamadı
          robotDrive.arcadeDrive(0, .6);
        }
    }
}
```
