set -e

RUN_GEMINI=false
RUN_OLLAMA=true
RUN_REASONING=true
declare -a CONFIGS=(
    "config.yaml" 
    "config-enhanced.yaml"
)
declare -a OLLAMA_MODELS=(
    "gemma3:4b-it-q4_K_M"
    "gemma3:12b-it-q4_K_M"
    "gemma3:27b-it-q4_K_M"
    "llama3.2:3b-instruct-q4_K_M"
    "qwen3:4b-q4_K_M"
    "qwen3:8b-q4_K_M"
    "qwen3:14b-q4_K_M"
    "qwen3:32b-q4_K_M"
    "mistral:7b-instruct-q4_0"
    "mistral-small:24b-instruct-2501-q4_K_M"
    "cogito:70b-v1-preview-llama-q4_K_M"
    "cogito:32b-v1-preview-qwen-q4_K_M"
    "cogito:14b-v1-preview-qwen-q4_K_M"
    "cogito:8b-v1-preview-llama-q4_K_M"
    "cogito:3b-v1-preview-llama-q4_K_M"
    "dolphin3:8b-llama3.1-q4_K_M"
    "llama3.3:70b-instruct-q4_K_M"
    "phi4:14b-q4_K_M")
declare -a OLLAMA_MODELS_REASONING=(
    "phi4-reasoning:14b-plus-q4_K_M"
    "qwq:32b-q4_K_M"
    "deepseek-r1:7b-qwen-distill-q4_K_M"
    "deepseek-r1:14b-qwen-distill-q4_K_M"
    "deepseek-r1:32b-qwen-distill-q4_K_M"
    "deepseek-r1:70b-llama-distill-q4_K_M")
ARTICLE_PATH=article-text
OUTPUT_PATH=ratings

TMP_DIR=.tmp
OLLAMA_CTX_SIZE=20000
mkdir -p $TMP_DIR

if [[ $RUN_GEMINI == true ]]
then
    for config in ${CONFIGS[@]}
    do
        if [[  $config == "config-enhanced.yaml" ]]
        then
            OUTPUT_PATH=ratings_improved
        else 
            OUTPUT_PATH=ratings
        fi
        for set in article-text/*
        do  
            set_name=$(basename $set)
            for text in article-text/$set_name/*
            do 
                text_name=$(basename "$text" | sed 's/\.txt//')
                echo Analysing $text_name with $config
                uv run rate \
                    --article_path "$text" \
                    --output_path "$OUTPUT_PATH/gemini/$set_name/$text_name.json" \
                    --config_path $config &
            done
        done
    done
fi

if [[ $RUN_OLLAMA == true ]]
then
    for model in ${OLLAMA_MODELS[@]}
    do
        echo Pulling ollama model $model
        echo -e "FROM $model\nPARAMETER num_ctx $OLLAMA_CTX_SIZE" > $TMP_DIR/Modelfile
        ollama create tmp_model -f $TMP_DIR/Modelfile
        for config in ${CONFIGS[@]}
        do
            if [[  $config == "config-enhanced.yaml" ]]
            then
                OUTPUT_PATH=ratings_improved
            else 
                OUTPUT_PATH=ratings
            fi
            for set in article-text/*
            do  
                set_name=$(basename $set)
                for text in article-text/$set_name/*
                do 
                    text_name=$(basename "$text" | sed 's/\.txt//')
                    output_path="$OUTPUT_PATH/$(echo $model | sed 's/:/-/g')/$set_name/$text_name.json"
                    if [[ ! -f "$output_path" ]]
                    then
                        echo Analysing $text_name with $model and $config
                        uv run rate \
                            --article_path "$text" \
                            --output_path "$output_path" \
                            --config_path $config \
                            --local_model ollama:tmp_model \
                            --with_names \
                            --max_tokens 5000
                    fi
                done
            done
        done
        # stop model to free memory
        ollama stop tmp_model
        ollama rm tmp_model
        ollama rm $model
    done
fi

if [[ $RUN_REASONING == true ]]
then
    for model in ${OLLAMA_MODELS_REASONING[@]}
    do
        echo Pulling ollama model $model
        echo -e "FROM $model\nPARAMETER num_ctx $OLLAMA_CTX_SIZE" > $TMP_DIR/Modelfile
        ollama create tmp_model -f $TMP_DIR/Modelfile
        for config in ${CONFIGS[@]}
        do
            if [[  $config == "config-enhanced.yaml" ]]
            then
                OUTPUT_PATH=ratings_improved
            else 
                OUTPUT_PATH=ratings
            fi
            for set in article-text/*
            do  
                set_name=$(basename $set)
                for text in article-text/$set_name/*
                do 
                    text_name=$(basename "$text" | sed 's/\.txt//')
                    output_path="$OUTPUT_PATH/$(echo $model | sed 's/:/-/g')/$set_name/$text_name.json"
                    if [[ ! -f "$output_path" ]]
                    then
                        echo Analysing $text_name with $model and $config
                        uv run rate \
                            --article_path "$text" \
                            --output_path "$output_path" \
                            --config_path $config \
                            --local_model ollama:tmp_model \
                            --with_names \
                            --prompt_type reasoning
                    fi
                done
            done
        done
        # stop model to free memory
        ollama stop tmp_model
        ollama rm tmp_model
        ollama rm $model
    done
fi
