data_path=$1
llm_output_path=$2
output_dir=$3
api_key=$4
api_base=$5
model_name=$6
language=$7


python3 evaluation/llm_based_extraction.py \
    --data_path $data_path \
    --llm_output_path $llm_output_path \
    --output_path "${output_dir}/${model_name}_llm_extraction_results.jsonl" \
    --api_key $api_key \
    --api_base $api_base \
    --language $language


python3 evaluation/llm_based_evaluation.py \
    --data_path $data_path \
    --llm_output_path $llm_output_path \
    --output_path "${output_dir}/${model_name}_llm_evaluation_results.jsonl" \
    --api_key $api_key \
    --api_base $api_base \
    --language $language


python3 evaluation/rule_based_evaluation.py \
    --data_path $data_path \
    --extraction_path "${output_dir}/${model_name}_llm_extraction_results.jsonl" \
    --output_path "${output_dir}/${model_name}_rule_evaluation_results.jsonl"


python3 evaluation/aggregation.py \
    --data_path $data_path \
    --llm_evaluation_path "${output_dir}/${model_name}_llm_evaluation_results.jsonl" \
    --rule_evaluation_path "${output_dir}/${model_name}_rule_evaluation_results.jsonl" \
    --model $model_name \
    --output_path $output_dir