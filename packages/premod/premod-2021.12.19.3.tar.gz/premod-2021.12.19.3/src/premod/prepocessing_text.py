def case_folding(dataset):
    #list tampungan data akhir
    tampungan_data_akhir = []
    for i in range(len(dataset)):
        #membaca tiap row
        tampungan = dataset[i]
        #case Folding
        tampungan = tampungan.lower()
        #menyimpan ke bentuk list
        tampungan_data_akhir.append(tampungan)
    return tampungan_data_akhir

def cleansing(dataset):
    import re        
    pun = '\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^\\_\\`\\{\\|\\}\\~'
    #list tampungan data akhir
    tampungan_data_akhir = []
    
    #dataset = dataset.str.replace(r'\b\w\b','').str.replace(r'\s+', ' ')    
    for i in range(len(dataset)):
        #membaca tiap row + cleansing   
        tampungan = dataset[i].replace('\\n',' ')        
        tampungan = re.sub("b'", '', tampungan)
        tampungan = re.sub('https?://\S+|www\.\S+', ' ', tampungan)
        tampungan = re.sub('@[a-z0-9]+', ' ', tampungan)    
        tampungan = re.sub('<.*?>+', ' ', tampungan)        
        tampungan = re.sub('\w*\d\w*', ' ', tampungan)
        tampungan = re.sub("#[a-z0-9]+","",tampungan)
        #tampungan = re.sub('[^a-z]', ' ', tampungan)        
        tampungan = re.sub('[%s]' % re.escape(pun), ' ', tampungan)
        tampungan = re.sub(' +', ' ', tampungan)
        tampungan = tampungan.strip()
        tampungan_data_akhir.append(tampungan)
    
    return tampungan_data_akhir

def replace_value(dataset_kamus, dataset):
    import re
    dataset_kamus = dataset_kamus.applymap(str)
    dataset_kamus["kumpulan kata"] = dataset_kamus.loc[:,'kata 1':].agg(','.join, axis=1)
    dataset_kamus["kumpulan kata"] = dataset_kamus['kumpulan kata'].str.replace(',nan' , '')
    
    tampungan_data_akhir_kamus=[]
    for index, row in dataset_kamus.iterrows(): 
        tampungan = row['kumpulan kata'].split(",")
        tampungan_data_akhir_kamus.append((row['baku'], tampungan))
    
    tampungan_data_akhir = []
    for i in range(len(dataset)):
        tampungan = dataset[i]                
        d={ k : "\\b(?:" + "|".join(v) + ")\\b" for k,v in tampungan_data_akhir_kamus}
        for k,r in d.items(): tampungan = re.sub(r, k, tampungan)  
        tampungan = tampungan.split()
        tampungan = ' '.join(tampungan)
        tampungan_data_akhir.append(tampungan)
    return tampungan_data_akhir

def tokinize_stemmer_stopwords(dataset):
    tampungan_data_akhir = []
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory    
    for i in range(len(dataset)):
        #Tokinize
        tampungan = dataset[i].split()
        #Stopword + Stemming
        stemmer = StemmerFactory().create_stemmer()        
        tampungan = [stemmer.stem(word) for word in tampungan if not word in set(stopwords.words('indonesian'))]
        tampungan = ' '.join(tampungan)
        tampungan_data_akhir.append(tampungan)
    return tampungan_data_akhir