from re import sub
from re import findall
import html2text
import string

half_space_char = '\u200c'
punctuations = string.punctuation + "؛»«،؟"


def removeSpecialHtmlAttributes(text):
    results = findall(r"href\s*=\s*\"[^\"]*\"", text)  # Remove href = " ".
    for token in results:
        text = text.replace(token, "")

    results = findall(r"src\s*=\s*\"[^\"]*\"", text)  # Remove src = " ".
    for token in results:
        text = text.replace(token, "")
    return text


def convertToPlainText(text):
    text = removeSpecialHtmlAttributes(text)
    text = html2text.html2text(text)
    return text


def normalize(text):
    text = convertToPlainText(text)
    text = half_space_correction(space_correction(match_alpha(text))).strip()
    text = detachPunctuations(text)
    return text


def detachPunctuations(text):
    for char in punctuations:
        if char != '\\' and char != '^':
            text = sub("[" + char + "]", " " + char + " ", text)
    text = sub(r"\\", " \\ ", text)
    text = sub(r"\^", " ^ ", text)
    text = sub("[ ][ ]+", " ", text)
    return text


def match_alpha(text):
    aftery = sub("ء", "ئ", text)
    aftera = sub(r"[ٲٱإﺍأ]", r"ا", aftery)
    abfterb = sub(r"[ﺐﺏﺑ]", r"ب", aftera)
    afterp = sub(r"[ﭖﭗﭙﺒﭘ]", r"پ", abfterb)
    aftert = sub(r"[ﭡٺٹﭞٿټﺕﺗﺖﺘ]", r"ت", afterp)
    afterc = sub(r"[ﺙﺛ]", r"ث", aftert)
    afterj = sub(r"[ﺝڃﺠﺟ]", r"ج", afterc)
    afterch = sub(r"[ڃﭽﭼ]", r"چ", afterj)
    afterh = sub(r"[ﺢﺤڅځﺣ]", r"ح", afterch)
    afterkh = sub(r"[ﺥﺦﺨﺧ]", r"خ", afterh)
    afterd = sub(r"[ڏډﺪﺩ]", r"د", afterkh)
    afterz = sub(r"[ﺫﺬﻧ]", r"ذ", afterd)
    afterr = sub(r"[ڙڗڒڑڕﺭﺮ]", r"ر", afterz)
    afterzi = sub(r"[ﺰﺯ]", r"ز", afterr)
    afterzh = sub(r"ﮊ", r"ژ", afterzi)
    aftersin = sub(r"[ݭݜﺱﺲښﺴﺳ]", r"س", afterzh)
    aftersh = sub(r"[ﺵﺶﺸﺷ]", r"ش", aftersin)
    aftersad = sub(r"[ﺺﺼﺻ]", r"ص", aftersh)
    afterzad = sub(r"[ﺽﺾﺿﻀ]", r"ض", aftersad)
    afterta = sub(r"[ﻁﻂﻃﻄ]", r"ط", afterzad)
    afterza = sub(r"[ﻆﻇﻈ]", r"ظ", afterta)
    afterein = sub(r"[ڠﻉﻊﻋ]", r"ع", afterza)
    afterghein = sub(r"[ﻎۼﻍﻐﻏ]", r"غ", afterein)
    afterf = sub(r"[ﻒﻑﻔﻓ]", r"ف", afterghein)
    afterghaf = sub(r"[ﻕڤﻖﻗ]", r"ق", afterf)
    afterkaf = sub(r"[ڭﻚﮎﻜﮏګﻛﮑﮐڪك]", r"ک", afterghaf)
    aftergaf = sub(r"[ﮚﮒﮓﮕﮔ]", r"گ", afterkaf)
    afterlam = sub(r"[ﻝﻞﻠڵ]", r"ل", aftergaf)
    aftermim = sub(r"[ﻡﻤﻢﻣ]", r"م", afterlam)
    afternun = sub(r"[ڼﻦﻥﻨ]", r"ن", aftermim)
    aftervav = sub(r"[ވﯙۈۋﺆۊۇۏۅۉﻭﻮؤ]", r"و", afternun)
    afterhe = sub(r"[ﺔﻬھﻩﻫﻪۀەةہ]", r"ه", aftervav)
    afterye = sub(r"[ﭛﻯۍﻰﻱﻲںﻳﻴﯼېﯽﯾﯿێےىي]", r"ی", afterhe)
    afternot = sub(r'¬', r'‌', afterye)
    afterdot = sub(r'[•·●·・∙｡ⴰ]', r'.', afternot)
    aftercomma = sub(r'[,٬٫‚，]', r'،', afterdot)
    afterqu = sub(r'ʕ', r'؟', aftercomma)
    afterzero = sub(r'[۰٠]', r'0', afterqu)
    nc1 = sub(r'[۱١]', r'1', afterzero)
    nc2 = sub(r'[۲٢]', r'2', nc1)
    ec1 = sub(r'ـ|ِ|ُ|َ|ٍ|ٌ|ً|', r'', nc2)
    Sc1 = sub(r'( )+', r' ', ec1)
    final = sub(r'(\n)+', r'\n', Sc1)
    return final


