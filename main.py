import pygame
import bad_af_file
import pickle
pygame.font.init()
import math
import random

dim = int(input("Dimension (hauteur) :"))

# Kind 
#   - Noun 
#   - Adjective
#   - Verb
#   - Adverb
#   - Other 

# Suffix / prefix
#   - From a list + flexion 

# Language
#   - Fr, Gr, En, Ch
#   - 1  2    0

# Translation

# nexus 
# # # # - Suffixless Prefixless
# - Translation
# - Ancient
# - Perfect translation
# - Suffix 
# - Same field words

class dictionnary():
    def __init__(self):
        self.words_list = []
        self.fixes = {
            "trans":fixes("trans-"),
            "able":fixes("-able"),
            "in":fixes("in-"),
            "un":fixes("un-"),
            "sup":fixes("sup-"),
            "de":fixes("de-"),
            "en":fixes("-en"),
            "extra":fixes("extra-"),
            "intra":fixes("intra-"),
            "inter":fixes("inter-")}
        self.keren = ["hippos","dromos","polites","kosmos","caput"]
        self.update_fixes_list()

    def update_fixes_list(self):
        self.fixes_lists= list(self.fixes.keys())
        for i in range(len(self.fixes_lists)):
            self.fixes_lists[i] = self.fixes_lists[i].replace("-","")

    def input(self,word):
        vec_word = word
        vec_word.search_nexus(self.words_list)
        vec_word.reciprocal_t1_nexus(self.words_list)
        vec_word.search_translation(self.words_list)
        self.words_list.append(word)
        for words in self.words_list:
            words.search_all_links()
        
class fixes():
    def __init__(self,name):
        self.name = name
        self.words_containing_me = []

class word():
    def __init__(self,name,kind,lang,fixations,t1_nexus,t2_nexus,ker):
        self.name = name
        self.kind = kind
        self.lang = lang
        self.fixations = fixations

        self.saving = [name,kind,lang,fixations,t1_nexus,t2_nexus,ker]
        #--*--*--*--*

        new_t1_nexus = []
        for obj in t1_nexus:
            if type(obj) == type(""):
                new_t1_nexus.append(obj)
            else:
                new_t1_nexus.append(obj.name)

        #--*--*--*--*

        new_t2_nexus = []
        for obj in t2_nexus:
            if type(obj[0]) == type(""):
                new_t2_nexus.append(obj)
            else:
                new_obj = [obj[0].name,obj[1]]
                new_t2_nexus.append(new_obj)
        
        #--*--*--*--*


        self.nexus = [new_t1_nexus,new_t2_nexus,[],{},[],[]]
        self.ker = ker

        self.append_fixations_nexus_class()

    def append_fixations_nexus_class(self):
        for fixations in self.fixations:
            self.nexus[3][fixations.name] = []

    def reciprocal_t1_nexus(self,called_dictionnary):
        
        for i in range(len(self.nexus[0])):
            for word in called_dictionnary:
                if word.name == self.nexus[0][i]:
                    self.nexus[0][i] = word
                    
                    #PUT TRANSLATION IN SELF
                    found = False
                    for j in range(len(word.nexus[0])):
                        if word.nexus[0][j] == self.name:
                            word.nexus[0][j] = self
                            found = True
                    if not found:
                        word.nexus[0].append(self)

    def search_translation(self,called_dictionnary):

        for i in range(len(self.nexus[1])):
            for link in called_dictionnary:
                if self.nexus[1][i][0] == link.name and link.lang ==self.nexus[1][i][1]:
                    self.nexus[1][i][0] = link
                    found = False

                    for j in range(len(link.nexus[1])):
                        if link.nexus[1][j][1] == self.lang:
                            link.nexus[1][j][0] = self
                            found = True 
                    if not found:
                        link.nexus[1].append([self,self.lang])
        
    def search_nexus(self,called_dictionnary):
        # Search for same ker 
        for kers in self.ker:
            for word in called_dictionnary:
                if word != self:
                    if kers in word.ker:
                        self.nexus[2].append(word)
                        word.nexus[2].append(self)
        
        # Search for same fixations
        for word in called_dictionnary:
            if word != self:
                for self_fixations in self.fixations:
                    if self_fixations in word.fixations:
                        self.nexus[3][self_fixations.name].append(word)
                        word.nexus[3][self_fixations.name].append(self)

    def search_all_links(self):
        self.nexus[4] = []
        
        for word in self.nexus[0]:
            if type(word) != "str":
                self.nexus[4].append(word)

        for word in self.nexus[2]:
            if type(word) != "str":
                self.nexus[4].append(word)
        
        for i in range(len(self.nexus[3])):
            for word in self.nexus[3][self.fixations[i].name]:
                if type(word) != "str":
                    self.nexus[4].append(word)
        
        for j in range(len(self.nexus[1])):
            if type(j) != str:
                self.nexus[4].append(self.nexus[1][j][0])
        

        self.nexus[4] = set(self.nexus[4])

