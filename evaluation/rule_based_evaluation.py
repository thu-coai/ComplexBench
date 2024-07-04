import json
import argparse
from con_rule import decompose_judge

def load_jsonl(file_path):
    _data = []
    with open(file_path, 'r') as f:
        for data in f:
            jline = json.loads(data)
            _data.append(jline)
    return _data


def preprocess(s, ass):
    if ass == None or s == None:
        return None, []
    if "【模型回复中评分问题的评测对象】\n" in ass:
        ass = ass.rsplit("【模型回复中评分问题的评测对象】\n", maxsplit=1)[1]
    ass = ass.rsplit("\n\n请注意", maxsplit=1)[0]
    ass = ass.rsplit("\n\n**注意", maxsplit=1)[0]
    ass = ass.rsplit("\n\n注意", maxsplit=1)[0]
    if "评分对象：" in ass:
        decompose = ass.rsplit("评分对象：", maxsplit=1)[1]
    elif "评测对象：" in ass:
         decompose = ass.rsplit("评测对象：", maxsplit=1)[1]
    elif "：" in ass:
         decompose = ass.rsplit("：", maxsplit=1)[1]
    else:
        decompose = ass

    if decompose.startswith('all'):
        rs = [s]
    elif 'None' in decompose:
        rs = []
    else:
        rs = decompose.split('||')
        rs = [r.strip() for r in rs]
    return decompose, rs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="")
    parser.add_argument("--extraction_path", type=str, default="")
    parser.add_argument("--output_path", type=str, default="")
    args = parser.parse_args()

    extractions = load_jsonl(args.extraction_path)
    rule_evaluation_results = []
    for e in extractions:
        decompose, rs = preprocess(e['output'], e['ass'])
        result = decompose_judge(e['rule'], rs)
        e['point_judge'] = result
        e['point_explanation'] = 'RAL'
        rule_evaluation_results.append(e)

    with open(args.output_path, 'w') as f:
        for r in rule_evaluation_results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')