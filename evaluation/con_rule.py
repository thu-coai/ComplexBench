import json
import re
import string

keyword_pattern = r"keyword:(\[.*?\])$"
forbidden_word_pattern = r"forbidden_word:(\[.*?\])$"
startswith_pattern = r"startswith:(.*?)$"
endswith_pattern = r"endswith:(.*?)$"
startswith_and_endswith_pattern = r"startswith:(.*?)\nendswith:(.*?)$"
not_endswith_pattern = r"not endswith:(.*?)$"
length_pattern = r"length:(\[.*?\])$"
length_word_pattern = r"length_word:(\[.*?\])$"
match_pattern = r"match:(.*?)$"
keys_pattern = r"keys:(\[.*?\])$"
json_pattern = r"Json:(\[.*?\])$"
constraint_punc_pattern = r"constraint_punc:(\[.*?\])$"

model_startswith_pattern = r"model_startswith:(.*?)$"
model_endswith_pattern = r"model_endswith:(.*?)$"
model_length_word_pattern = r"model_length_word:(\[.*?\])$"
model_keyword_num_pattern = r"model_keyword_num:(\[.*?\])$"
model_forbidden_word_each_pattern = r"model_forbidden_word_each:(\[.*?\])$"
model_forbidden_word_pattern = r"model_forbidden_word:(\[.*?\])$"
model_keyword_num_and_forbidden_word_each_pattern = r"model_keyword_num_each:(\[.*?\])\nmodel_forbidden_word_each:(\[.*?\])$"
model_keyword_num_each_pattern = r"model_keyword_num_each:(\[.*?\])$"

model_not_startswith_pattern = r"model_not_startswith:(.*?)$"
model_not_endswith_pattern = r"model_not_endswith:(.*?)$"
model_not_endswith_each_pattern = r"model_not_endswith_each:(.*?)$"


model_startswith_and_endswith_pattern = r"model_startswith:(.*?)\nmodel_endswith:(.*?)$"
model_constraint_punc_pattern = r"model_constraint_punc:(\[.*?\])$"
model_constraint_punc_each_pattern = r"model_constraint_punc_each:(\[.*?\])$"
model_startswith_each_pattern = r"model_startswith_each:(.*?)$"
model_endswith_each_pattern = r"model_endswith_each:(.*?)$"
model_starts_with_list_each_pattern = r"model_starts_with_list_each:(\[.*?\])$"
model_keyword_each_pattern = r"model_keyword_each:(\[.*?\])$"
model_keyword_pattern = r"model_keyword:(\[.*?\])$"
model_number_each_pattern = r"model_number_each:(\[.*?\])$"
model_length_each_pattern = r"model_length_each:(\[.*?\])$"
model_length_word_each_pattern = r"model_length_word_each:(\[.*?\])$"
model_length_pattern = r"model_length:(\[.*?\])$"



def decom(s):
    if s == None or s == "":
        return ""
    while s[0] == "\n":
        s = s[1:]
    if s[0] in ['"', '“', '`'] and s[-1] in ['"', '”', '`']:
        return s[1:-1]
    else:
        return s


def extract_json(s):
    stack = 0
    json_start = 0

    if '{' not in s:
        return ""
    
    for i, char in enumerate(s):
        if char == '{':
            if stack == 0:
                json_start = i
            stack += 1
        elif char == '}':
            stack -= 1
            if stack == 0:
                return s[json_start:i+1]
    
    return ""


def extract_and_replace_punctuation_zh(text):
    en_punctuation = string.punctuation
    cn_punctuation = "！" + "\"" + "＃" + '＄' + '％' + '＆' + '\'' + '（'+ '）' + '＊' \
        + '+' + '，' + '-' + '。' + '/' + '：' + '；' + '<' + '=' + '>' + '？' + '@' + '[' + '＼' \
        + ']' + '＾' + '_' + '`' + '{' + '|' + '}' + "~"
    en_to_cn_punctuation = str.maketrans(en_punctuation, cn_punctuation)
    text = text.translate(en_to_cn_punctuation)
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")
    return text


