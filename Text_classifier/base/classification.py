from transformers import pipeline

def classifier(text):
    classifier = pipeline("sentiment-analysis", model="youchengChung/10epoch_PTT_classifier_bert-base-mengzi_model")
    result = classifier(text)
    return result
