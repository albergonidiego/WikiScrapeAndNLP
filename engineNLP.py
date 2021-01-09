# thanks to James Briggs
# check out https://medium.com/better-programming/how-to-summarize-text-with-googles-t5-4dd1ae6238b6

import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

def nlp_it (text, lenght):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    inputs = tokenizer.encode(
        "summarize: " + text,
                              return_tensors='pt',
                              max_length=512,
                              truncation=True
    )

    summary_ids = model.generate(inputs, max_length=lenght, min_length=80, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0])

    return summary
