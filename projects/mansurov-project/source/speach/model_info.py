from TTS.api import TTS

# available models
for i, model in enumerate(TTS.list_models()):
    # if model.split('/')[1]=='en':
    print(f"{i}\t{model}")
    