def space_correction(doc_string):   # space to half space
    mi_nemi = sub(r'^(بی|می|نمی)( )', r'\1‌', doc_string)
    c0 = sub(r'( )(می|نمی|بی)( )', r'\1\2‌', mi_nemi)
    c1 = sub(r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین'
             r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )', r'‌\2\3', c0)
    c2 = sub(r'( )(شده|نشده)( )', r'‌\2‌', c1)
    c3 = sub(r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|آوری|سازی|'
             r'بندی|کننده|کنندگان|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|پذیری'
             r'|پذیر|پذیران|گر|ریز|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )?', r'‌\2\3 ', c2)
    return c3


def read_file(path):
    maplist = {}
    with open(path, 'r', encoding='utf-8') as f:
        file_lines = f.readlines()
        for pair in file_lines:
            split_pair = pair.split(' ')
            try:
                maplist[split_pair[0].strip()] = sub('\n', '', split_pair[1].strip())
            except:
                continue
    return maplist


def half_space_correction(text):   # adds space
    mapped_dic1 = read_file('Resources/Normalizer/no_space1.txt')
    output_txt1 = ''
    split_text = text.split(' ')
    for word in split_text:
        if word in mapped_dic1:
            output_txt1 = output_txt1 + ' ' + mapped_dic1[word]
        else:
            output_txt1 = output_txt1 + ' ' + word

    mapped_dic2 = read_file('Resources/Normalizer/no_space2.txt')
    output_txt2 = ''
    splitted_text2 = output_txt1.split(' ')
    cnt = 1
    for i in range(0, len(splitted_text2) - 1):
        w = splitted_text2[i] + splitted_text2[i + 1]
        if w in mapped_dic2:
            output_txt2 = output_txt2 + ' ' + mapped_dic2[w]
            cnt = 0
        else:
            if cnt == 1:
                output_txt2 = output_txt2 + ' ' + splitted_text2[i]
            cnt = 1
    if cnt == 1:
        output_txt2 = output_txt2 + ' ' + splitted_text2[i + 1]

    mapped_dic3 = read_file('Resources/Normalizer/no_space3.txt')
    output_txt3 = ''
    splitted_text3 = output_txt2.split(' ')
    cnt = 1
    cnt2 = 0
    for i in range(0, len(splitted_text3) - 2):
        w = splitted_text3[i] + splitted_text3[i + 1] + splitted_text3[i + 2]
        try:
            output_txt3 = output_txt3 + ' ' + mapped_dic3[w]
            cnt = 0
            cnt2 = 2
        except KeyError:
            if cnt == 1 and cnt2 == 0:
                output_txt3 = output_txt3 + ' ' + splitted_text3[i]
            else:
                cnt2 -= 1
            cnt = 1
    if cnt == 1 and cnt2 == 0:
        output_txt3 = output_txt3 + ' ' + splitted_text3[i + 1] + ' ' + splitted_text3[i + 2]
    elif cnt == 1 and cnt2 == 1:
        output_txt3 = output_txt3 + ' ' + splitted_text3[i + 2]
    return output_txt3


# print(normalize("دنیای اقتصاد نوشت: شاخص کل بورس تهران در معاملات شنبه مسیر صعودی خود را با شتاب پیمود. رشد قیمت در بیش از ۸۰ درصد از نمادهای بورسی باعث شد تا نماگر اصلی سهام ۱.۵ درصد افزایش یابد و به سطح ۲۹۴ هزار واحد برسد."))
# print(normalize("سپرده گذاری بانک مجلس اعلام"))
