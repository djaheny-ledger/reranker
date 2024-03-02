import cohere

# instantiate the Cohere client
co = cohere.Client("YOUR_API_KEY")  

rerank_dataset = co.create_dataset(name="rerank-dataset",
                                   data=open("path/to/train.jsonl, "rb"),
                                   dataset_type="reranker-finetune-input")
print(rerank_dataset.await_validation())
                                   
rerank_dataset_with_eval = co.create_dataset(name="rerank-dataset-with-eval",
                                             data=open("path/to/train.jsonl, "rb"),
                                             eval_data=open("path/to/eval.jsonl, "rb"),
                                             dataset_type="reranker-finetune-input")
print(rerank_dataset_with_eval.await_validation())