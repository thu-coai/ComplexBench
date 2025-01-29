import json
import os
import time
import argparse
import traceback
from os.path import exists
import openai
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from prompts.RAL_extractor import EXTRACTION_PROMPT, EXTRACTION_PROMPT_EACH


def load_jsonl(file_path):
    _data = []
    with open(file_path, 'r') as f:
        for data in f:
            jline = json.loads(data)
            _data.append(jline)
    return _data


def get_payload(line):
    instruction = line['instruction'][:6000]
    question = line['question']
    if line['output'] != None:
        output = line['output'][:4000]
    else:
        output = "None"
    if 'each' in line['rule']:
        content =  SYS_MSG_EACH.format(instruction=instruction, response=output, question=question)
    else:
        content =  SYS_MSG.format(instruction=instruction, response=output, question=question)
    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 8192,
        "temperature": 0.0,
        "top_p": 0.95,
        "stream": True
    }
    return payload


def save_jsonl(entry, sava_path):
    with open(sava_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False)+ "\n")


def get_answer(input_data: dict, retry=30):
    entry, save_path = input_data['data'], input_data['save_path']
    try:
        payload = get_payload(entry)
        chat_completion = openai.ChatCompletion.create(model=payload['model'], temperature=0, messages=payload['messages'])
        generation = chat_completion.choices[0].message.content

        if generation == None or generation == "":
            get_answer(input_data, retry=retry-1)

        entry['ass'] = generation
        entry['payload'] = payload
        save_jsonl(entry, save_path)
    except Exception as e:
        time.sleep(1.2)
        retry -= 1
        if retry < 0:
            entry['ass'] = "None"
            entry['payload'] = payload
            save_jsonl(entry, save_path)
        print(f"retry:剩余{retry}次")
        print(e)
        print(traceback.format_exc())
        get_answer(input_data, retry=retry)


def run_extraction(save_path, datas, num_pool):
    _input = [{"data": i, "eval_model": "gpt-4-1106-preview", "save_path":save_path} for i in datas if i]
    with ThreadPoolExecutor(max_workers=num_pool) as executor:
        tqdm(executor.map(get_answer, _input), total=len(_input), desc='Processing', ncols=100)


def get_data(data_path, llm_output_path, language="zh"):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(llm_output_path, 'r', encoding='utf-8') as f:
        outputs = [json.loads(line) for line in f.readlines()]
    
    datas = []
    for i, (d, o) in enumerate(zip(data, outputs)):
        for j, q in enumerate(d['scoring_questions']):
            if q['rule'] == None:
                continue
            
            if language == "zh":
                datas.append({
                    "main_id" : i,
                    "point_id" : j,
                    "instruction" : d['instruction'],
                    "rule" : q['rule'],
                    "question" : q['question'],
                    "output" : o['generated'],
                })
            elif language == "en":
                datas.append({
                    "main_id" : i,
                    "point_id" : j,
                    "instruction" : d['instruction_en'],
                    "rule" : q['rule'],
                    "question" : q['question_en'],
                    "output" : o['generated'],
                })
    
    return datas


def main_run(args):    
    datas = get_data(data_path=args.data_path, llm_output_path=args.llm_output_path, language=args.language)
    run_extraction(args.output_path, datas, args.num_pool)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="")
    parser.add_argument("--llm_output_path", type=str, default="")
    parser.add_argument("--num_pool", type=int, default=40)
    parser.add_argument("--output_path", type=str, default="")
    parser.add_argument("--api_key", type=str, default="")
    parser.add_argument("--api_base", type=str, default="")
    parser.add_argument("--language", type=str, default="zh")
    args = parser.parse_args()
    openai.api_key = args.api_key
    openai.api_base = args.api_base
    SYS_MSG = EXTRACTION_PROMPT
    SYS_MSG_EACH = EXTRACTION_PROMPT_EACH
    main_run(args)
