from .utils import convert_lines_from_excel, plot_dendogram

    
def hmin_plot(args):
    
    args.file_path
    
    file_path = args.file_path
    line_idx = int(args.number_col)
    
    from kobert_transformers import get_kobert_model, get_tokenizer
    tokenizer = get_tokenizer()
    model = get_kobert_model()
    
    result = convert_lines_from_excel(file_path, line_idx, tokenizer, model)
    
    plot_dendogram(result)
