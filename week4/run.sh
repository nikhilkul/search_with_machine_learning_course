set -x

MIN_QUERIES=1000
OUTPUT='/workspace/datasets/labeled_query_data.txt'
TRAIN_FILE='/workspace/datasets/query.train'
TEST_FILE='/workspace/datasets/query.test'

init(){
    pyenv activate search_with_ml_week4
}

create_labeled_queries(){
    python week4/create_labeled_queries.py \
        --min_queries "$MIN_QUERIES" \
        --output "$OUTPUT"_unshuf
}

generate_training_data(){
    local N=50000
    shuf "$OUTPUT"_unshuf > "$OUTPUT"
    # Split labeled data into training and test.
    head -n "$N" "$OUTPUT" > "$TRAIN_FILE"
    tail -"$N" "$OUTPUT" > "$TEST_FILE"
}

generate_preprocessed_training_data(){
    local N=50000
    shuf "$OUTPUT"_unshuf > "$OUTPUT"
    # Preprocess the text and recreate the training and test data
    cat "$OUTPUT"| sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" > query_categegory.preprocessed.txt
    head -n "$N" query_categegory.preprocessed.txt > "$TRAIN_FILE"
    tail -"$N" query_categegory.preprocessed.txt > "$TEST_FILE"
}

train(){
    local MODEL_OUT=model_nikhil_${MIN_QUERIES}
    ~/fastText-0.9.2/fasttext supervised -input "$TRAIN_FILE" -output $MODEL_OUT -epoch 25 -wordNgrams 2
    ~/fastText-0.9.2/fasttext test $MODEL_OUT.bin "$TEST_FILE"
}

main(){
    init
    create_labeled_queries
    generate_training_data
    # generate_preprocessed_training_data
    train
}

main

exit 0