def keyword(s, keywords):
    flag = True
    for keyword in keywords:
        keyword = extract_and_replace_punctuation_zh(keyword)
        if keyword not in s:
            flag = False
            
    return flag


def forbidden_word(s, forbidden_words):
    flag = True
    for forbidden_word in forbidden_words:
        forbidden_word = extract_and_replace_punctuation_zh(forbidden_word)
        if forbidden_word in s:
            flag = False
            
    return flag


def keyword_and_forbidden_word(s, keywords, forbidden_words):
    return keyword(s, keywords) and forbidden_word(s, forbidden_words)


def startswith(s, starts):
    starts = extract_and_replace_punctuation_zh(starts)
    if s.startswith(starts):
        return True
    if s.startswith(starts + "。"):
        return True
    if s.startswith(starts + "？"):
        return True
    return False


def endswith(s, ends):
    ends = extract_and_replace_punctuation_zh(ends)
    if s.endswith(ends):
        return True
    if s.endswith(ends + "。"):
        return True
    if s.endswith(ends + "？"):
        return True
    return False


def not_endswith(s, ends):
    ends = extract_and_replace_punctuation_zh(ends)
    if s.endswith(ends):
        return False
    if s.endswith(ends + "。"):
        return False
    if s.endswith(ends + "？"):
        return False
    return True


def length(s, l):
    if len(s) >= l[0] and len(s) <= l[1]:
        return True
    return False


def length_word(s, l):
    s = s.split()
    if len(s) >= l[0] and len(s) <= l[1]:
        return True
    return False


def json_test(s, keys):
    try:
        s = json.loads(s)
    except:
        return False
    if keys == None:
        return True
    
    for key in keys:
        if key not in s.keys():
            return False
    return True


def check_json(s, keys):
    s = extract_json(s)
    keys = [k for k in keys if k != ""]
    try:
        s = json.loads(s)
        if type(s) == dict:
            for k in keys:
                if k not in s.keys():
                    return False
            if len(s.keys()) != len(keys) and len(keys) != 0:
                return False
            return True
        else:
            return False
    except:
        return False


def constraint_punc(s, punc):
    punc = [extract_and_replace_punctuation_zh(p) for p in punc]
    for p in string.punctuation:
        p = extract_and_replace_punctuation_zh(p)
        if p in s and p not in punc:
            return False
    return True


