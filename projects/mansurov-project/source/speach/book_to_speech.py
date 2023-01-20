import time
from TTS.api import TTS

def text_to_speech(txt, out_file, gpu=True):
    # Get model
    model_name = TTS.list_models()[12]  # 12 norm, 20 - many voices
    # Init TTS
    tts = TTS(model_name, progress_bar=True, gpu=gpu)
    # Run TTS
    tts.tts_to_file(text=txt, file_path=out_file)

def book_to_speech(in_file, out_file, part_size=-1, gpu=True):
    # Get model
    model_name = TTS.list_models()[12]  # 12 norm, 20 - many voices
    # Init TTS
    tts = TTS(model_name, progress_bar=True, gpu=gpu)
    
    if part_size == -1:
        # Full read
        st = time.time()
        # Get book text
        with open(in_file, 'r') as bookfile:
            txt = bookfile.read()
        # Run TTS
        tts.tts_to_file(text=txt, file_path=out_file)
        print(f"Spent {time.time()-st} seconds")
    else:
        # Read by parts
        i_part = 0
        txt = ""
        st = time.time()
        with open(in_file, 'r') as bookfile:
            for line in bookfile:
                txt += line
                if len(txt)>part_size:
                    if any(c.isalpha() for c in txt):
                        tts.tts_to_file(text=txt, file_path=f"{out_file}/part_{i_part}.wav")
                    txt = ""
                    i_part += 1
                    print(i_part)
            if any(c.isalpha() for c in txt):
                tts.tts_to_file(text=txt, file_path=f"{out_file}/part_{i_part}.wav")
                    
        print(f"Spent {time.time()-st} seconds")
    
    
if __name__=="__main__":
    # book_to_speech("projects/mansurov-project/assets/tts/book.txt", "projects/mansurov-project/assets/tts/part_1-3.wav")
    book_to_speech("projects/mansurov-project/assets/tts/book.txt", "projects/mansurov-project/assets/tts/part_1-3", part_size=10000)
    
#     txt = '''\"Naotsugu, look out! Up ahead on your right!\"
# \"Bring it! I\'ve got this.\"
# Naotsugu yelled back to Shiroe, raising his shield. The shield gleamed dull silver as he brought it down on a Triffid.
# \"My liege!\"
# Checking a writhing green vine that had darted out from the left with a single swift strike, Akatsuki slid into a low crouch, positioned to guard Shiroe.
# Smallstone Herb Garden wasn\'t a large zone. However, the ancient gaming facility within its boundaries meant the topography was more varied than the surrounding ruins, and this made it a difficult place to fight.
# \"Hey, how come there are so many of these things?\"
# \"They multiply every time you say something off-color, Naotsugu.\"
# \"What, it\'s my fault?!\"
# Instead of answering, Shiroe generated a pale magic arrow and fired it into a Brier Weasel. Mind Bolt, an arrow of psychic power that could go right through single enemies, was one of the basic offensive spells for Enchanters. Even as he watched the meter-long weasel jump with a piercing shriek, Shiroe mentally visualized an icon. Since recast time was in effect, the icon had lost all its color and was slowly refilling like an hourglass. Shiroe wouldn\'t be able to use that spell again until the icon had regained its glow. It didn\'t matter. He had nearly thirty other spells at his command.
# \"Rush them! Akatsuki, you take the left flank!\"
# \"Yes, sir!\"
# \"On it!\"
# In any case, even if he hadn\'t been able to use his spells, Shiroe had two companions on his side now.
# \"Better get ready \'cos here I come! Shield Smash!\"
# The silver-armored warrior charging down the moss-covered path, sweeping his shield from side to side, was Naotsugu. He was a tall guy with short hair and bright, lively eyes, and he and Shiroe had been friends for years. His class was Guardian. The three Warrior classes specialized in single-handedly fielding enemy attacks, and of the three, Guardians had the highest Defense. In Elder Tales, they boasted the nickname \"The Unbreakable Shield.\"
# \"Too slow.\"
# A girl who had the air of a swallow about her darted through the space Naotsugu\'s advance had cleared. A grotesque creature like a split rugby ball with glass fangs sprang at her, but the girl cut it down with her short sword as she ran, not even pausing. This was Akatsuki: a slight girl whose black hair danced in the wind. Also Shiroe\'s friend, she felt no qualms about calling him \"my liege.\" She was an Assassin, a type of master swordsman whose techniques included a one-strike kill and which boasted the greatest physical attack force of all twelve classes.
# Even as he admired their work, Shiroe hurried after them.
# Shiroe\'s class was Enchanter. Of the three Magician classes, Enchanters were a complete support class that specialized in support spells and negative status magic. As with all the Magician classes, their Defense was shaky. Shiroe couldn\'t even wear the Adventurer\'s leather armor Akatsuki wore, let alone Naotsugu\'s sturdy full armor. All he had under his big white mantle, which looked a bit like a lab coat, were an ordinary tunic shirt and trousers.
# Since Shiroe was a rear guard player with poor Defense, it wasn\'t a good idea for him to be alone on a battlefield. That said, considering the enemy\'s ranged attack spells, it was dangerous for him to get too close to the front line, too. The best policy was for him to leave a certain distance between himself and Naotsugu and Akatsuki while keeping a wary eye out for sneak attacks from the rear.'''
    
#     text_to_speech(txt, "projects/mansurov-project/assets/tts/test.wav")