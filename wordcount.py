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
            total_words += 138342 #Total words in base game
            for character in self.basegame_character_words:
                character_words[character] = self.basegame_character_words[character]

            #Programatically gets basegame files from folder "basegame". Replaced with raw values
            #for file in os.listdir(os.path.join(Path.cwd(), "basegame")):
            #    if file.endswith(".rpy"):
            #        files_to_parse.append(os.path.join(Path.cwd(), "basegame", file))

        #Add selected mod files if necessary
        if self.include_mod.get():
            selected_mods = [self.mod_list.get(i) for i in self.mod_list.curselection()]
            for mod in self.mods:
                if mod in selected_mods:
                    for file in os.listdir(self.mods[mod]):
                        if file.endswith(".rpy"):
                            files_to_parse.append(os.path.join(self.mods[mod], file))
        
        for file in files_to_parse:
            if self.include_total.get():
                total_words += self.get_words_in_file(file)
            if self.include_characters.get():
                character_words = self.get_words_by_character(file, character_words)
        
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
            with open(os.path.join(self.file_path, "__init__.py"), encoding = "utf-8") as current:
                for line in current:
                    line = line.strip()
                    if re.search("^return\s?\((?:\"|')(.+)(?:\"|'),\s?(?:\"|').+(?:\"|'),\s?(?:\"|').+(?:\"|')\)", line):
                        self.mods[re.search("^return\s?\((?:\"|')(.+)(?:\"|'),\s?(?:\"|').+(?:\"|'),\s?(?:\"|').+(?:\"|')\)", line).group(1)] = path
                        return
                    elif re.search("^name\s?=\s?(?:\"|')(.+)(?:\"|')", line):
                        self.mods[re.search("^name\s?=\s?(?:\"|')(.+)(?:\"|')", line).group(1)] = path
                        return

        self.mod_list.config(listvariable = StringVar(value = [key for key in self.mods]))

    def get_words_in_file(self, file):
        wordcount = 0
        with open(file, encoding = 'cp850') as current:
            for line in current:
                line = line.strip()
                line_regex = re.search("^(?!if)^(\w{1,2}|(?:\"|')(?:Announcer|\?\?\?)(?:\"|')) (?:\"|')(.+)(?:\"|')(?: with .+)?", line)
                
                if not line_regex:
                    continue

                for letter in line_regex.group(2):
                    if letter == " ":
                        wordcount += 1
                
                #Add one for the first word
                wordcount += 1
        
        return wordcount

    def get_words_by_character(self, file, dictionary):
        with open(file, encoding = 'cp850') as current:
            for line in current:
                line = line.strip()

                line_regex = re.search("^(?!if)^(\w{1,2}|(?:\"|')(?:Announcer|\?\?\?)(?:\"|')) (?:\"|')(.+)(?:\"|')(?: with .+)?", line)

                if not line_regex:
                    continue

                if line_regex.group(1) not in dictionary:
                    dictionary[line_regex.group(1)] = 0

                for letter in line_regex.group(2):
                    if letter == " ":
                        dictionary[line_regex.group(1)] += 1
                
                #Add one for the first word
                dictionary[line_regex.group(1)] += 1
        
        dictionary = dict(sorted(dictionary.items(), key = lambda x: x[1], reverse = True))

        return dictionary

#Initialize GUI
root = Tk()
app = Window(root)

root.wm_title("AwSW Word Counter")
root.geometry("800x600")

root.mainloop()