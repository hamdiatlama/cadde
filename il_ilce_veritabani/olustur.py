import json, csv, os

BASE = os.path.dirname(__file__)

ILLER = [
    # (il_adi, plaka, telefon_kodu, bolge, nufus_milyon)
    ("Adana", "01", "322", "Akdeniz", 2.27),
    ("Adıyaman", "02", "416", "Güneydoğu", 0.63),
    ("Afyonkarahisar", "03", "272", "Ege", 0.75),
    ("Ağrı", "04", "472", "Doğu", 0.52),
    ("Amasya", "05", "358", "Karadeniz", 0.34),
    ("Ankara", "06", "312", "İç Anadolu", 5.80),
    ("Antalya", "07", "242", "Akdeniz", 2.69),
    ("Artvin", "08", "466", "Karadeniz", 0.17),
    ("Aydın", "09", "256", "Ege", 1.15),
    ("Balıkesir", "10", "266", "Marmara", 1.27),
    ("Bilecik", "11", "228", "Marmara", 0.22),
    ("Bingöl", "12", "426", "Doğu", 0.29),
    ("Bitlis", "13", "434", "Doğu", 0.35),
    ("Bolu", "14", "374", "Karadeniz", 0.32),
    ("Burdur", "15", "248", "Akdeniz", 0.27),
    ("Bursa", "16", "224", "Marmara", 3.15),
    ("Çanakkale", "17", "286", "Marmara", 0.56),
    ("Çankırı", "18", "376", "İç Anadolu", 0.20),
    ("Çorum", "19", "364", "Karadeniz", 0.53),
    ("Denizli", "20", "258", "Ege", 1.06),
    ("Diyarbakır", "21", "412", "Güneydoğu", 1.82),
    ("Edirne", "22", "284", "Marmara", 0.42),
    ("Elazığ", "23", "424", "Doğu", 0.60),
    ("Erzincan", "24", "446", "Doğu", 0.24),
    ("Erzurum", "25", "442", "Doğu", 0.75),
    ("Eskişehir", "26", "222", "İç Anadolu", 0.91),
    ("Gaziantep", "27", "342", "Güneydoğu", 2.15),
    ("Giresun", "28", "454", "Karadeniz", 0.46),
    ("Gümüşhane", "29", "456", "Karadeniz", 0.15),
    ("Hakkari", "30", "438", "Doğu", 0.28),
    ("Hatay", "31", "326", "Akdeniz", 1.69),
    ("Isparta", "32", "246", "Akdeniz", 0.45),
    ("Mersin", "33", "324", "Akdeniz", 1.93),
    ("İstanbul", "34", "212/216", "Marmara", 15.66),
    ("İzmir", "35", "232", "Ege", 4.48),
    ("Kars", "36", "474", "Doğu", 0.28),
    ("Kastamonu", "37", "366", "Karadeniz", 0.38),
    ("Kayseri", "38", "352", "İç Anadolu", 1.44),
    ("Kırklareli", "39", "288", "Marmara", 0.37),
    ("Kırşehir", "40", "386", "İç Anadolu", 0.24),
    ("Kocaeli", "41", "262", "Marmara", 2.06),
    ("Konya", "42", "332", "İç Anadolu", 2.30),
    ("Kütahya", "43", "274", "Ege", 0.58),
    ("Malatya", "44", "422", "Doğu", 0.81),
    ("Manisa", "45", "236", "Ege", 1.46),
    ("Kahramanmaraş", "46", "344", "Akdeniz", 1.19),
    ("Mardin", "47", "482", "Güneydoğu", 0.87),
    ("Muğla", "48", "252", "Ege", 1.07),
    ("Muş", "49", "436", "Doğu", 0.40),
    ("Nevşehir", "50", "384", "İç Anadolu", 0.31),
    ("Niğde", "51", "388", "İç Anadolu", 0.37),
    ("Ordu", "52", "452", "Karadeniz", 0.77),
    ("Rize", "53", "464", "Karadeniz", 0.35),
    ("Sakarya", "54", "264", "Marmara", 1.08),
    ("Samsun", "55", "362", "Karadeniz", 1.38),
    ("Siirt", "56", "484", "Güneydoğu", 0.34),
    ("Sinop", "57", "368", "Karadeniz", 0.22),
    ("Sivas", "58", "346", "İç Anadolu", 0.64),
    ("Tekirdağ", "59", "282", "Marmara", 1.17),
    ("Tokat", "60", "356", "Karadeniz", 0.61),
    ("Trabzon", "61", "462", "Karadeniz", 0.82),
    ("Tunceli", "62", "428", "Doğu", 0.08),
    ("Şanlıurfa", "63", "414", "Güneydoğu", 2.21),
    ("Uşak", "64", "276", "Ege", 0.38),
    ("Van", "65", "432", "Doğu", 1.15),
    ("Yozgat", "66", "354", "İç Anadolu", 0.42),
    ("Zonguldak", "67", "372", "Karadeniz", 0.59),
    ("Aksaray", "68", "382", "İç Anadolu", 0.43),
    ("Bayburt", "69", "458", "Karadeniz", 0.09),
    ("Karaman", "70", "338", "İç Anadolu", 0.26),
    ("Kırıkkale", "71", "318", "İç Anadolu", 0.28),
    ("Batman", "72", "488", "Güneydoğu", 0.63),
    ("Şırnak", "73", "486", "Güneydoğu", 0.56),
    ("Bartın", "74", "378", "Karadeniz", 0.20),
    ("Ardahan", "75", "478", "Doğu", 0.10),
    ("Iğdır", "76", "476", "Doğu", 0.20),
    ("Yalova", "77", "226", "Marmara", 0.30),
    ("Karabük", "78", "370", "Karadeniz", 0.25),
    ("Kilis", "79", "348", "Güneydoğu", 0.15),
    ("Osmaniye", "80", "328", "Akdeniz", 0.56),
    ("Düzce", "81", "380", "Karadeniz", 0.40),
]

