source .env

declare -a CONFIGS=("config.yaml" "config-enhanced.yaml")
declare -a OLLAMA_MODELS=(
    "gemma3:4b-it-q4_K_M"
    "gemma3:12b-it-q4_K_M"
    "llama3.2:3b-instruct-q4_K_M"
    "qwen3:4b-q4_K_M"
    "qwen3:8b-q4_K_M"
    "mistral:7b-instruct-q4_0"
    "phi4:14b-q4_K_M")
ARTICLE_PATH=article-text
OUTPUT_PATH=ratings

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
            uv run python src/rate.py \
                --article_path "$text" \
                --output_path "$OUTPUT_PATH/gemini/$set_name/$text_name.json" \
                --config_path $config &
        done
    done
done

for model in ${OLLAMA_MODELS[@]}
do
    echo Pulling ollama model $model
    ollama pull $model
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
                uv run python src/rate.py \
                    --article_path "$text" \
                    --output_path $OUTPUT_PATH/$(echo $model | sed 's/:/-/g')/$set_name/$text_name.json \
                    --config_path $config \
                    --local_model $model
            done
        done
    done
done