def decompose_judge(point, rs):
    if 'model_keyword_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        flag = True
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            k_matches = re.findall(model_keyword_each_pattern, point)
            k_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in k_matches]
            if keyword(r, k_matches[0]) == False:
                flag = False
        return flag
    elif 'model_keyword_num_each' in point and "model_forbidden_word_each" in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        k_matches = re.search(model_keyword_num_and_forbidden_word_each_pattern, point, re.DOTALL).group(1)
        f_matches = re.search(model_keyword_num_and_forbidden_word_each_pattern, point, re.DOTALL).group(2)
        k_matches = k_matches.strip('[]').split(',')
        f_matches = f_matches.strip('[]').split(',')
        L = int(k_matches[0])
        R = int(k_matches[1])

        keys = k_matches[2:]
        flag = True
        for r in rs:
            if r == "":
                continue
            
            cnt_1 = 0
            cnt_2 = 0
            for k in keys:
                cnt_1 += keyword(r, [k])
            for f in f_matches:
                cnt_2 += keyword(r, [f])
            
            if cnt_1 < L or cnt_1 > R:
                flag = False
            if cnt_2 > 0:
                flag = False
        return flag
    elif 'model_keyword_num_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        k_matches = re.search(model_keyword_num_each_pattern, point, re.DOTALL).group(1)
        k_matches = k_matches.strip('[]').split(',')
        L = int(k_matches[0])
        R = int(k_matches[1])

        keys = k_matches[2:]
        flag = True
        for r in rs:
            if r == "":
                continue
            cnt_1 = 0
            for k in keys:
                cnt_1 += keyword(r, [k])
            if cnt_1 < L or cnt_1 > R:
                flag = False
        return flag
    elif 'model_keyword_num' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False

        k_matches = re.findall(model_keyword_num_pattern, point)
        k_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in k_matches]
        L = int(k_matches[0][0])
        R = int(k_matches[0][1])
        keys = k_matches[0][2:]

        cnt = 0
        for k in keys:
            cnt += keyword(rs[0], [k])
        
        return cnt >= L and cnt <= R
    elif 'model_keyword' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        k_matches = re.findall(model_keyword_pattern, point)
        k_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in k_matches]
        return keyword(rs[0], k_matches[0])
    elif 'model_forbidden_word_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return True
        f_matches = re.findall(model_forbidden_word_each_pattern, point)
        f_matches = [[x.strip() for x in f.strip('[]').split(',')] for f in f_matches]
        flag = True
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if forbidden_word(r, f_matches[0]) == False:
                flag = False
        
        return flag
    elif 'model_forbidden_word' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return True
        f_matches = re.findall(model_forbidden_word_pattern, point)
        f_matches = [[x.strip() for x in f.strip('[]').split(',')] for f in f_matches]
        return forbidden_word(rs[0], f_matches[0])
    elif 'model_number_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        n_matches = re.findall(model_number_each_pattern, point)
        number = eval(n_matches[0])

        return len(rs) >= number[0] and len(rs) <= number[1]
    elif 'model_length_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        l_matches = re.findall(model_length_each_pattern, point)
        l = eval(l_matches[0])
        flag = True
        for r in rs:
            if r == "":
                continue
            if length(r, l) == False and length(decom(r), l) == False:
                flag = False            
        return flag
    elif 'model_length_word_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        l_matches = re.findall(model_length_word_each_pattern, point)
        l = eval(l_matches[0])
        flag = True
        for r in rs:
            if r == "":
                continue
            if length_word(r, l) == False and length_word(decom(r), l) == False:
                flag = False   
        return flag
    elif 'model_length_word' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        l_matches = re.findall(model_length_word_pattern, point)
        l = eval(l_matches[0])
        return length_word(rs[0], l) or length_word(decom(rs[0]), l)
    elif 'model_length:' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        l_matches = re.findall(model_length_pattern, point)
        l = eval(l_matches[0])
        return length(decom(rs[0]), l) or length(rs[0], l)
    elif 'model_startswith_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        flag = True
        s_matches = re.findall(model_startswith_each_pattern, point, flags=re.DOTALL)
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if startswith(r, s_matches[0]) == False:
                flag = False
        return flag
    elif 'model_starts_with_list_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        s_matches = re.findall(model_starts_with_list_each_pattern, point)
        ks = [[x.strip() for x in s.strip('[]').split(',')] for s in s_matches][0]
        
        if len(rs) != len(ks):
            return False
        
        flag = True
        for i, r in enumerate(rs):
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if startswith(r, ks[i]) == False:
                flag = False
        return flag
    elif 'model_startswith' in point and "model_endswith" in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        s_matches = re.search(model_startswith_and_endswith_pattern, point, flags=re.DOTALL).group(1)
        e_matches = re.search(model_startswith_and_endswith_pattern, point, flags=re.DOTALL).group(2)
        return startswith(rs[0], s_matches) and endswith(rs[0], e_matches)
    elif 'model_startswith' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        s_matches = re.findall(model_startswith_pattern, point, flags=re.DOTALL)
        return startswith(rs[0], s_matches[0])
    elif 'model_endswith_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        flag = True
        e_matches = re.findall(model_endswith_each_pattern, point, flags=re.DOTALL)
        if len(rs) != 1:
            rs = rs[:-1]
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if endswith(decom(r), e_matches[0]) == False and endswith(r, e_matches[0]) == False:
                flag = False
        return flag
    elif 'model_endswith' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        e_matches = re.findall(model_endswith_pattern, point, flags=re.DOTALL)
        return endswith(rs[0], e_matches[0])
    elif 'model_constraint_punc_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        flag = True
        p_matches = re.findall(model_constraint_punc_each_pattern, point)
        p_matches = [[x.strip() for x in p.strip('[]').split(',')] for p in p_matches]
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if constraint_punc(decom(r), p_matches[0]) == False and constraint_punc(r, p_matches[0]) == False:
                flag = False
        return flag
    elif 'model_constraint_punc' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return False
        p_matches = re.findall(model_constraint_punc_pattern, point)
        p_matches = [[x.strip() for x in p.strip('[]').split(',')] for p in p_matches]
        return constraint_punc(decom(rs[0]), p_matches[0])
    elif 'model_not_startswith' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return True
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        s_matches = re.findall(model_not_startswith_pattern, point, flags=re.DOTALL)
        return not startswith(rs[0], s_matches[0])
    elif 'model_not_endswith_each' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return True
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        e_matches = re.findall(model_not_endswith_each_pattern, point, flags=re.DOTALL)
        flag = True
        for r in rs:
            if r == "":
                continue
            r = extract_and_replace_punctuation_zh(r)
            if not_endswith(r, e_matches[0]) == False:
                flag = False
        return flag
    elif 'model_not_endswith' in point:
        if len(rs) == 0 or (len(rs) == 1 and rs[0] == ""):
            return True
        rs[0] = extract_and_replace_punctuation_zh(rs[0])
        e_matches = re.findall(model_not_endswith_pattern, point, flags=re.DOTALL)
        return not_endswith(rs[0], e_matches[0])
    elif 'model' in point or 'each' in point:
        return 2
    else:
        if len(rs) == 0:
            return rule("", point)
        return rule(decom(rs[0]), point) or rule(rs[0], point)