ILCELER = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu", "Karaisalı", "Karataş", "Kozan", "Pozantı", "Saimbeyli", "Sarıçam", "Seyhan", "Tufanbeyli", "Yumurtalık", "Yüreğir"],
    "Adıyaman": ["Besni", "Çelikhan", "Gerger", "Gölbaşı", "Kâhta", "Merkez", "Samsat", "Sincik", "Tut"],
    "Afyonkarahisar": ["Başmakçı", "Bayat", "Bolvadin", "Çay", "Çobanlar", "Dazkırı", "Dinar", "Emirdağ", "Evciler", "Hocalar", "İhsaniye", "İscehisar", "Kızılören", "Merkez", "Sandıklı", "Sinanpaşa", "Sultandağı", "Şuhut"],
    "Ağrı": ["Diyadin", "Doğubayazıt", "Eleşkirt", "Hamur", "Merkez", "Patnos", "Taşlıçay", "Tutak"],
    "Amasya": ["Göynücek", "Gümüşhacıköy", "Hamamözü", "Merkez", "Merzifon", "Suluova", "Taşova"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı", "Güdül", "Haymana", "Kahramankazan", "Kalecik", "Keçiören", "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar", "Sincan", "Şereflikoçhisar", "Yenimahalle"],
    "Antalya": ["Akseki", "Aksu", "Alanya", "Demre", "Döşemealtı", "Elmalı", "Finike", "Gazipaşa", "Gündoğmuş", "İbradı", "Kaş", "Kemer", "Kepez", "Konyaaltı", "Korkuteli", "Kumluca", "Manavgat", "Muratpaşa", "Serik"],
    "Artvin": ["Ardanuç", "Arhavi", "Borçka", "Hopa", "Kemalpaşa", "Merkez", "Murgul", "Şavşat", "Yusufeli"],
    "Aydın": ["Bozdoğan", "Buharkent", "Çine", "Didim", "Efeler", "Germencik", "İncirliova", "Karacasu", "Karpuzlu", "Koçarlı", "Köşk", "Kuşadası", "Kuyucak", "Nazilli", "Söke", "Sultanhisar", "Yenipazar"],
    "Balıkesir": ["Altıeylül", "Ayvalık", "Balya", "Bandırma", "Bigadiç", "Burhaniye", "Dursunbey", "Edremit", "Erdek", "Gömeç", "Gönen", "Havran", "İvrindi", "Karesi", "Kepsut", "Manyas", "Marmara", "Savaştepe", "Sındırgı", "Susurluk"],
    "Bilecik": ["Bozüyük", "Gölpazarı", "İnhisar", "Merkez", "Osmaneli", "Pazaryeri", "Söğüt", "Yenipazar"],
    "Bingöl": ["Adaklı", "Genç", "Karlıova", "Kiğı", "Merkez", "Solhan", "Yayladere", "Yedisu"],
    "Bitlis": ["Adilcevaz", "Ahlat", "Güroymak", "Hizan", "Merkez", "Mutki", "Tatvan"],
    "Bolu": ["Dörtdivan", "Gerede", "Göynük", "Kıbrıscık", "Mengen", "Merkez", "Mudurnu", "Seben", "Yeniçağa"],
    "Burdur": ["Ağlasun", "Altınyayla", "Bucak", "Çavdır", "Çeltikçi", "Gölhisar", "Karamanlı", "Kemer", "Merkez", "Tefenni", "Yeşilova"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik", "Karacabey", "Keles", "Kestel", "Mudanya", "Mustafakemalpaşa", "Nilüfer", "Orhaneli", "Orhangazi", "Osmangazi", "Yenişehir", "Yıldırım"],
    "Çanakkale": ["Ayvacık", "Bayramiç", "Biga", "Bozcaada", "Çan", "Eceabat", "Ezine", "Gelibolu", "Gökçeada", "Lapseki", "Merkez", "Yenice"],
    "Çankırı": ["Atkaracalar", "Bayramören", "Çerkeş", "Eldivan", "Ilgaz", "Kızılırmak", "Korgun", "Kurşunlu", "Merkez", "Orta", "Şabanözü", "Yapraklı"],
    "Çorum": ["Alaca", "Bayat", "Boğazkale", "Dodurga", "İskilip", "Kargı", "Laçin", "Mecitözü", "Merkez", "Oğuzlar", "Ortaköy", "Osmancık", "Sungurlu", "Uğurludağ"],
    "Denizli": ["Acıpayam", "Babadağ", "Baklan", "Bekilli", "Beyağaç", "Bozkurt", "Buldan", "Çal", "Çameli", "Çardak", "Çivril", "Güney", "Honaz", "Kale", "Merkezefendi", "Pamukkale", "Sarayköy", "Serinhisar", "Tavas"],
    "Diyarbakır": ["Bağlar", "Bismil", "Çermik", "Çınar", "Çüngüş", "Dicle", "Eğil", "Ergani", "Hani", "Hazro", "Kayapınar", "Kocaköy", "Kulp", "Lice", "Silvan", "Sur", "Yenişehir"],
    "Edirne": ["Enez", "Havsa", "İpsala", "Keşan", "Lalapaşa", "Meriç", "Merkez", "Süloğlu", "Uzunköprü"],
    "Elazığ": ["Ağın", "Alacakaya", "Arıcak", "Baskil", "Karakoçan", "Keban", "Kovancılar", "Maden", "Merkez", "Palu", "Sivrice"],
    "Erzincan": ["Çayırlı", "İliç", "Kemah", "Kemaliye", "Merkez", "Otlukbeli", "Refahiye", "Tercan", "Üzümlü"],
    "Erzurum": ["Aşkale", "Aziziye", "Çat", "Hınıs", "Horasan", "İspir", "Karaçoban", "Karayazı", "Köprüköy", "Narman", "Oltu", "Olur", "Palandöken", "Pasinler", "Pazaryolu", "Şenkaya", "Tekman", "Tortum", "Uzundere", "Yakutiye"],
    "Eskişehir": ["Alpu", "Beylikova", "Çifteler", "Günyüzü", "Han", "İnönü", "Mahmudiye", "Mihalgazi", "Mihalıççık", "Odunpazarı", "Sarıcakaya", "Seyitgazi", "Sivrihisar", "Tepebaşı"],
    "Gaziantep": ["Araban", "İslahiye", "Karkamış", "Nizip", "Nurdağı", "Oğuzeli", "Şahinbey", "Şehitkamil", "Yavuzeli"],
    "Giresun": ["Alucra", "Bulancak", "Çamoluk", "Çanakçı", "Dereli", "Doğankent", "Espiye", "Eynesil", "Görele", "Güce", "Keşap", "Merkez", "Piraziz", "Şebinkarahisar", "Tirebolu", "Yağlıdere"],
    "Gümüşhane": ["Kelkit", "Köse", "Kürtün", "Merkez", "Şiran", "Torul"],
    "Hakkari": ["Çukurca", "Derecik", "Merkez", "Şemdinli", "Yüksekova"],
    "Hatay": ["Altınözü", "Antakya", "Arsuz", "Belen", "Defne", "Dörtyol", "Erzin", "Hassa", "İskenderun", "Kırıkhan", "Kumlu", "Payas", "Reyhanlı", "Samandağ", "Yayladağı"],
    "Isparta": ["Aksu", "Atabey", "Eğirdir", "Gelendost", "Gönen", "Keçiborlu", "Merkez", "Senirkent", "Sütçüler", "Şarkikaraağaç", "Uluborlu", "Yalvaç", "Yenişarbademli"],
    "Mersin": ["Akdeniz", "Anamur", "Aydıncık", "Bozyazı", "Çamlıyayla", "Erdemli", "Gülnar", "Mezitli", "Mut", "Silifke", "Tarsus", "Toroslar", "Yenişehir"],
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ", "Bornova", "Buca", "Çeşme", "Çiğli", "Dikili", "Foça", "Gaziemir", "Güzelbahçe", "Karabağlar", "Karaburun", "Karşıyaka", "Kemalpaşa", "Kınık", "Kiraz", "Konak", "Menderes", "Menemen", "Narlıdere", "Ödemiş", "Seferihisar", "Selçuk", "Tire", "Torbalı", "Urla"],
    "Kars": ["Akyaka", "Arpaçay", "Digor", "Kağızman", "Merkez", "Sarıkamış", "Selim", "Susuz"],
    "Kastamonu": ["Abana", "Ağlı", "Araç", "Azdavay", "Bozkurt", "Cide", "Çatalzeytin", "Daday", "Devrekani", "Doğanyurt", "Hanönü", "İhsangazi", "İnebolu", "Küre", "Merkez", "Pınarbaşı", "Şenpazar", "Seydiler", "Taşköprü", "Tosya"],
    "Kayseri": ["Akkışla", "Bünyan", "Develi", "Felahiye", "Hacılar", "İncesu", "Kocasinan", "Melikgazi", "Özvatan", "Pınarbaşı", "Sarıoğlan", "Sarız", "Talas", "Tomarza", "Yahyalı", "Yeşilhisar"],
    "Kırklareli": ["Babaeski", "Demirköy", "Kofçaz", "Lüleburgaz", "Merkez", "Pehlivanköy", "Pınarhisar", "Vize"],
    "Kırşehir": ["Akçakent", "Akpınar", "Boztepe", "Çiçekdağı", "Kaman", "Merkez", "Mucur"],
    "Kocaeli": ["Başiskele", "Çayırova", "Darıca", "Derince", "Dilovası", "Gebze", "Gölcük", "İzmit", "Kandıra", "Karamürsel", "Kartepe", "Körfez"],
    "Konya": ["Ahırlı", "Akören", "Akşehir", "Altınekin", "Beyşehir", "Bozkır", "Cihanbeyli", "Çeltik", "Çumra", "Derbent", "Derebucak", "Doğanhisar", "Emirgazi", "Ereğli", "Güneysınır", "Hadim", "Halkapınar", "Hüyük", "Ilgın", "Kadınhanı", "Karapınar", "Karatay", "Kulu", "Meram", "Sarayönü", "Selçuklu", "Seydişehir", "Taşkent", "Tuzlukçu", "Yalıhüyük", "Yunak"],
    "Kütahya": ["Altıntaş", "Aslanapa", "Çavdarhisar", "Domaniç", "Dumlupınar", "Emet", "Gediz", "Hisarcık", "Merkez", "Pazarlar", "Simav", "Şaphane", "Tavşanlı"],
    "Malatya": ["Akçadağ", "Arapgir", "Arguvan", "Battalgazi", "Darende", "Doğanşehir", "Doğanyol", "Hekimhan", "Kale", "Kuluncak", "Pütürge", "Yazıhan", "Yeşilyurt"],
    "Manisa": ["Ahmetli", "Akhisar", "Alaşehir", "Demirci", "Gölmarmara", "Gördes", "Kırkağaç", "Köprübaşı", "Kula", "Salihli", "Sarıgöl", "Saruhanlı", "Selendi", "Soma", "Şehzadeler", "Turgutlu", "Yunusemre"],
    "Kahramanmaraş": ["Afşin", "Andırın", "Çağlayancerit", "Dulkadiroğlu", "Ekinözü", "Elbistan", "Göksun", "Nurhak", "Onikişubat", "Pazarcık", "Türkoğlu"],
    "Mardin": ["Artuklu", "Dargeçit", "Derik", "Kızıltepe", "Mazıdağı", "Midyat", "Nusaybin", "Ömerli", "Savur", "Yeşilli"],
    "Muğla": ["Bodrum", "Dalaman", "Datça", "Fethiye", "Kavaklıdere", "Köyceğiz", "Marmaris", "Menteşe", "Milas", "Ortaca", "Seydikemer", "Ula", "Yatağan"],
    "Muş": ["Bulanık", "Hasköy", "Korkut", "Malazgirt", "Merkez", "Varto"],
    "Nevşehir": ["Acıgöl", "Avanos", "Derinkuyu", "Gülşehir", "Hacıbektaş", "Kozaklı", "Merkez", "Ürgüp"],
    "Niğde": ["Altunhisar", "Bor", "Çamardı", "Çiftlik", "Merkez", "Ulukışla"],
    "Ordu": ["Akkuş", "Altınordu", "Aybastı", "Çamaş", "Çatalpınar", "Çaybaşı", "Fatsa", "Gölköy", "Gülyalı", "Gürgentepe", "İkizce", "Kabadüz", "Kabataş", "Korgan", "Kumru", "Mesudiye", "Perşembe", "Ulubey", "Ünye"],
    "Rize": ["Ardeşen", "Çamlıhemşin", "Çayeli", "Derepazarı", "Fındıklı", "Güneysu", "Hemşin", "İkizdere", "İyidere", "Kalkandere", "Merkez", "Pazar"],
    "Sakarya": ["Adapazarı", "Akyazı", "Arifiye", "Erenler", "Ferizli", "Geyve", "Hendek", "Karapürçek", "Karasu", "Kaynarca", "Kocaali", "Pamukova", "Sapanca", "Serdivan", "Söğütlü", "Taraklı"],
    "Samsun": ["19 Mayıs", "Alaçam", "Asarcık", "Atakum", "Ayvacık", "Bafra", "Canik", "Çarşamba", "Havza", "İlkadım", "Kavak", "Ladik", "Salıpazarı", "Tekkeköy", "Terme", "Vezirköprü", "Yakakent"],
    "Siirt": ["Baykan", "Eruh", "Kurtalan", "Merkez", "Pervari", "Şirvan", "Tillo"],
    "Sinop": ["Ayancık", "Boyabat", "Dikmen", "Durağan", "Erfelek", "Gerze", "Merkez", "Saraydüzü", "Türkeli"],
    "Sivas": ["Akıncılar", "Altınyayla", "Divriği", "Doğanşar", "Gemerek", "Gölova", "Gürün", "Hafik", "İmranlı", "Kangal", "Koyulhisar", "Merkez", "Suşehri", "Şarkışla", "Ulaş", "Yıldızeli", "Zara"],
    "Tekirdağ": ["Çerkezköy", "Çorlu", "Ergene", "Hayrabolu", "Kapaklı", "Malkara", "Marmara Ereğlisi", "Muratlı", "Saray", "Süleymanpaşa", "Şarköy"],
    "Tokat": ["Almus", "Artova", "Başçiftlik", "Erbaa", "Merkez", "Niksar", "Pazar", "Reşadiye", "Sulusaray", "Turhal", "Yeşilyurt", "Zile"],
    "Trabzon": ["Akçaabat", "Araklı", "Arsin", "Beşikdüzü", "Çarşıbaşı", "Çaykara", "Dernekpazarı", "Düzköy", "Hayrat", "Köprübaşı", "Maçka", "Of", "Ortahisar", "Sürmene", "Şalpazarı", "Tonya", "Vakfıkebir", "Yomra"],
    "Tunceli": ["Çemişgezek", "Hozat", "Mazgirt", "Merkez", "Nazımiye", "Ovacık", "Pertek", "Pülümür"],
    "Şanlıurfa": ["Akçakale", "Birecik", "Bozova", "Ceylanpınar", "Eyyübiye", "Halfeti", "Haliliye", "Harran", "Hilvan", "Karaköprü", "Siverek", "Suruç", "Viranşehir"],
    "Uşak": ["Banaz", "Eşme", "Karahallı", "Merkez", "Sivaslı", "Ulubey"],
    "Van": ["Bahçesaray", "Başkale", "Çaldıran", "Çatak", "Edremit", "Erciş", "Gevaş", "Gürpınar", "İpekyolu", "Muradiye", "Özalp", "Saray", "Tuşba"],
    "Yozgat": ["Akdağmadeni", "Aydıncık", "Boğazlıyan", "Çandır", "Çayıralan", "Çekerek", "Kadışehri", "Merkez", "Saraykent", "Sarıkaya", "Sorgun", "Şefaatli", "Yenifakılı", "Yerköy"],
    "Zonguldak": ["Alaplı", "Çaycuma", "Devrek", "Ereğli", "Gökçebey", "Kilimli", "Kozlu", "Merkez"],
    "Aksaray": ["Ağaçören", "Eskil", "Gülağaç", "Güzelyurt", "Merkez", "Ortaköy", "Sarıyahşi", "Sultanhanı"],
    "Bayburt": ["Aydıntepe", "Demirözü", "Merkez"],
    "Karaman": ["Ayrancı", "Başyayla", "Ermenek", "Kazımkarabekir", "Merkez", "Sarıveliler"],
    "Kırıkkale": ["Bahşılı", "Balışeyh", "Çelebi", "Delice", "Karakeçili", "Keskin", "Merkez", "Sulakyurt", "Yahşihan"],
    "Batman": ["Beşiri", "Gercüş", "Hasankeyf", "Kozluk", "Merkez", "Sason"],
    "Şırnak": ["Beytüşşebap", "Cizre", "Güçlükonak", "İdil", "Merkez", "Silopi", "Uludere"],
    "Bartın": ["Amasra", "Kurucaşile", "Merkez", "Ulus"],
    "Ardahan": ["Çıldır", "Damal", "Göle", "Hanak", "Merkez", "Posof"],
    "Iğdır": ["Aralık", "Karakoyunlu", "Merkez", "Tuzluca"],
    "Yalova": ["Altınova", "Armutlu", "Çınarcık", "Çiftlikköy", "Merkez", "Termal"],
    "Karabük": ["Eflani", "Eskipazar", "Merkez", "Ovacık", "Safranbolu", "Yenice"],
    "Kilis": ["Elbeyli", "Merkez", "Musabeyli", "Polateli"],
    "Osmaniye": ["Bahçe", "Düziçi", "Hasanbeyli", "Kadirli", "Merkez", "Sumbas", "Toprakkale"],
    "Düzce": ["Akçakoca", "Cumayeri", "Çilimli", "Gölyaka", "Gümüşova", "Kaynaşlı", "Merkez", "Yığılca"],
}

SEMTLER = {
    "İstanbul": {
        "Fatih": ["Aksaray", "Alemdar", "Balat", "Çarşamba", "Eminönü", "Fener", "Haliç", "Kadırga", "Kocamustafapaşa", "Kumkapı", "Laleli", "Saraçhane", "Sultanahmet", "Tahtakale", "Topkapı", "Vatan", "Yedikule", "Zeyrek"],
        "Kadıköy": ["Bostancı", "Caferağa", "Caddebostan", "Eğitim", "Fenerbahçe", "Fikirtepe", "Göztepe", "Hasanpaşa", "Koşuyolu", "Küçükyalı", "Merdivenköy", "Moda", "Osmanağa", "Rasimpaşa", "Sahrayıcedit", "Suadiye", "Zühtüpaşa"],
        "Beşiktaş": ["Abbasağa", "Akaretler", "Arnavutköy", "Bebek", "Dikilitaş", "Etiler", "Gayrettepe", "Konaklar", "Kuruçeşme", "Levent", "Levazım", "Ortaköy", "Rumelihisarı", "Türkali", "Ulus", "Vişnezade", "Yıldız"],
        "Şişli": ["Bomonti", "Çağlayan", "Cumhuriyet", "Duatepe", "Esentepe", "Fulya", "Gülbağ", "Halaskargazi", "Harbiye", "Kuştepe", "Mecidiyeköy", "Merkez", "Nişantaşı", "Okmeydanı", "Pangaltı", "Teşvikiye"],
        "Üsküdar": ["Acıbadem", "Altunizade", "Bağlarbaşı", "Beylerbeyi", "Bulgurlu", "Burhaniye", "Çengelköy", "Ferah", "Güzeltepe", "İcadiye", "Kandilli", "Kısıklı", "Küçüksu", "Kuleli", "Kuzguncuk", "Muratreis", "Salacak", "Sultantepe", "Ünalan", "Valide-i Atik", "Zeynep Kamil"],
        "Beyoğlu": ["Asmalımescit", "Ayvansaray", "Balıkpazarı", "Bülbül", "Cihangir", "Çukurcuma", "Fındıklı", "Galata", "Gümüşsuyu", "Hacıahmet", "İstiklal", "Kalyoncu", "Kasımpaşa", "Kuledibi", "Küçük Piyale", "Okmeydanı", "Piyalepaşa", "Sütlüce", "Taksim", "Tarlabaşı", "Tepebaşı"],
        "Maltepe": ["Aydınevler", "Bağlarbaşı", "Cevizli", "Çınar", "Esenkent", "Feyzullah", "Fındıklı", "Girne", "Gülensu", "Gülsuyu", "İdealtepe", "Küçükyalı", "Maltepe", "Rızapaşa", "Yalı", "Zümrütevler"],
        "Kartal": ["Atalar", "Cevizli", "Cumhuriyet", "Çavuşoğlu", "Esentepe", "Gümüşpınar", "Hürriyet", "Karlıktepe", "Kordonboyu", "Orhantepe", "Petrol İş", "Soğanlık", "Topselvi", "Uğur Mumcu", "Yakacık", "Yalı"],
        "Pendik": ["Ahmet Yesevi", "Bahçelievler", "Batı", "Çamçeşme", "Çınardere", "Doğu", "Dumlupınar", "Ertuğrulgazi", "Güllübağlar", "Harmantepe", "Kaynarca", "Kurtköy", "Orhangazi", "Orta", "Ramazanoğlu", "Sanayi", "Sapanbağları", "Sümer", "Velibaba", "Yeni", "Yeşilbağlar"],
        "Bağcılar": ["Bağcılar", "Çiftehavuzlar", "Demirkapı", "Evren", "Fatih", "Fevzi Çakmak", "Göztepe", "Güneşli", "Hürriyet", "İnönü", "Kazım Karabekir", "Kemalpaşa", "Kirazlı", "Mahmutbey", "Merkez", "Sancaktepe", "Yavuz Selim", "Yenimahalle"],
        "Küçükçekmece": ["Atakent", "Atatürk", "Cennet", "Cumhuriyet", "Fatih", "Fevzi Çakmak", "Gültepe", "Halkalı", "İnönü", "İstasyon", "Kanarya", "Kartaltepe", "Kemalpaşa", "Mehmet Akif", "Söğütlüçeşme", "Sultanmurat", "Tevfikbey", "Yarımburgaz", "Yeni Mahalle"],
        "Esenler": ["Birlik", "Çiftehavuzlar", "Davutpaşa", "Fatih", "Fevzi Çakmak", "Güneşli", "Havaalanı", "Kazım Karabekir", "Kemer", "Menderes", "Mimarsinan", "Namık Kemal", "Oruçreis", "Tuna", "Turgutreis", "Yavuz Selim"],
        "Ümraniye": ["Adem Yavuz", "Altınşehir", "Armağanevler", "Aşağı Dudullu", "Atakent", "Atatürk", "Cemil Meriç", "Çakmak", "Çamlık", "Dudullu", "Dumlupınar", "Elmalıkent", "Esenkent", "Esentepe", "Fatih", "Fevzi Çakmak", "Haldun Alagaş", "Hekimbaşı", "İhsaniye", "İnkılap", "İstiklal", "Kâzım Karabekir", "Madenler", "Mehmet Akif", "Moralar", "Namık Kemal", "Parseller", "Saray", "Site", "Tatlısu", "Tepeüstü", "Yamanevler", "Yenişehir"],
        "Sarıyer": ["Ayazağa", "Bahçeköy", "Baltalimanı", "Büyükdere", "Çayırbaşı", "Darüşşafaka", "Demirciköy", "Emirgan", "Ferahevler", "Garipçe", "Gümüşdere", "Huzur", "İstinye", "Kazım Karabekir", "Kireçburnu", "Kısırkaya", "Maden", "Maslak", "Pınar", "Poligon", "Reşitpaşa", "Rumelifeneri", "Rumelihisarı", "Sarıyer", "Tarabya", "Yenimahalle", "Yeniköy"],
        "Avcılar": ["Ambarlı", "Cihangir", "Denizköşkler", "Firuzköy", "Gümüşpala", "Merkez", "Mustafa Kemal Paşa", "Tahtakale", "Üniversite", "Yeşilkent"],
    },
    "Ankara": {
        "Çankaya": ["Ahlatlıbel", "Aile", "Alacaatlı", "Aşağı Ayrancı", "Aşağı Öveçler", "Aşıkpaşa", "Aydınlar", "Ayrancı", "Aziziye", "Bakanlıklar", "Balımağara", "Barbaros", "Beşevler", "Bilkent", "Cebeci", "Çayyolu", "Çiğdem", "Dikmen", "Emeğiyenimahalle", "Emek", "Eryaman", "Gaziosmanpaşa", "Gökçek", "Güvenevler", "Harbiye", "Havuzbaşı", "Hilal", "İncesu", "İşçi Blokları", "Karakusunlar", "Kavaklıdere", "Keklikpınarı", "Kırkkonaklar", "Kızılay", "Kocatepe", "Konutkent", "Küçükesat", "Maltepe", "Mebusevleri", "Mimar Sinan", "Mutlukent", "Namık Kemal", "Oran", "Öveçler", "Remzi Oğuz Arık", "Saimekadın", "Sancar", "Sögütözü", "Sokullu", "Tandoğan", "Topraklık", "Üniversiteler", "Yıldızevler", "Yukarı Ayrancı", "Yukarı Bahçelievler", "Yukarı Dikmen", "Yüzüncüyıl", "Zafertepe"],
        "Keçiören": ["Akşemsettin", "Andaç", "Atapark", "Ayvalı", "Basınevleri", "Çaldıran", "Çiçekli", "Esertepe", "Etlik", "Güçlükaya", "Gümüşdere", "Güzelyurt", "Hasköy", "İncirli", "Kalaba", "Kavacık", "Kuyubaşı", "Pınarbaşı", "Sanatoryum", "Şefkat", "Şenlik", "Tepebaşı", "Ufuktepe", "Yakacık", "Yayla"],
        "Yenimahalle": ["Anadolu", "Ata", "Aziziye", "Batıkent", "Beştepe", "Boğaziçi", "Çamlıca", "Demetevler", "Elvankent", "Eryaman", "Gayret", "Göztepe", "Gülbağı", "Güventepe", "İlkyerleşim", "İnönü", "İstasyon", "Karşıyaka", "Kavaklı", "Karakusunlar", "Kentkoop", "Mehmet Akif Ersoy", "Mete Kutalmış", "Mimar Sinan", "Mutlu", "Ostim", "Pamuklar", "Ragıp Tüzün", "Şentepe", "Turgut Özal", "Uğur Mumcu", "Yeni Batı", "Yenişehir", "Yeşilevler", "Yurtçu", "Yücetepe"],
        "Altındağ": ["Akköprü", "Altınpark", "Aydıncık", "Beşikkaya", "Çamlık", "Dışkapı", "Doğantepe", "Doğu", "Feridun Çelik", "Gülpınar", "Güneşevler", "Hacı Bayram", "Hıdırlıktepe", "İskitler", "Karacaören", "Karapürçek", "Kavaklı", "Kazım Karabekir", "Köyler", "Önder", "Sakarya", "Samanpazarı", "Sıhhiye", "Solmaz", "Seyranbağları", "Telsizler", "Ulubey", "Ulus", "Yıldırım Beyazıt", "Ziraat"],
        "Mamak": ["Abidinpaşa", "Akdere", "Aktepe", "Altıağaç", "Başak", "Battalgazi", "Bilir", "Boztepe", "Cebeci", "Çiğiltepe", "Demirlibahçe", "Derbent", "Dostlar", "Durali Alıç", "Dutluk", "Ege", "Ekin", "Fahri Korutürk", "General Zeki Doğan", "Gökçeyurt", "Gülden", "Harman", "Hüseyin Gazi", "Karaağaç", "Kartaltepe", "Kayaş", "Kazım Orbay", "Kutlu", "Küçükkayaş", "Lalahan", "Misket", "Müderrisler", "Orgeneral Vecihi Akın", "Pekin", "Saimekadın", "Şafaktepe", "Şahapgürler", "Şehit Cengiz", "Şehit Hüseyin Aslan", "Siteler", "Şura", "Tuzluçayır", "Üreğil", "Yapracık", "Yenimahalle", "Yeşil Bayır", "Yeşiltepe", "Yukarı İmamoğlu"],
    },
    "İzmir": {
        "Konak": ["Alsancak", "Balçova", "Basmane", "Çankaya", "Eşrefpaşa", "Göztepe", "Güzelyalı", "Hatay", "Kahramanlar", "Kalkış", "Karantina", "Karataş", "Konak", "Kubilay", "Kültür", "Mersinli", "Montrö", "Pasaport", "Selimiye", "Umurbey", "Yenişehir", "Yeşildere"],
        "Karşıyaka": ["Alaybey", "Atakent", "Ataköy", "Bahriye Üçok", "Bostanlı", "Cumhuriyet", "Çarşı", "Çiğli", "Demirköprü", "Donanmacı", "Fikri Altay", "Goncalar", "İmbatlı", "İnönü", "Kalebodur", "Köşk", "Mavişehir", "Mustafa Kemal", "Nergiz", "Örnekköy", "Sancaklı", "Semikler", "Suna", "Şemikler", "Tuna", "Yalı", "Yamanlar", "Zübeyde Hanım"],
        "Bornova": ["Altındağ", "Atatürk", "Barbaros", "Beşyol", "Birlik", "Çamdibi", "Çamkule", "Çiçekli", "Doğanlar", "Egemenlik", "Ege Mahallesi", "Ergene", "Evka 3", "Evka 4", "Gazi Osman Paşa", "Gökdere", "Gürpınar", "Işıklar", "Kazımdirik", "Kemalpaşa", "Kızılay", "Koşukavak", "Merkez", "Mevlana", "Mimar Sinan", "Naldöken", "Pınarbaşı", "Rafet Paşa", "Sarnıç", "Serintepe", "Tuna", "Uğur Mumcu", "Yeşilova", "Yıldırım Beyazıt", "Zafer"],
        "Buca": ["Adatepe", "Akıncılar", "Atatürk", "Baran", "Buca Koop", "Çamlık", "Çamlıkule", "Cumhuriyet", "Doğu", "Dumlupınar", "Efeler", "Fırat", "Gazi", "Göksu", "Güven", "Hacıbayramlar", "Halkapınar", "İnkılap", "İsmet İnönü", "Karaburun", "Karanfil", "Kaynaklar", "Kırıklar", "Kızılçullu", "Kuruçeşme", "Lale", "Menderes", "Mimar Sinan", "Mustafa Kemal", "Oğuzhan", "Pınarbaşı", "Sebze Hali", "Şirinyer", "Ufuk", "Vali Rahmi Bey", "Yenigün", "Yıldız"],
        "Çiğli": ["Ataşehir", "Atatürk", "Çiğli", "Egekent", "Evka 2", "Güzeltepe", "Harmandalı", "İnönü", "Kaklıç", "Köyiçi", "Küçük Çiğli", "Maltepe", "Sasallı", "Şirintepe", "Yahya Kemal", "Yeni Mahalle"],
    },
    "Bursa": {
        "Nilüfer": ["Ataevler", "Bağlarbaşı", "Barış", "Beşevler", "Çalı", "Çamlıca", "Dumlupınar", "Ertuğrul", "Esentepe", "Fethiye", "Görükle", "İhsaniye", "İzmir", "Karaman", "Konak", "Kültür", "Küçükbalıklı", "Maksem", "Mimar Sinan", "Nilüfer", "Odunluk", "Özlüce", "Süleyman Orhan", "Üçevler", "Yüzüncüyıl"],
        "Osmangazi": ["Adalet", "Ahmet Yesevi", "Akkay", "Akpınar", "Alemdar", "Altınova", "Anaç", "Arabayatağı", "Atıcılar", "Çarşı", "Demirtaş", "Dikkaldırım", "Elmasbahçeler", "Emek", "Ertuğrulgazi", "Gaziakdemir", "Hacı İlyas", "Hacı Sevim", "Hamitler", "Hürriyet", "İnkaya", "Kanal", "Karaman", "Kiremitçi", "Kükürtlü", "Maksem", "Mollaarap", "Ovaakça", "Panayır", "Reşatpaşa", "Santral Garaj", "Seçköy", "Selimiye", "Sıracevizler", "Süleyman Çelebi", "Şahin", "Şehabettinpaşa", "Tayakadın", "Tuzpazarı", "Yiğitler", "Zafer"],
        "Yıldırım": ["Akkavak", "Arapzade", "Asmalı", "Bakır", "Çınar", "Çınardibi", "Davutdede", "Değirmenönü", "Eğitim", "Emirsultan", "Eşeyenilme", "Gedik", "Gülbahçe", "Hacivat", "Karamazak", "Kazım Karabekir", "Kocabay", "Kurtoğlu", "Mimarsinan", "Nalbantoğlu", "Orhangazi", "Otosansit", "Piremir", "Samanköy", "Selçukbey", "Sıracevizler", "Sözandı", "Şeyh Edebali", "Teferrüç", "Ulus", "Vilayet", "Yavuz Selim", "Yenimahalle", "Yıldırım"],
    },
}

def main():
    os.makedirs(os.path.join(BASE, "illere_gore"), exist_ok=True)

    # 1. Iller
    iller_list = []
    for i, (ad, plaka, tel, bolge, nufus) in enumerate(ILLER, 1):
        iller_list.append({
            "id": i,
            "ad": ad,
            "plaka": plaka,
            "telefon_kodu": tel,
            "bolge": bolge,
            "nufus": nufus,
            "slug": ad.lower().replace(" ", "-").replace("ç","c").replace("ğ","g").replace("ı","i").replace("ö","o").replace("ş","s").replace("ü","u").replace("î","i"),
        })
    with open(os.path.join(BASE, "iller.json"), "w", encoding="utf-8") as f:
        json.dump(iller_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(BASE, "iller.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id","ad","plaka","telefon_kodu","bolge","nufus","slug"])
        w.writeheader()
        w.writerows(iller_list)
    print(f"  [OK] {len(iller_list)} il yazıldı")

    # 2. Ilceler
    plaka_map = {ad: plaka for ad, plaka, _, _, _ in ILLER}
    il_map = {ad: i+1 for i, (ad, *_) in enumerate(ILLER)}
    ilceler_list = []
    for il_adi, ilceler in sorted(ILCELER.items()):
        il_id = il_map.get(il_adi)
        plaka = plaka_map.get(il_adi)
        for ic in ilceler:
            ilceler_list.append({
                "il_id": il_id,
                "il": il_adi,
                "plaka": plaka,
                "ilce": ic,
                "slug": ic.lower().replace(" ", "-").replace("ç","c").replace("ğ","g").replace("ı","i").replace("ö","o").replace("ş","s").replace("ü","u"),
            })
    with open(os.path.join(BASE, "ilceler.json"), "w", encoding="utf-8") as f:
        json.dump(ilceler_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(BASE, "ilceler.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["il_id","il","plaka","ilce","slug"])
        w.writeheader()
        w.writerows(ilceler_list)
    print(f"  [OK] {len(ilceler_list)} ilçe yazıldı")

    # 3. Semtler (sadece büyük şehirler için)
    semtler_list = []
    for il_adi, ilceler_dict in SEMTLER.items():
        il_id = il_map.get(il_adi)
        plaka = plaka_map.get(il_adi)
        for ilce_adi, semtler in ilceler_dict.items():
            for s in semtler:
                semtler_list.append({
                    "il_id": il_id,
                    "il": il_adi,
                    "plaka": plaka,
                    "ilce": ilce_adi,
                    "semt": s,
                    "slug": s.lower().replace(" ", "-").replace("ç","c").replace("ğ","g").replace("ı","i").replace("ö","o").replace("ş","s").replace("ü","u"),
                })
    with open(os.path.join(BASE, "semtler.json"), "w", encoding="utf-8") as f:
        json.dump(semtler_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(BASE, "semtler.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["il_id","il","plaka","ilce","semt","slug"])
        w.writeheader()
        w.writerows(semtler_list)
    print(f"  [OK] {len(semtler_list)} semt yazıldı")

    # 4. Il'ere göre ayrı JSON
    for il_adi in sorted(ILCELER.keys()):
        il_id = il_map.get(il_adi)
        plaka = plaka_map.get(il_adi)
        ilce_data = [{"ilce": ic} for ic in sorted(ILCELER[il_adi])]
        out = {"il_id": il_id, "il": il_adi, "plaka": plaka, "ilceler": ilce_data}
        fn = il_adi.lower().replace(" ", "-").replace("ç","c").replace("ğ","g").replace("ı","i").replace("ö","o").replace("ş","s").replace("ü","u")
        with open(os.path.join(BASE, "illere_gore", f"{fn}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  [OK] {len(ILCELER)} il için illere_gore/ dosyaları")

    # 5. SQL insert
    with open(os.path.join(BASE, "iller.sql"), "w", encoding="utf-8") as f:
        f.write("-- İller\n")
        for il in iller_list:
            f.write(f"INSERT INTO iller (id, ad, plaka, telefon_kodu, bolge) VALUES ({il['id']}, '{il['ad']}', '{il['plaka']}', '{il['telefon_kodu']}', '{il['bolge']}');\n")
        f.write(f"\n-- {len(ilceler_list)} ilçe\n")
        for ic in ilceler_list:
            f.write(f"INSERT INTO ilceler (il_id, ilce) VALUES ({ic['il_id']}, '{ic['ilce']}');\n")
    print(f"  [OK] SQL insert dosyası")

if __name__ == "__main__":
    main()
    print("\n=== TAMAMLANDI ===")
