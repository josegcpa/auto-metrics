source .env

declare -a CONFIGS=("config.yaml" "config-enhanced.yaml")
ARTICLE_PATH=article-text
OUTPUT_PATH=ratings

for config in ${CONFIGS[@]}
do
    if [[  $config == "config-enhanced.yaml" ]]
    then
        OUTPUT_PATH=ratings-enhanced
    else 
        OUTPUT_PATH=ratings
    fi
    for set in article-text/*
    do  
        set_name=$(basename $set)
        for text in article-text/$set_name/*
        do 
            text_name=$(basename $text | sed 's/\.txt//')
            echo Analysing $text_name with $config
            uv run python src/rate.py \
                --article_path "$text" \
                --output_path $OUTPUT_PATH/gemini/$set_name/$text_name.json \
                --config_path $config &
        done
    done
done