import pickle
from main import my_tokenizer, word2vec_vectorize
from huggingsound import SpeechRecognitionModel
from gensim.models import Word2Vec

# model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
# audio_paths = ["audio_1.wav", "audio_2.wav", "audio_3.wav"]
# # audio_paths = ["audio_21.wav", "audio_22.wav", "audio_23.wav"]
# # audio_paths = ["audio_31.wav", "audio_32.wav", "audio_33.wav", "audio_34.wav"]
#
# transcriptions = model.transcribe(audio_paths)
# transcription = ""
# for item in transcriptions:
#     transcription += item['transcription'] + '.\n'
# print(transcription)

# transcription = "I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed I fuck her long, ain't no Minute Maid, my diamonds lemonade Flexin' hard, call me Popeye, wallet filled with spinach, ayy Cut you off on the interstate, I'm first to finish, ayy I'm a young, rich nigga, bitch, it's always been that way To the grave, might just be tomorrow, might just be today So I always live it up, we poppin' bottles, poppin' K'sGucci shades from my bougie bitch, I ain't even had to pay Had to put on for the team and had to put on for the BayI'm still fly when I wear Robin's wings, I can't stay in one place Russian Creams in my rocket ship, we go to outer space Mask off, mask on, fuck it, I can't catch a case Blast off, blast off, see the stars up in the Wraith You can't get into the crib because the mansion got a gate You can't come into my section, I'm gon' put you into place If your club goin' up, you bet I'm sliding like it's chess And I think I fell in love, she shook that ass up in my face I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed She just can't seem to keep her knees closed She just can't seem to keep her knees closed ⁠⁠I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed I don't want a valentine, I just want Valentino I just want the neck, I poke her face like a casino Deep throat, know I get it in like a free throw Shawty want some mo', she just can't seem to keep her knees closed"
# transcription = "When darkness falls, may it be That we should see the light When reaper calls, may it be That we walk straight and right When doubt returns, may it be That faith shall permeate our scars When we're seduced, then may it be That we not deviate our cause All sinners, a future All saints, a past Beginning, the ending Return to ash Now that we're dead, my dear We can be together Now that we're dead, my dear We can live forever When all is pain, may it be It's all we've ever known When flame consumes, may it be It warms our dying bones When loss has won, may it be It's you I'm madly fighting for When kingdom comes, may it be We walk right through that open door All sinners, a future All saints, a past Beginning, the ending Return to ash Now that we're dead, my dear We can be together Now that we're dead, my dear We can live forever NA All sinners, a future All saints, a past Beginning, the ending Return to ash Now that we're dead, my dear We can be together Now that we're dead, my dear We can live, we can live forever Return to ashes, shed this skin Beyond the black, we rise again We shall live forever"
transcription = "Can't be sleeping Keep on waking without the woman next to me Guilt is burning, inside I'm hurting This ain't a feeling I can keep So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Can't you see it? I was manipulated I had to let her through the door I had no choice in this, I was the friend she missed She needed me to talk So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Oh I'm so sorry, so sorry baby (I'll be better this time...) I will be better this time I got to say, I'm so sorry Oh I promise (I'll be better this time, I'll be better this time...) Don't blame it on me Don't blame it on me Can't be sleeping Keep on waking without the woman next to me Guilt is burning, inside I'm hurting This ain't a feeling I can keep So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Can't you see it? I was manipulated I had to let her through the door I had no choice in this, I was the friend she missed She needed me to talk So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Oh I'm so sorry, so sorry baby (I'll be better this time...) I will be better this time I got to say, I'm so sorry Oh I promise (I'll be better this time, I'll be better this time...) Don't blame it on me Don't blame it on me Can't be sleeping Keep on waking without the woman next to me Guilt is burning, inside I'm hurting This ain't a feeling I can keep So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Can't you see it? I was manipulated I had to let her through the door I had no choice in this, I was the friend she missed She needed me to talk So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Oh I'm so sorry, so sorry baby (I'll be better this time...) I will be better this time I got to say, I'm so sorry Oh I promise (I'll be better this time, I'll be better this time...) Don't blame it on me Don't blame it on me Can't be sleeping Keep on waking without the woman next to me Guilt is burning, inside I'm hurting This ain't a feeling I can keep So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Can't you see it? I was manipulated I had to let her through the door I had no choice in this, I was the friend she missed She needed me to talk So blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me Blame it on the night Don't blame it on me, don't blame it on me So blame it on the night Don't blame it on me, don't blame it on me Oh I'm so sorry, so sorry baby (I'll be better this time...) I will be better this time I got to say, I'm so sorry Oh I promise (I'll be better this time, I'll be better this time...) Don't blame it on me Don't blame it on me"
tokenized_text = my_tokenizer(transcription)
print(tokenized_text)
model = Word2Vec.load('word2vec_model')
vector = word2vec_vectorize(tokenized_text, model)
print(vector)

with open('all_clf', 'rb') as file:
    all_clf = pickle.load(file)
pred = all_clf.predict([vector])
proba = all_clf.predict_proba([vector])
print(f"Песня относится к жанру: {pred[0]}, {proba}")

if pred[0] in 'pop':
    with open('pop_clf', 'rb') as file:
        pop_clf = pickle.load(file)
    pred = pop_clf.predict([vector])
    proba = pop_clf.predict_proba([vector])
    print(f"Песня относится к поджанру: {pred[0]}, {proba}")

if pred[0] in 'rock':
    with open('rock_clf', 'rb') as file:
        rock_clf = pickle.load(file)
    pred = rock_clf.predict([vector])
    proba = rock_clf.predict_proba([vector])
    print(f"Песня относится к поджанру: {pred[0]}, {proba}")

if pred[0] in 'rap':
    with open('rap_clf', 'rb') as file:
        rap_clf = pickle.load(file)
    pred = rap_clf.predict([vector])
    proba = rap_clf.predict_proba([vector])
    print(f"Песня относится к поджанру: {pred[0]}, {proba}")
