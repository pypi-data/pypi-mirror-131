from .utils import (convert_lines_from_excel,
                    predict_cluster_from_threshold,
                    save_prediction_to_excel)


def hmin_predict(args):
    
    args.file_path
    
    file_path = args.file_path
    line_idx = int(args.number_col)
    threshold = int(args.threshold)
    
    from kobert_transformers import get_kobert_model, get_tokenizer
    tokenizer = get_tokenizer()
    model = get_kobert_model()
    
    result = convert_lines_from_excel(file_path, line_idx, tokenizer, model)
    
    prediction = predict_cluster_from_threshold(result, threshold)
    save_prediction_to_excel(prediction, file_path, line_idx)