def rule(s, point):
    if 'model' in point:
        return 2
    if "keyword" in point and "forbidden_word" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        k_matches = re.findall(keyword_pattern, point)
        f_matches = re.findall(forbidden_word_pattern, point)
        k_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in k_matches]
        f_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in f_matches]
        return keyword_and_forbidden_word(s, k_matches[0], f_matches[0])
    elif "keyword" in point and "keyword_num" not in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        k_matches = re.findall(keyword_pattern, point)
        k_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in k_matches]
        return keyword(s, k_matches[0])

    elif "match" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        m_matches = re.findall(match_pattern, point)
        return s == m_matches[0] or s == m_matches[0] + "。" or s == m_matches[0] + "."    
    
    elif "constraint_punc" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        p_matches = re.findall(constraint_punc_pattern, point)
        p_matches = [[x.strip() for x in p.strip('[]').split(',')] for p in p_matches]
        return constraint_punc(s, p_matches[0])
    
    elif "forbidden_word" in point:
        if s == "" or "None" in s:
            return True
        s = extract_and_replace_punctuation_zh(s)
        f_matches = re.findall(forbidden_word_pattern, point)
        f_matches = [[x.strip() for x in k.strip('[]').split(',')] for k in f_matches]
        return forbidden_word(s, f_matches[0])
    
    elif "startswith" in point and "endswith" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        s_matches = re.search(startswith_and_endswith_pattern, point, flags=re.DOTALL).group(1)
        e_matches = re.search(startswith_and_endswith_pattern, point, flags=re.DOTALL).group(2)
        return startswith(s, s_matches) and endswith(s, e_matches)
    elif "startswith" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        s_matches = re.findall(startswith_pattern, point, flags=re.DOTALL)
        return startswith(s, s_matches[0])

    elif "not endswith" in point:
        if s == "" or "None" in s:
            return True
        s = extract_and_replace_punctuation_zh(s)
        e_matches = re.findall(not_endswith_pattern, point, flags=re.DOTALL)
        return not_endswith(s, e_matches[0])
    
    elif "endswith" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        e_matches = re.findall(endswith_pattern, point, flags=re.DOTALL)
        return endswith(s, e_matches[0])

    elif "length_word:" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        l_w_matches = re.findall(length_word_pattern, point, flags=re.DOTALL)
        return length_word(s, eval(l_w_matches[0]))
    elif "length:" in point:
        if s == "" or "None" in s:
            return False
        s = extract_and_replace_punctuation_zh(s)
        l_matches = re.findall(length_pattern, point, flags=re.DOTALL)
        return length(s, eval(l_matches[0]))
    elif "Json" in point:
        if s == "" or "None" in s:
            return False
        j_matches = re.findall(json_pattern, point.strip(), flags=re.DOTALL)
        return check_json(s, eval(j_matches[0]))
    else:
        return 2

