import gensim
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from tokenization_word2vec import sentences_to_vector
import torch
import torchaudio
import rulemma
import rupostagger
import os
import pickle

tagger = rupostagger.RuPosTagger()
tagger.load()
lemmatizer = rulemma.Lemmatizer()
lemmatizer.load()
stemmer = SnowballStemmer("russian")

MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-russian"
processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)


def get_transcription(audio_path):
    # load our wav file
    speech, sr = torchaudio.load(audio_path)
    speech = speech.squeeze()

    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech)
    # tokenize our wav
    input_values = processor(speech, return_tensors="pt", sampling_rate=16000)["input_values"]
    # perform inference
    logits = model(input_values)["logits"]
    # use argmax to get the predicted IDs
    predicted_ids = torch.argmax(logits, dim=-1)
    # decode the IDs to text
    transcription = processor.decode(predicted_ids[0])
    return transcription.lower()


def fragments_connector(audio_paths: [str]):
    texts = []
    counter = 0
    for audio_path in audio_paths:
        try:
            texts.append(get_transcription(audio_path))
        except Exception as e:
            texts.append([])
            print(e)
        counter += 1
        print(f"Audio {audio_path} transcripted, file count: {counter}")
    return texts


def text_processor(text):
    tokens = word_tokenize(text)
    tags = tagger.tag(tokens)
    lemmas = lemmatizer.lemmatize(tags)
    lemms = []
    for lemma in lemmas:
        lemms.append(lemma[2])
    del lemmas
    stemms = [stemmer.stem(token) for token in tokens]

    return tokens, lemms, stemms


def main():
    data_path = "../../assets/science_audio/"
    audio_paths = os.listdir(data_path)
    audio_paths = [data_path + path for path in audio_paths]
    texts = fragments_connector(audio_paths)
    tokens = []
    lemms = []
    stemms = []
    for text in texts:
        toks, lems, stems = text_processor(text)
        if len(toks):
            tokens.append(toks)
        if len(lems):
            lemms.append(lems)
        if len(stems):
            stemms.append(stems)
    # print(tokens)
    print(lemms)
    # print(stemms)
    model = gensim.models.Word2Vec.load('../../assets/w2v_model')
    vector = sentences_to_vector(lemms, model)
    with open('../../assets/mlp_clf', 'rb') as file:
        clf = pickle.load(file)
    pred_proba = clf.predict_proba([vector])
    pred = clf.predict([vector])
    print(f"Доклад относится к классу: {pred[0]} с вероятностями: {pred_proba}")
    mapping = {'Economy': 0, 'Graphics': 1, 'History': 2, 'IT': 3, 'Maths': 4, 'Physics': 5}
    mapping2 = {0: 'Economy', 1: 'Graphics', 2: 'History', 3: 'IT', 4: 'Maths', 5: 'Physics'}
    current = pred_proba[0][mapping[pred[0]]]
    pred_proba[0][mapping[pred[0]]] = 0
    candidate = max(pred_proba[0])
    candidate_index = max(enumerate(pred_proba[0]), key=lambda x: x[1])[0]
    candidate_name = mapping2[candidate_index]
    is_deep = (pred[0] in ['Maths', 'Physics']) and (candidate_name in ['Maths', 'Physics'])
    if is_deep:
        if current - candidate > 0.2:
            print('Дополнительная проверка не требуется')
        else:
            print('Дополнительная проверка...')
            with open('../../assets/deep_mlp_clf', 'rb') as file:
                model = pickle.load(file)
            pred_proba2 = model.predict_proba([vector])
            pred2 = model.predict([vector])
            print(f"Доклад относится к классу: {pred2[0]} с вероятностями: {pred_proba2}")

    if current > 0.3:
        print('Классификатор уверен в правильности ответа')
    else:
        print('Классификатор не уверен в правильности ответа')


if __name__ == "__main__":
    main()