class graphic():
    def __init__(self,dim):
        self.h = dim
        self.lard = int(dim*1600/900)
        self.screen = pygame.display.set_mode((self.lard,self.h))
        self.surface = pygame.Surface((1600,900))
        self.surface_2 = pygame.Surface((250,900))
        self.surface3 = pygame.Surface((1600,150))
        self.running = True 
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption('Carte heuristique')

        self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.font = pygame.font.Font("good font.otf",50)
        self.font_little2 = pygame.font.Font("good font.otf",20)
        self.font_little15 = pygame.font.Font("good font.otf",23)
        self.font_little = pygame.font.Font("good font.otf",25)
        self.font_middle = pygame.font.Font("good font.otf",30)
        self.font_2 = pygame.font.Font("good font.otf",60)
        self.focused_traduction = 0
        self.camera = [0,0]
        self.zoom_factor = 10
        self.colors = [(139,189,187),(38,78,88),(110,102,89),(55,71,133)]

        # word adding 
        self.ewann_button = pygame.rect.Rect(250/2-self.font_little.size("Hamon Ewann")[0]/2+1350,850,self.font_little.size("Hamon Ewann")[0],self.font_little.size("Hamon Ewann")[1])
        self.writing_rect = pygame.rect.Rect(330,150/2-28,350,56)
        self.is_adding = False
        self.focused_enter = None
        self.enters_rects = [[self.writing_rect,"",self.surface3,"Mot que vous souhaitez ajouter",(94,42,44)],[pygame.rect.Rect(340,64+150+126-30,280,56),"",self.surface,"Fixe correspondant",(37,37,37)],[pygame.rect.Rect(340+320,64+150+126-30,280,56),"",self.surface,"Chercher cousin",(37,37,37)],[pygame.rect.Rect(340+320+320,64+150+126-30,280,56),"",self.surface,"Chercher traduction",(37,37,37)],[pygame.rect.Rect(340+640
        +320,64+150+126-30,280,56),"",self.surface,"Chercher noyau",(37,37,37)]]
        self.switch = [0,60,False,{True:" ;",False:""}]
        self.capslock = False
        self.underlines = [pygame.rect.Rect(64,150/2-self.font_middle.size("Ajouter un mot :")[1]/2+self.font_middle.size("Ajouter un mot :")[1]+6,self.font_middle.size("Ajouter un mot :")[0],3),
                           pygame.rect.Rect(1050,150/2-self.font_middle.size("Enregistrer votre entree")[1]/2+self.font_middle.size("Enregistrer votre entree")[1]+6,self.font_middle.size("Enregistrer votre entree")[0],3)
                            ]

        # language section 
        self.language_list = ["Anglais","Francais","Allemand","Noyau"]
        self.focused_language = 1
        self.chosen = []
        self.chosen_words = []
        self.new_language_list = []
        self.word_found = {}
        self.chosen_kers = []

        self.main_dict = dictionnary()
        
        self.graphic_words = []
        self.links_type = 0
        suffix_chioces = list(self.main_dict.fixes.keys())
        number = 0
        """
        for i in range(24):
            self.main_dict.input(word(self.alphabet[i],"None",0,[self.main_dict.fixes[suffix_chioces[random.randint(0,3)]]],[],[],[]))
            self.graphic_words.append(word_object(self.main_dict.words_list[-1],*self.calculate_emplacement(i)))
        """
        self.drawing_words = self.graphic_words

        self.focused_word = None
        self.language_dict = {0:"Anglais",1:"Francais",2:"Allemand",3:"Latin"}

        self.text_dict = {0:"Contextuels",1:"Traductions",2:"Noyau commun",3:"Fixes communs",4:"Tous"}

    def calculate_emplacement(self,t):
        t = (t+10)*math.pi/5
        x = int(math.cos(t) * 300/math.pi * t )
        y = int(math.sin(t) * 300/math.pi * t )
        return x,y
        
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.is_adding:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                        if event.button == 1:
                            reached = False 
                            for words in self.drawing_words:
                                if words.rect.collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))): #REPLACE
                                    self.focused_word = words 
                                    reached = True
                            if not reached:
                                self.focused_word = None
                        
                            # detect for adding word 

                            if self.ewann_button.collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))): #replace
                                self.is_adding =  True 
                            else:
                                self.is_adding = False
                        
                        if event.button == 4:
                            self.zoom_factor += 0.5
                            for objs in self.graphic_words:
                                objs.change_scale(self.camera,self.zoom_factor,self.focused_word)

                        if event.button == 5:
                            self.zoom_factor -= 0.5
                            for objs in self.graphic_words:
                                objs.change_scale(self.camera,self.zoom_factor,self.focused_word)
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.links_type += 1
                        if self.links_type == 5:
                            self.links_type = 0
                    if event.key == pygame.K_DOWN:
                        self.links_type -= 1
                        if self.links_type == -1:
                            self.links_type = 4
                    if event.key == pygame.K_a:
                        self.camera[0] += 250
                        for words in self.graphic_words:
                            words.update_rect(self.camera,self.zoom_factor)
                    if event.key == pygame.K_d:
                        self.camera[0] -= 250
                        for words in self.graphic_words:
                            words.update_rect(self.camera,self.zoom_factor)
                    if event.key == pygame.K_w:
                        self.camera[1] += 250
                        for words in self.graphic_words:
                            words.update_rect(self.camera,self.zoom_factor)
                    if event.key == pygame.K_s:
                        self.camera[1] -= 250
                        for words in self.graphic_words:
                            words.update_rect(self.camera,self.zoom_factor)
                    if event.key == pygame.K_p:
                        usefull_info = []
                        for dsd in self.main_dict.words_list:
                            usefull_info.append(dsd.saving)

                        pickle.dump( [usefull_info,self.main_dict.fixes,self.main_dict.keren], open( "save.data", "wb" ) )
                        print("has saved")
                    if event.key == pygame.K_o:
                        usefull_info = pickle.load( open( "save.data", "rb" ) )
                        self.main_dict.words_list = []
                        self.drawing_words = []
                        self.graphic_words = []
                        self.main_dict.keren = usefull_info[2]
                        self.main_dict.fixes = usefull_info[1]
                        self.main_dict.update_fixes_list()
                        for wrd in usefull_info[0]:
                            self.main_dict.input(word(*wrd))
                            self.graphic_words.append(word_object(self.main_dict.words_list[-1],*self.calculate_emplacement(self.main_dict.words_list.index(self.main_dict.words_list[-1]))))
                        self.drawing_words = self.graphic_words
            
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    found = False 
                    for rect in self.enters_rects:
                        if rect[0].collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                            self.focused_enter = rect
                            found = True 

                    for i in range(len(self.language_list)):
                        rect = pygame.rect.Rect(24+100,64+150+126+i*86-5,self.font_little.size(self.language_list[i])[0],50)
                        if rect.collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):

                            self.focused_language = i

                    if self.focused_enter == self.enters_rects[1] and self.enters_rects[1][1] != "":
                        for p in range(len(self.propo)):
                            if pygame.rect.Rect(350,64+150+126+56+10+p*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                if self.propo[p] in self.chosen:
                                    self.chosen.remove(self.propo[p])
                                else:
                                    self.chosen.append(self.propo[p])
                                self.enters_rects[1][1] = ""
                        if pygame.rect.Rect(350,64+150+126+56+10+(len(self.propo))*58-30,260,56).collidepoint(int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h))):
                            self.main_dict.fixes[self.enters_rects[1][1]] = fixes(self.enters_rects[1][1])
                            self.main_dict.update_fixes_list()
                            self.chosen.append(self.enters_rects[1][1])
                            self.enters_rects[1][1] = ""
                    
                    if self.focused_enter == self.enters_rects[2] and self.enters_rects[2][1] != "":
                        for p in range(len(self.word_proposition)):
                            if pygame.rect.Rect(350+320,64+150+126+56+10+p*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                if self.word_proposition[p] in self.chosen_words:
                                    self.chosen_words.remove(self.word_proposition[p])
                                else:
                                    self.chosen_words.append(self.word_proposition[p])
                                self.enters_rects[2][1] = ""
                        if pygame.rect.Rect(350+320,64+150+126+56+10+(len(self.word_proposition))*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                            pass

                    if self.focused_enter == self.enters_rects[4] and self.enters_rects[4][1] != "":
                        for p in range(len(self.ker_proposition)):
                            if pygame.rect.Rect(350+640+320,64+150+126+56+10+p*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                if self.ker_proposition[p] in self.chosen_kers:
                                    self.chosen_kers.remove(self.ker_proposition[p])
                                else:
                                    self.chosen_kers.append(self.ker_proposition[p])
                                
                                self.enters_rects[4][1] = ""
                        if pygame.rect.Rect(350+640+320,64+150+126+56+10+(len(self.ker_proposition))*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                            
                            self.main_dict.keren.append(self.enters_rects[4][1].lower())
                            self.chosen_kers.append(self.main_dict.keren[-1])
                            self.enters_rects[4][1] = ""

                    if self.focused_language!= "Noyau":
                        for i in range(len(self.new_language_list)):
                            rect = pygame.rect.Rect(24+100+320*3-70,900-48-50-i*95-5,self.font_little15.size(self.new_language_list[i])[0],50)
                            if rect.collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                self.focused_traduction = i

                        if self.focused_enter == self.enters_rects[3] and self.enters_rects[3][1] != "":
                            for p in range(len(self.trad_proposition)):
                                if pygame.rect.Rect(350+320+320,64+150+126+56+10+p*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                    self.word_found.pop(self.language_list[self.focused_language], None)
                                    self.word_found[self.new_language_list[self.focused_traduction]] = self.trad_proposition[p]
                                    self.enters_rects[3][1] = ""
                            if pygame.rect.Rect(350+320+320,64+150+126+56+10+(len(self.word_proposition))*58-30,260,56).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                                pass

                    if pygame.rect.Rect(1050-10,150/2-self.font_middle.size("Enregistrer votre entree")[1]/2-10,self.font_middle.size("Enregistrer votre entree")[0]+20,self.font_middle.size("Enregistrer votre entree")[1]+20).collidepoint((int(pygame.mouse.get_pos()[0]*(900/self.h)),int(pygame.mouse.get_pos()[1]*(900/self.h)))):
                        temp_fixes = []
                        for f in self.chosen:
                            temp_fixes.append(self.main_dict.fixes[f])
                        temp_trad = []
                        for value in list(self.word_found.keys()):
                            temp_trad.append([self.word_found[value],self.language_list.index(value)])
                        self.main_dict.input(word(self.enters_rects[0][1],"none",self.focused_language,temp_fixes,self.chosen_words,temp_trad,self.chosen_kers))
                        self.focused_language = 1
                        self.chosen = []
                        self.chosen_words = []
                        self.new_language_list = []
                        self.word_found = {}
                        self.chosen_kers = []
                        self.is_adding = False
                        self.graphic_words.append(word_object(self.main_dict.words_list[-1],*self.calculate_emplacement(self.main_dict.words_list.index(self.main_dict.words_list[-1]))))
                        self.drawing_words = self.graphic_words
                        for objs in self.graphic_words:
                            objs.change_scale(self.camera,self.zoom_factor,self.focused_word)                       
                            objs.update_rect(self.camera,self.zoom_factor)
                    if not found:
                        self.focused_enter = None
                
                if event.type == pygame.KEYDOWN:
                    if str(event.unicode).lower() in self.alphabet:
                        if self.focused_enter != None:
                            for rect in self.enters_rects:
                                if rect == self.focused_enter:
                                    rect[1] += str(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        for rect in self.enters_rects:
                                if rect == self.focused_enter:
                                    rect[1] = rect[1][:-1]
                    elif event.key == pygame.K_SPACE:
                        for rect in self.enters_rects:
                                if rect == self.focused_enter:
                                    rect[1] += " "

    def run(self):
        self.event()

    def draw(self):
        self.surface.fill((22,22,22))
        
        if not self.is_adding:

            # DRAW LINKS
            
            if self.focused_word != None:
                if self.links_type != 4:
                    for linky in self.focused_word.word_linked.nexus[self.links_type]:
                        if self.links_type == 0: # If they are in the same family, all in one color
                            for object in self.graphic_words:
                                if object.word_linked == linky:
                                    pygame.draw.line(self.surface,(130,130,130),self.focused_word.rect.center,object.rect.center,5)                        
                        
                        elif self.links_type == 1: # If they have the same ker, all in one color
                            for words in self.focused_word.word_linked.nexus[1]:
                                for object in self.graphic_words:
                                    if object.word_linked == words[0]:
                                        pygame.draw.line(self.surface,self.colors[words[1]],self.focused_word.rect.center,object.rect.center)  

                        
                        elif self.links_type == 2: # If they have the same ker, all in one color
                            for object in self.graphic_words:
                                if object.word_linked == linky:
                                    pygame.draw.line(self.surface,(130,130,130),self.focused_word.rect.center,object.rect.center)  
                        
                        elif self.links_type == 3: # If they have mutal fixations, each fixes each color
                            number_of_fixes = len(self.focused_word.word_linked.nexus[3])
                            
                            for i in range(number_of_fixes):
                                for intra_words in self.focused_word.word_linked.nexus[3][self.focused_word.word_linked.fixations[i].name]: # Check for all the words in each type in fixes
                                    for object in self.graphic_words:
                                        if object.word_linked == intra_words:
                                            pygame.draw.line(self.surface,self.colors[i],self.focused_word.rect.center,object.rect.center)

                else :
                    
                    for linky in self.focused_word.word_linked.nexus[4]:
                        for object in self.graphic_words:
                            if object.word_linked == linky:
                                pygame.draw.line(self.surface,(150,150,150),self.focused_word.rect.center,object.rect.center,4)
                                
                                # ------------

                                fake_nexus_5 = []
                                for baby_link in linky.nexus[4]:
                                    if baby_link not in self.focused_word.word_linked.nexus[4] and baby_link != self.focused_word.word_linked:
                                        fake_nexus_5.append(baby_link)
                            
                                fake_nexus_5 = list(set(fake_nexus_5))
                                
                                for baby_link in fake_nexus_5:
                                    for baby_object in self.graphic_words:
                                            if baby_object.word_linked == baby_link:
                                                pygame.draw.line(self.surface,(80,80,80),baby_object.rect.center,object.rect.center,2)

                                                # --------------

                                                fake_nexus_6 = []
                                                for grandson_link in baby_link.nexus[4]:
                                                    if grandson_link not in self.focused_word.word_linked.nexus[4] and grandson_link not in linky.nexus[4] and  grandson_link != self.focused_word and grandson_link != linky and grandson_link != baby_link:
                                                        fake_nexus_6.append(grandson_link)
                                                
                                                fake_nexus_6 = list(set(fake_nexus_6))
                                                for grandson_link in fake_nexus_6:
                                                    for grandson_object in self.graphic_words:
                                                        if grandson_object.word_linked == grandson_link:
                                                            pygame.draw.line(self.surface,(50,50,50),baby_object.rect.center,grandson_object.rect.center,1)

            # WRITE WORDS

            for words in self.drawing_words:
                pygame.draw.rect(self.surface,(22,22,22),(words.rect.x,words.rect.y,*pygame.font.Font("good font.otf",int(80*self.zoom_factor/10)).size(words.word_linked.name)))
                if words == self.focused_word:
                    self.surface.blit(pygame.font.Font("good font.otf",int(90*self.zoom_factor/10)).render(words.word_linked.name,True,(163,51,39)),(words.rect.x,words.rect.y))
                else:
                    self.surface.blit(pygame.font.Font("good font.otf",int(80*self.zoom_factor/10)).render(words.word_linked.name,True,(199,73,68)),(words.rect.x,words.rect.y))
                

            # BANDEAU DROITE 

            self.surface_2.fill((79,27,29))     
            self.surface_2.blit(self.font_middle.render("Liens affiches : ",True,(255,255,255)),(250/2-self.font_middle.size("Liens affiches : ")[0]/2,50))
            self.surface_2.blit(self.font_little.render(self.text_dict[self.links_type],True,(230,230,230)),(250/2-self.font_little.size(self.text_dict[self.links_type])[0]/2,100))
            
            self.surface_2.blit(self.font_middle.render("Facteur",True,(255,255,255)),(250/2-self.font_middle.size("Facteur")[0]/2,185))
            self.surface_2.blit(self.font_middle.render("de zoom :",True,(255,255,255)),(250/2-self.font_middle.size("de zoom :")[0]/2,220))
            self.surface_2.blit(self.font_little.render(str(self.zoom_factor/10),True,(230,230,230)),(250/2-self.font_little.size(str(self.zoom_factor/10))[0]/2,270))
            self.surface_2.blit(self.font_middle.render("Legende :",True,(255,255,255)),(250/2-self.font_middle.size("Legende :")[0]/2,355))
            self.surface_2.blit(self.font_little.render("Hamon Ewann",True,(230,230,230)),(250/2-self.font_little.size("Hamon Ewann")[0]/2,850))

            if self.focused_word != None:
                self.surface_2.blit(self.font_little.render("Mot : "+str(self.focused_word.word_linked.name),True,(230,230,230)),(250/2-self.font_little.size("Mot : "+str(self.focused_word.word_linked.name))[0]/2,395))
                if self.links_type == 3:
                    self.surface_2.blit(self.font_middle.render("Fixes :",True,(230,230,230)),(250/2-self.font_middle.size("Fixes :")[0]/2,455))
                    for i in range(len(self.focused_word.word_linked.nexus[3])):
                        pygame.draw.rect(self.surface_2,self.colors[i],pygame.rect.Rect(30,505+i*30,20,20))
                        self.surface_2.blit(self.font_little.render(self.focused_word.word_linked.fixations[i].name,True,(230,230,230)),(60,505+i*30-7))
                
                if self.links_type == 1:
                    self.surface_2.blit(self.font_middle.render("Traductions :",True,(230,230,230)),(250/2-self.font_middle.size("Traductions :")[0]/2,455))
                
                    for i in range(len(self.focused_word.word_linked.nexus[1])):
                        pygame.draw.rect(self.surface_2,self.colors[self.focused_word.word_linked.nexus[1][i][1]],pygame.rect.Rect(30,505+i*30,20,20))
                        self.surface_2.blit(self.font_little.render(self.language_dict[self.focused_word.word_linked.nexus[1][i][1]],True,(230,230,230)),(60,505+i*30-7))
                
                if self.links_type == 2:
                    self.surface_2.blit(self.font_middle.render("Noyaux :",True,(230,230,230)),(250/2-self.font_middle.size("Noyaux :")[0]/2,455))
                
                    for i in range(len(self.focused_word.word_linked.ker)):
                        pygame.draw.rect(self.surface_2,self.colors[i],pygame.rect.Rect(30,505+i*30,20,20))
                        
                        self.surface_2.blit(self.font_little.render(self.focused_word.word_linked.ker[i],True,(230,230,230)),(60,505+i*30-7))
            self.surface.blit(self.surface_2,(1350,0))
        else:
            self.surface.fill((22,22,22))
            self.surface3.fill((79,27,29))
            self.surface3.blit(self.font_middle.render("Ajouter un mot :",True,(255,255,255)),(64,150/2-self.font_middle.size("Ajouter un mot :")[1]/2))
            self.surface3.blit(self.font_middle.render("Enregistrer votre entree",True,(255,255,255)),(1050,150/2-self.font_middle.size("Enregistrer votre entree")[1]/2))
            
            pygame.draw.rect(self.surface3,(94,42,44),self.writing_rect)
            
            # cursor switch 1
            self.switch[0] += 1 
            if self.switch[0] > self.switch[1]:
                self.switch[0] = 0 
                self.switch[2] = not self.switch[2]
            
            
            # draw textes in enters rects 
            for rects in self.enters_rects:
                pygame.draw.rect(rects[2],rects[4],rects[0])
                if rects == self.focused_enter:
                    if rects[1] == "":
                        rects[2].blit(self.font_little2.render(rects[3],True,(200,200,200)),(10+rects[0].x,rects[0].y+rects[0].height/2-self.font_little2.size(rects[1]+self.switch[3][self.switch[2]])[1]/2))
                    else:
                        rects[2].blit(self.font_little2.render(rects[1]+self.switch[3][self.switch[2]],True,(255,255,255)),(10+rects[0].x,rects[0].y+rects[0].height/2-self.font_little2.size(rects[1]+self.switch[3][self.switch[2]])[1]/2))
                    
                else:
                    if rects[1] == "":
                        rects[2].blit(self.font_little2.render(rects[3],True,(185,185,185)),(10+rects[0].x,rects[0].y+rects[0].height/2-self.font_little2.size(rects[1]+self.switch[3][self.switch[2]])[1]/2))
                    else:
                        rects[2].blit(self.font_little2.render(rects[1],True,(215,215,215)),(10+rects[0].x,rects[0].y+rects[0].height/2-self.font_little2.size(rects[1]+self.switch[3][self.switch[2]])[1]/2))
            
            for underline in self.underlines:
                pygame.draw.rect(self.surface3,(255,255,255),underline)

            self.surface.blit(self.surface3,(0,0))
        
            #******* SECTION 1 LANGUE *******#

            #---  présentation ---#
            pygame.draw.line(self.surface,(255,255,255),(320,48+150),(320,900-48),5)
            self.surface.blit(self.font_middle.render("Langue : ",True,(255,255,255)),(160-self.font_middle.size("Langue :")[0]/2,64+150))


            for i in range(len(self.language_list)):
                if i == self.focused_language:
                    pygame.draw.rect(self.surface,(255,255,255),(24+80,64+150+126+i*86,10,10))
                    self.surface.blit(self.font_little.render(self.language_list[i],True,(255,255,255)),(24+100,64+150+126+i*86))
                    pygame.draw.rect(self.surface,(255,255,255),(24+100,64+150+126+i*86+36,self.font_little.size(self.language_list[i])[0],4))
                else:
                    pygame.draw.rect(self.surface,(205,205,205),(24+80,64+150+126+i*86,10,10))
                    self.surface.blit(self.font_little.render(self.language_list[i],True,(205,205,205)),(24+100,64+150+126+i*86))
            
            #******* SECTION 2 FIXES *******#

            #---  présentation ---#
            pygame.draw.line(self.surface,(255,255,255),(640,48+150),(640,900-48),5)
            self.surface.blit(self.font_middle.render("Fixes : ",True,(255,255,255)),(320+160-self.font_middle.size("Fixes :")[0]/2,64+150))
            
            self.propo = []
            for fixations in self.main_dict.fixes_lists:
                correct = True
                for i in range(len(self.enters_rects[1][1])):
                    if len(fixations) >= len(self.enters_rects[1][1]):
                        if self.enters_rects[1][1][i] != fixations[i]:
                            correct = False 
                    else:
                        correct = False 
                if correct:
                    self.propo.append(fixations)
            if self.enters_rects[1][1] != "" and self.focused_enter == self.enters_rects[1]:
                for p in range(len(self.propo)):
                    pygame.draw.rect(self.surface,(37,37,37),(350,64+150+126+56+10+p*58-30,260,56))
                    self.surface.blit(self.font_little.render(self.main_dict.fixes[self.propo[p]].name,True,(255,255,255)),(350+10,64-30+150+126+56+13+p*58))
                pygame.draw.rect(self.surface,(37,37,37),(350,64+150+126+56+10+(len(self.propo))*58-30,260,56))
                self.surface.blit(self.font_little.render("Ajouter "+self.enters_rects[1][1],True,(255,255,255)),(350+10,64-30+150+126+56+13+(len(self.propo))*58))
            
            for j in range(len(self.chosen)):
                self.surface.blit(self.font_little.render("-"+self.chosen[j],True,(150,150,150)),(350+10,900-48-50-j*45))
            
            # SECTION 3 MOTS APPARENTES 
            
            #---  présentation ---#
            pygame.draw.line(self.surface,(255,255,255),(960,48+150),(960,900-48),5)
            self.surface.blit(self.font_middle.render("Cousins : ",True,(255,255,255)),(640+160-self.font_middle.size("Cousins :")[0]/2,64+150))
            
            self.word_proposition= []
            for wrds in self.main_dict.words_list:
                correct = True
                if wrds.lang == self.focused_language:
                    for i in range(len(self.enters_rects[2][1])):
                        if len(wrds.name) >= len(self.enters_rects[2][1]):
                            if self.enters_rects[2][1][i] != wrds.name[i]:
                                correct = False 
                        else:
                            correct = False 
                else:
                    correct = False
                if correct:
                    self.word_proposition.append(wrds)
            if self.enters_rects[2][1] != "" and self.focused_enter == self.enters_rects[2]:
                for p in range(len(self.word_proposition)):
                    pygame.draw.rect(self.surface,(37,37,37),(350+320,64+150+126+56+10+p*58-30,260,56))
                    self.surface.blit(self.font_little.render(self.word_proposition[p].name,True,(255,255,255)),(350+320+10,64-30+150+126+56+13+p*58))
                pygame.draw.rect(self.surface,(37,37,37),(350+320,64+150+126+56+10+(len(self.word_proposition))*58-30,260,56))
                self.surface.blit(self.font_little15.render("Ajouter "+self.enters_rects[2][1],True,(255,255,255)),(350+10+320,64-30+150+126+56+18+(len(self.word_proposition))*58))

            for j in range(len(self.chosen_words)):
                self.surface.blit(self.font_little.render("-"+self.chosen_words[j].name,True,(150,150,150)),(350+320+10,900-48-50-j*45))
            
            # SECTION 4 TRADUCTIONS
            pygame.draw.line(self.surface,(255,255,255),(960+320,48+150),(960+320,900-48),5)
            self.surface.blit(self.font_middle.render("Traductions : ",True,(255,255,255)),(640+320+160-self.font_middle.size("Traductions :")[0]/2,64+150))

            l = self.language_list[self.focused_language]
            if l != "Noyau":
                self.new_language_list = self.language_list.copy()
                
                self.new_language_list.remove(l)
                self.new_language_list.remove("Noyau")
                for i in range(len(self.new_language_list)):
                    if i == self.focused_traduction:
                        pygame.draw.rect(self.surface,(255,255,255),(24+80+320*3-70,900-48-50-i*95,10,10))
                        self.surface.blit(self.font_little15.render(self.new_language_list[i],True,(255,255,255)),(24+100+320*3-70,900-48-50-i*95))
                        pygame.draw.rect(self.surface,(255,255,255),(24+100+320*3-70,900-48-50-i*95+36,self.font_little15.size(self.new_language_list[i])[0],4))
                        if self.new_language_list[i] in list(self.word_found.keys()):
                            self.surface.blit(self.font_little15.render("- "+self.word_found[self.new_language_list[i]].name,True,(230,230,230)),(24+100+320*3-70+40,900-48-50-i*95+45))
                    else:
                        pygame.draw.rect(self.surface,(200,200,200),(24+80+320*3-70,900-48-50-i*95,10,10))
                        self.surface.blit(self.font_little15.render(self.new_language_list[i],True,(200,200,200)),(24+100+320*3-70,900-48-50-i*95))
                        if self.new_language_list[i] in list(self.word_found.keys()):
                            self.surface.blit(self.font_little15.render("- "+self.word_found[self.new_language_list[i]].name,True,(175,175,175)),(24+100+320*3-70+40,900-48-50-i*95+45))
            #get propositions 3/4
            self.trad_proposition = []
            
            for wrds in self.main_dict.words_list:
                correct = True
                if wrds.lang == self.language_list.index(self.new_language_list[self.focused_traduction]):
                    for i in range(len(self.enters_rects[3][1])):
                        if len(wrds.name) >= len(self.enters_rects[3][1]):
                            if self.enters_rects[3][1][i] != wrds.name[i]:
                                correct = False
                        else:
                            correct = False 
                else:
                    correct = False
                if correct:
                    self.trad_proposition.append(wrds)
            if self.enters_rects[3][1] != "" and self.focused_enter == self.enters_rects[3]:
                for p in range(len(self.trad_proposition)):
                    pygame.draw.rect(self.surface,(37,37,37),(350+320+320,64+150+126+56+10+p*58-30,260,56))
                    self.surface.blit(self.font_little.render(self.trad_proposition[p].name,True,(255,255,255)),(350+320+320+10,64-30+150+126+56+13+p*58))
                pygame.draw.rect(self.surface,(37,37,37),(350+320+320,64+150+126+56+10+(len(self.trad_proposition))*58-30,260,56))
                self.surface.blit(self.font_little15.render("Ajouter "+self.enters_rects[3][1],True,(255,255,255)),(350+320+10+320,64-30+150+126+56+18+(len(self.trad_proposition))*58))



            # SECTION 5 NOYAU

            self.surface.blit(self.font_middle.render("Noyaux : ",True,(255,255,255)),(640+320+320+160-self.font_middle.size("Noyaux :")[0]/2,64+150))

            self.ker_proposition = []
            
            for wrds in self.main_dict.keren:
                correct = True
                for i in range(len(self.enters_rects[4][1])):
                    if len(wrds) >= len(self.enters_rects[4][1]):
                        if self.enters_rects[4][1][i] != wrds[i]:
                            correct = False
                    else:
                        correct = False 
            
                if correct:
                    self.ker_proposition.append(wrds)
            if self.enters_rects[4][1] != "" and self.focused_enter == self.enters_rects[4]:
                for p in range(len(self.ker_proposition)):
                    pygame.draw.rect(self.surface,(37,37,37),(350+640+320,64+150+126+56+10+p*58-30,260,56))
                    self.surface.blit(self.font_little.render(self.ker_proposition[p],True,(255,255,255)),(350+640+320+10,64-30+150+126+56+13+p*58))
                pygame.draw.rect(self.surface,(37,37,37),(350+320+640,64+150+126+56+10+(len(self.ker_proposition))*58-30,260,56))
                self.surface.blit(self.font_little15.render("Ajouter "+self.enters_rects[4][1],True,(255,255,255)),(350+640+10+320,64-30+150+126+56+18+(len(self.ker_proposition))*58))


            for j in range(len(self.chosen_kers)):
                self.surface.blit(self.font_little.render("-"+self.chosen_kers[j],True,(150,150,150)),(350+640+10+320,900-48-50-j*45))

        # BLIT ALL

        surf = pygame.transform.scale(self.surface, (self.lard,self.h))
        self.screen.blit(surf,(0,0))
        pygame.display.flip()

class word_object():
    def __init__(self,word,x,y):
        self.word_linked = word
        
        self.true_rect = pygame.rect.Rect(x,y,100,100)
        self.rect = pygame.rect.Rect(x,y,100,100)
        self.rect.width = pygame.font.Font("good font.otf",int(80)).size(self.word_linked.name)[0]
        self.rect.height= pygame.font.Font("good font.otf",int(80)).size(self.word_linked.name)[1]
    
    def update_rect(self,camera,zoom):
        self.rect.x = int((self.true_rect.x + camera[0])*zoom/10)
        self.rect.y = int((self.true_rect.y + camera[1])*zoom/10)

    def change_scale(self,camera,zoom,focused_word):
        self.rect.x = int((self.true_rect.x + camera[0])*zoom/10)
        self.rect.y = int((self.true_rect.y + camera[1])*zoom/10)
        if focused_word != self:
            self.rect.width = pygame.font.Font("good font.otf",int(90*zoom/10)).size(self.word_linked.name)[0]
            self.rect.height = pygame.font.Font("good font.otf",int(90*zoom/10)).size(self.word_linked.name)[1]
        else:
            self.rect.width = pygame.font.Font("good font.otf",int(80*zoom/10)).size(self.word_linked.name)[0]
            self.rect.height = pygame.font.Font("good font.otf",int(80*zoom/10)).size(self.word_linked.name)[1]

main_graphic = graphic(dim)
while main_graphic.running:
    main_graphic.run()
    main_graphic.draw()
    main_graphic.clock.tick(60)


