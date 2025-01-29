# Benchmarking Complex Instruction-Following with Multiple Constraints Composition (NeurIPS 2024)

This repository is the official implementation of Benchmarking Complex Instruction-Following with Multiple Constraints Composition. [Our Paper](https://arxiv.org/abs/2407.03978) 

## 🔥 Update

[2025.01.29] We have released the English translation version of ComplexBench in `data/data_final.json`.

## ⚙️ Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

## 📦 Data

All data of ComplexBench is placed in `data/data_final.json` . The entire dataset is organized in the format of a list, where each element of the list is an instance of the dataset. The format of an instance is as follows.

- `main_id` (integer): A unique identifier for the instance.
- `instruction` (string): The actual instruction. 
- `instruction_en` (string): The actual instruction (English translation). 
- `task_types` (string): The task type of the instruction. 
- `constraint_dimensions` (list): All constraint dimensions within the instruction.
- `composition_types` (list): All composition types of constraints within the instruction.
- `category` (list): The category of the instruction based on composition types within it. 
- `scoring_questions` (list): All scoring questions of the instruction, which are designed to verify each constraint dimensions and composition types.  Each element of this list contains:
  - `point_id` (integer): Number of the scoring question.
  - `question` (string): The actual scoring question.
  - `question_en` (string): The actual scoring question (English translation).
  - `rule` (string): Verification rule for the score scoring. `null` indicates that the score question cannot be verified by rules.
  - `constraint_dimensions` (string): All constraint dimensions that the scoring question verifies.
  - `composition_types` (string): All composition types that the scoring question verifies. 
  - `dep` (list): The numbers of all score questions on which this score question depends.

Here is an example of ComplexBench.

```json
{
        "main_id": 899,
        "instruction": "依次判断以下两个案例中的国家是否有特别提款权。如果有，请写出一篇为该国申请提款的文章，字数不少于300字，且分点明确。如果没有则解释原因，字数不超过100字。\n\n案例1：\n\n国家A是一个发展中国家，是国际货币基金组织（IMF）的成员国，正在经历一场自然灾害，导致该国经济陷入危机，失去了国际支付能力。\n\n案例2：\n\n国家B是一个富裕国家，面临着国内通货膨胀问题，B是IMF的成员国，拥有充足的外汇储备。",
        "instruction_en": "Sequentially determine whether the countries in the following two cases have Special Drawing Rights (SDRs). If they do, please write an article of no less than 300 characters applying for withdrawals for that country, output in bullet points format. If not, explain the reason in no more than 100 characters.\n \nCase 1:\n \nCountry A is a developing country and a member of the International Monetary Fund (IMF). It is currently experiencing a natural disaster, leading to an economic crisis and a loss of international payment capability.\n \nCase 2:\n \nCountry B is a wealthy country facing domestic inflation issues. B is a member of the IMF and has ample foreign exchange reserves.",
        "task_types": "Professional Writing",
        "constraint_dimensions": [
            "Length",
            "Helpfulness",
            "Bullets Format",
            "Factuality"
        ],
        "composition_types": [
            "And",
            "Selection"
        ],
        "category": "Selection_2",
        "scoring_questions": [
            {
                "point_id": 0,
                "question": "模型是否正确判断国家A有特别提款权？",
                "question_en": "Does the model correctly determine that Country A possesses Special Drawing Rights?",
                "rule": null,
                "constraint_dimensions": [
                    "Factuality"
                ],
                "composition_types": [
                    "Selection"
                ],
                "dep": []
            },
            {
                "point_id": 1,
                "question": "模型是否正确判断国家B没有特别提款权？",
                "question_en": "Does the model correctly determine that Country B does not have Special Drawing Rights?",
                "rule": null,
                "constraint_dimensions": [
                    "Factuality"
                ],
                "composition_types": [
                    "Selection"
                ],
                "dep": []
            },
            {
                "point_id": 2,
                "question": "模型是否根据国家A有特别提款权生成申请提款的文章？",
                "question_en": "Does the model generate an article on the application for withdrawal based on the Special Drawing Rights of Country A?",
                "rule": null,
                "constraint_dimensions": [
                    "Helpfulness"
                ],
                "composition_types": [],
                "dep": [
                    0
                ]
            },
            {
                "point_id": 3,
                "question": "模型生成的申请提款文章是否逻辑合理，符合事实？",
                "question_en": "Is the withdrawal application article generated by the model logically sound and factually accurate?",
                "rule": null,
                "constraint_dimensions": [
                    "Factuality"
                ],
                "composition_types": [],
                "dep": [
                    0
                ]
            },
            {
                "point_id": 4,
                "question": "模型生成的申请提款文章是否在300字以上？",
                "question_en": "Is the withdrawal application article generated by the model over 300 charcters?",
                "rule": "model_length:[300,10000]",
                "constraint_dimensions": [
                    "Length"
                ],
                "composition_types": [],
                "dep": [
                    0
                ]
            },
            {
                "point_id": 5,
                "question": "模型生成的申请提款文章是否分点明确？",
                "question_en": "Is the withdrawal application article generated by the model output in bullet points format?",
                "rule": null,
                "constraint_dimensions": [
                    "Bullets Format"
                ],
                "composition_types": [],
                "dep": [
                    0
                ]
            },
            {
                "point_id": 6,
                "question": "模型是否生成国家B没有特别提款权的解释？",
                "question_en": "Does the model generate an explanation for why Country B does not have Special Drawing Rights?",
                "rule": null,
                "constraint_dimensions": [
                    "Helpfulness"
                ],
                "composition_types": [],
                "dep": [
                    1
                ]
            },
            {
                "point_id": 7,
                "question": "模型生成的解释是否逻辑合理，符合事实？",
                "question_en": "Are the explanations generated by the model logically sound and factually accurate?",
                "rule": null,
                "constraint_dimensions": [
                    "Factuality"
                ],
                "composition_types": [],
                "dep": [
                    1
                ]
            },
            {
                "point_id": 8,
                "question": "模型生成的解释是否不超过100字？",
                "question_en": "Does the explanation generated by the model not exceed 100 characters?",
                "rule": "model_length:[1,100]",
                "constraint_dimensions": [
                    "Length"
                ],
                "composition_types": [],
                "dep": [
                    1
                ]
            }
        ]
}
```

## 🚀 Evaluation

### Step1: Generating the responses

First, you need to deploy your target LLM and generate responses of it (This part is not included in this repository). We have placed the generated responses of 15 LLMs in our paper in `llm_generations`. You can refer the format of one of these files and replace `genereated` field with your target LLM responses.

We suggest using greedy decoding to avoid the randomness of decoding.

### Step2: Evaluation

Then, you can evaluate any desired model via scirpt `eval.sh`:

```bash
bash eval.sh "<path_to_data_final.json>" "<path_to_generated_responsed_in_step_1>" "<path_to_results>" "<openai_API_KEY>" "<openai_API_KEY>" "<your_model_name>" "<language(zh/en)>"
```

Here is an example:

```bash
bash eval.sh "data/data_final.json" "llm_generations/glm4.jsonl" "evaluation_results" "<openai_API_KEY>" "<openai_API_KEY>" "glm4" "zh"
```

In this example, you can find the results of each scored question in `evaluation_results/glm4_final_results.json`. The statistical data of the final results will be saved in `evaluation_results/glm4_statistics.json`.

## 👏 Citation

```
@article{wen2024benchmarking,
  title={Benchmarking Complex Instruction-Following with Multiple Constraints Composition},
  author={Wen, Bosi and Ke, Pei and Gu, Xiaotao and Wu, Lindong and Huang, Hao and Zhou, Jinfeng and Li, Wenchuang and Hu, Binxin and Gao, Wendy and Xu, Jiaxin and others},
  journal={arXiv preprint arXiv:2407.03978},
  year={2024}
}
```

Please kindly cite our paper if this paper and the codes are helpful.
