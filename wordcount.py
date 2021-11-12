from pathlib import Path
import os
import re
from tkinter import *
from tkinter import filedialog

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill = BOTH, expand = 1)

        #Variables
        #Checkbox bools
        self.include_basegame = BooleanVar(value = False)
        self.include_mod = BooleanVar(value = True)
        self.include_total = BooleanVar(value = True)
        self.include_characters = BooleanVar(value = False)

        #Mod list variables
        self.selected_path = ""
        self.mods = {} #Mod name: mod path
        self.basegame_character_words = {'c': 36032, 'm': 23356, 'n': 15793, 'Br': 8621, 'Ry': 8369, 'An': 6859, 's': 6794, 'Ad': 6419, 'Sb': 5914, 'As': 2803, 'Iz': 2488, 'Rz': 2455, 'Lo': 2211, 'Mv': 1845, 'Em': 1542, 'Zh': 1089, 'Hz': 981, 'St': 890, 'Ka': 700, 'Ip': 504, '"???"': 492, 'Kv': 302, 'a': 270, 'Sy': 263, 'Fr': 196, 'Wr': 186, 'Xu': 164, 'Dm': 146, 'Fv': 143, 'Al': 141, 'Hu': 69, '"Announcer"': 59, 'Kl': 56, 'Op': 42, 'Lu': 35, 'Ei': 34, 'Le': 23, 'Xi': 17, 'Gr': 13, 'Vr': 12, 'Am': 9, 'id': 3, 'Dr': 2} #Character: word count

        #Exit button
        self.exit_button = Button(self, text = "Exit", command = self.exec_exit_button, height = 1, width = 10)
        self.exit_button.place(x = 700, y = 560)

        #File explorer button and label
        self.file_explorer_label = Label(self, text = "")
        self.file_explorer_label.place(x = 400, y = 80, anchor = "center")
        self.file_explorer_button = Button(self, text = "Choose Base Mod File Path", command = self.exec_file_explorer, height = 1, width = 25)
        self.file_explorer_button.place(x = 400, y = 110, anchor = "center")

        #Checkbox labels
        self.inclusion_label = Label(self, text = "- Display -", font = ("Arial", 20))
        self.inclusion_label.place(x = 140, y = 150, anchor = "center")

        self.display_label = Label(self, text = "- Include -", font = ("Arial", 20))
        self.display_label.place(x = 140, y = 270, anchor = "center")
        
        #Include basegame wordcount checkbox
        self.include_basegame_checkbox = Checkbutton(self, text = "Include Base Game Word Count", command = self.update_generate_button, variable = self.include_basegame, onvalue = True, offvalue = False, width = 25)
        self.include_basegame_checkbox.place(x = 140, y = 310, anchor = "center")

        #Include mod wordcount checkbox
        self.include_mod_checkbox = Checkbutton(self, text = "Include Mod Word Count", command = self.update_generate_button, variable = self.include_mod, onvalue = True, offvalue = False, width = 25)
        self.include_mod_checkbox.place(x = 140, y = 340, anchor = "center")

        #Include total wordcount checkbox
        self.include_total_wordcount_checkbox = Checkbutton(self, text = "Display Total Word Count", command = self.update_generate_button, variable = self.include_total, onvalue = True, offvalue = False, width = 25)
        self.include_total_wordcount_checkbox.place(x = 140, y = 190, anchor = "center")

        #Include characters wordcount checkbox
        self.include_characters_wordcount_checkbox = Checkbutton(self, text = "Display Characters Word Count", command = self.update_generate_button, variable = self.include_characters, onvalue = True, offvalue = False, width = 25)
        self.include_characters_wordcount_checkbox.place(x = 140, y = 220, anchor = "center")

        #Mod List
        self.mod_list = Listbox(self, height = 25, width = 30, selectmode = "multiple")
        self.mod_list.bind("<<ListboxSelect>>", self.update_generate_button)
        self.mod_list.place(x = 400, y = 350, anchor = "center")

        #Generate button
        self.generate_button = Button(self, text = "Generate Word Count", command = self.exec_generate_button, height = 2, width = 20)
        self.generate_button.place(x = 400, y = 35, anchor = "center")
        self.generate_button.location = self.generate_button.place_info()
        self.generate_button.place_forget()

        #Results label
        self.wordcount_label = Label(self, text = "")
        self.wordcount_label.place(x = 650, y = 100, anchor = "n")

        #Author label
        self.author_label = Label(self, text = "Created by\nEval", font = ("Arial", 10))
        self.author_label.place(x = 140, y = 550, anchor = "center")
    
    def update_generate_button(self, event = None):
        if (len(self.mod_list.curselection()) > 0 and (self.include_total.get() or self.include_characters.get())) or (self.include_basegame.get() and (self.include_total.get() or self.include_characters.get())):
            self.generate_button.place(self.generate_button.location)
        else:
            self.generate_button.place_forget()
    
    def exec_generate_button(self):
        return_string = ""
        files_to_parse = []
        total_words = 0
        character_words = {}

        #Add basegame files if necessary
        if self.include_basegame.get():

            #Total words in base game
            total_words += 230177

            #Total words per character in basegame - static values since basegame files are not always accessable
            character_words = {'c': 36391, 'm': 23887, 'n': 16023, 'Br': 15681, 'Ad': 11973, 's': 11801, 'An': 11755, 'Ry': 11091, 'Lo': 9086, 'Sb': 7558, 'Em': 5337, 'Rz': 3969, 'As': 2803, 'Kv': 2796, 'Iz': 2488, 'Mv': 2178, 'Zh': 2163, 'Ip': 2048, 'Ka': 1698, 'Hz': 981, 'St': 890, 'a': 594, 'Dm': 438, 'Sy': 263, 'Fr': 196, 'Wr': 186, 'Xu': 164, 'Fv': 143, 'Al': 141, 'Hu': 69, 'b': 65, 'Kl': 56, 'Op': 42, 'Lu': 35, 'Ei': 34, 'Le': 23, 'Xi': 17, 'Gr': 13, 'Vr': 12, 'Am': 9, 'Dr': 2}

        #Add selected mod files if necessary
        if self.include_mod.get():
            selected_mods = [self.mod_list.get(i) for i in self.mod_list.curselection()]
            for mod in self.mods:
                if mod in selected_mods:
                    for file in os.listdir(os.path.join(self.file_path, self.mods[mod])):
                        if file.endswith(".rpy"):
                            files_to_parse.append(os.path.join(self.file_path, self.mods[mod], file))
        
        #Get the list of characters
        if self.include_characters.get():
            character_list = self.get_character_list(files_to_parse)
            for character in character_list:
                character_words[character] = 0
        
        for file in files_to_parse:
            if self.include_total.get():
                total_words += self.get_words_in_file(file)
            if self.include_characters.get():
                character_words = self.get_words_by_character(file, character_words, character_list)
        
        if self.include_total.get():
            return_string += "Total Word Count:\n{0}\n\n".format(str(total_words))
        
        if self.include_characters.get():
            return_string += "Character Word Count:\n"
            for i in range(0, len(character_words) - 1, 2):
                if (i == len(character_words) - 1):
                    if (len(character_words) % 2 == 0):
                        return_string += "{0}: {1} | {2}: {3}\n".format(list(character_words.keys())[i], list(character_words.values())[i], list(character_words.keys())[i+1], list(character_words.values())[i+1])
                    else:
                        return_string += "{0}: {1}".format(list(character_words.keys())[i], list(character_words.values()[i]))
                else:
                    return_string += "{0}: {1} | {2}: {3}\n".format(list(character_words.keys())[i], list(character_words.values())[i], list(character_words.keys())[i+1], list(character_words.values())[i+1])
        
        self.wordcount_label.config(text = return_string)
    
    def exec_exit_button(self):
        exit()
    
    def exec_file_explorer(self):
        self.file_path = filedialog.askdirectory(initialdir = Path.cwd(), title = "Select Mod Directory")
        self.mods = {} #Reset mod list
        self.file_explorer_label.config(text = "Current Directory: {0}".format(self.file_path))

        for folder in os.listdir(self.file_path):
            with open(os.path.join(self.file_path, folder, "__init__.py"), encoding = "utf-8") as current:
                for line in current:
                    line = line.strip()
                    if re.search("^return\s?\((?:\"|')(.+)(?:\"|'),\s?(?:\"|').+(?:\"|'),\s?(?:\"|').+(?:\"|')\)", line):
                        self.mods[re.search("^return\s?\((?:\"|')(.+)(?:\"|'),\s?(?:\"|').+(?:\"|'),\s?(?:\"|').+(?:\"|')\)", line).group(1)] = folder
                        break
                    elif re.search("^name\s?=\s?(?:\"|')(.+)(?:\"|')", line):
                        self.mods[re.search("^name\s?=\s?(?:\"|')(.+)(?:\"|')", line).group(1)] = folder
                        break

        self.mod_list.config(listvariable = StringVar(value = [key for key in self.mods]))
    
    def get_character_list(self, file_list):
        characters = []

        #Add basegame defined characters if necessary
        if not self.include_basegame.get():
            characters = ["c", "m", "n", "Br", "Ad", "s", "An", "Ry", "Lo", "Sb", "Em", "Rz", "As", "Kv", "Iz", "Mv", "Zh", "Ip", "Ka", "Hz", "St", "a", "Dm", "Sy", "Fr", "Wr", "Xu", "Fv", "Al", "Hu", "b", "Kl", "Op", "Lu", "Ei", "Le", "Xi", "Gr", "Vr", "Am", "Dr"]

        for file in file_list:
            with open(file, encoding = 'cp850') as current:
                for line in current:
                    line = line.strip()
        
                    define_regex = re.search("^define (.+)\s=\s*Character\s*\(.+\).*", line)

                    if define_regex and define_regex.group(1) != "nnvl":
                        characters.append(define_regex.group(1))
        return characters

    def get_words_in_file(self, file):
        is_python = False
        wordcount = 0
        with open(file, encoding = 'cp850') as current:
            for line in current:
                line = line.strip()

                if re.search(".*(?:python|screen).*:(?:\s*#+.+)?", line):
                    is_python = True
                
                if re.search("^label .+:(?:\s*#+.+)?", line):
                    is_python = False
                
                if is_python or re.search("^(if|#|play|elif|sound|\s|queue)", line):
                    continue

                #Get wordcount of line
                is_dialogue = False

                for i, letter in enumerate(line):
                    if not is_dialogue and letter == "\"" and i != 0:
                        is_dialogue = True
                    elif is_dialogue and letter == "\"" and line[i-1] != "\\":
                        is_dialogue = False
                    
                    if is_dialogue and letter == " ":
                        wordcount += 1
                
                #Add one for the first word
                wordcount += 1
        
        return wordcount

    def get_words_by_character(self, file, dictionary, character_list):
        with open(file, encoding = 'cp850') as current:
            for line in current:
                line = line.strip()
                character = ""

                for i in character_list:
                    if line.startswith(i):
                        character = i
                        break
                
                if character == "":
                    continue
                
                is_dialogue = False
                
                for i, letter in enumerate(line):
                    if not is_dialogue and letter == "\"":
                        is_dialogue = True
                    elif is_dialogue and letter == "\"" and line[i-1] != "\\":
                        is_dialogue = False
                    
                    if is_dialogue and letter == " ":
                        dictionary[character] += 1
                
                #Add one for the first word
                dictionary[character] += 1
        
        dictionary = dict(sorted(dictionary.items(), key = lambda x: x[1], reverse = True))

        return dictionary

#Initialize GUI
root = Tk()
app = Window(root)

root.wm_title("AwSW Word Counter")
root.geometry("800x600")

root.mainloop()