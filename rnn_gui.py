import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import shutil
import threading
from textgenrnn import textgenrnn


class RNNGui:

    __root = Tk()
    __thisModel = textgenrnn()
    __thisNewModel = True
    __thisDatasetPath = None
    __thisWordLevel = BooleanVar()
    __thisLineDelimited = BooleanVar()
    __thisBidirectional = BooleanVar()
    __thisIsCSV = BooleanVar()

    __thisLineDelimitedCheckbox = Checkbutton(
        __root, text="Line delimited", onvalue=True, offvalue=False, variable=__thisLineDelimited)
    __thisIsCSVCheckbox = Checkbutton(
        __root, text="csv file", onvalue=True, offvalue=False, variable=__thisIsCSV)
    __thisWordLevelCheckbox = Checkbutton(
        __root, text="Word level", onvalue=True, offvalue=False, variable=__thisWordLevel)
    __thisBidirectionalCheckbox = Checkbutton(
        __root, text="Bidirectional", onvalue=True, offvalue=False, variable=__thisBidirectional)
    __thisNumLayersLabel = Label(__root, text="RNN layers")
    __thisNumLayers = Scale(__root, from_=1, to=4, orient=HORIZONTAL)
    __thisNumLayers.set(2)
    __thisModelSaveNameLabel = Label(__root, text="Save model as")
    __thisModelSaveName = Entry(__root)
    __thisTrainSizeLabel = Label(__root, text="Train size")
    __thisTrainSize = Scale(__root, from_=0.5, to=1,
                            resolution=0.01, orient=HORIZONTAL)
    __thisTrainSize.set(1.0)
    __thisMaxTrainLengthLabel = Label(__root, text="Maximum sequence length")
    __thisMaxTrainLength = Scale(__root, from_=5, to=128, orient=HORIZONTAL)
    __thisMaxTrainLength.set(40)
    __thisLineDelimitedCheckbox.select()
    __thisWordLevelCheckbox.deselect()
    __thisEpochLabel = Label(__root, text="Epochs to train")
    __thisNumEpochs = Scale(__root, from_=1, to=10, orient=HORIZONTAL)
    __thisNumEpochs.set(1)
    __thisTemperatureLabel = Label(__root, text="Temperature (creativity)")
    __thisTemperature = Scale(__root, from_=0, to=1,
                              resolution=0.01, orient=HORIZONTAL)
    __thisTemperature.set(0.5)
    __thisMaxGenLengthLabel = Label(__root, text="Max gen length")
    __thisMaxGenLength = Entry(__root)
    __thisMaxGenLength.insert(0, 1000)
    __thisMaxWordsLabel = Label(__root, text="Max vocab (word level)")
    __thisMaxWordsEntry = Entry(__root)
    __thisMaxWordsEntry.insert(0, 2000)
    __thisPrefixLabel = Label(__root, text="Optional prefix")
    __thisPrefixEntry = Entry(__root)
    __thisNumGenLabel = Label(__root, text="Num to generate")
    __thisNumGenEntry = Entry(__root)
    __thisNumGenEntry.insert(0, 10)
    __thisTrainingLabel = Label(__root, text="\nTRAINING\n")
    __thisSamplingLabel = Label(__root, text="\nSAMPLING\n")
    # default window width and height
    __thisWidth = 360
    __thisHeight = 600

    def __init__(self, **kwargs):

        # Set icon
        try:
            self.__root.wm_iconbitmap("RNNGui.ico")
        except:
            pass

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("RNN gui")

        # Place window on right side of screen
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = screenWidth - self.__thisWidth
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        self.__thisLoadModelButton = Button(
            self.__root, text="Load existing model", bg="pink", command=self.__loadModel)
        self.__thisNewModelButton = Button(
            self.__root, text="Start with new model", bg="pink", command=self.__newModel)
        self.__thisDatasetButton = Button(
            self.__root, text="Choose dataset", bg="pink", command=self.__setDatasetPath)
        self.__thisTrainButton = Button(
            self.__root, text="Train", bg="pink", command=self.__goTrain)
        self.__thisTrainButton.config(state=DISABLED)
        self.__thisGenerateButton = Button(
            self.__root, text="Generate", bg="pink", command=self.__goGenerate, state=DISABLED)
        self.__thisGenToFileButton = Button(
            self.__root, text="Gen to file", bg="pink", command=self.__goGenToFile, state=DISABLED)

        # To make the textarea auto resizable
        self.__thisTrainingLabel.grid(row=0, columnspan=2)
        self.__thisDatasetButton.grid(row=1, columnspan=2, pady=(0, 10))
        self.__thisLoadModelButton.grid(row=2, padx=(10, 10))
        self.__thisNewModelButton.grid(row=2, column=1, padx=(10, 10))
        self.__thisModelSaveNameLabel.grid(row=4)
        self.__thisModelSaveName.grid(row=4, column=1)
        self.__thisNumLayersLabel.grid(row=5)
        self.__thisNumLayers.grid(row=5, column=1)
        self.__thisLineDelimitedCheckbox.grid(row=6)
        self.__thisIsCSVCheckbox.grid(row=6, column=1)
        self.__thisBidirectionalCheckbox.grid(row=7)
        self.__thisWordLevelCheckbox.grid(row=7,column=1)
        self.__thisMaxWordsLabel.grid(row=8)
        self.__thisMaxWordsEntry.grid(row=8, column=1)
        self.__thisTrainSizeLabel.grid(row=9)
        self.__thisTrainSize.grid(row=9, column=1)
        self.__thisMaxTrainLengthLabel.grid(row=10)
        self.__thisMaxTrainLength.grid(row=10, column=1)
        self.__thisEpochLabel.grid(row=12)
        self.__thisNumEpochs.grid(row=12, column=1)
        self.__thisTrainButton.grid(row=13, columnspan=2, pady=(10, 10))

        self.__thisSamplingLabel.grid(row=14, columnspan=2)
        self.__thisNumGenLabel.grid(row=15)
        self.__thisNumGenEntry.grid(row=15, column=1)
        self.__thisMaxGenLengthLabel.grid(row=16)
        self.__thisMaxGenLength.grid(row=16, column=1)
        self.__thisPrefixLabel.grid(row=17)
        self.__thisPrefixEntry.grid(row=17, column=1)
        self.__thisTemperatureLabel.grid(row=18)
        self.__thisTemperature.grid(row=18, column=1)
        self.__thisGenerateButton.grid(row=19, pady=(10, 10))
        self.__thisGenToFileButton.grid(row=19, column=1, pady=(10, 10))

    def __setDatasetPath(self):
        self.__thisDatasetPath = askopenfilename(initialdir="data", defaultextension=".txt",
                                                 filetypes=[("All Files", "*.*"),
                                                            ("Text Documents",
                                                             "*.txt"),
                                                            ("CSV Text Documents", "*.csv")])
        if self.__thisDatasetPath == "":
            self.__thisDatasetPath = None
        if self.__thisDatasetPath:
            basename = os.path.basename(self.__thisDatasetPath)
            self.__root.title(basename + " - RNNGui")
            self.__thisTrainButton.config(state=NORMAL)
            if self.__thisModelSaveName.get() == "" and self.__thisNewModel:
                self.__thisModelSaveName.insert(
                    0, os.path.splitext(basename)[0])

    def __loadModel(self):
        testPath = askdirectory(
            initialdir="weights", title="Open directory containing RNN training data")
        if (os.path.exists(testPath)):
            self.__thisNewModel = False
            modeldir = os.path.split(testPath)[1]
            self.__thisModelSaveName.delete(0, 'end')
            self.__thisModelSaveName.insert(0, modeldir)
            load_loc = os.path.join('weights', modeldir)
            weights_loc = os.path.join(load_loc, 'textgenrnn_weights.hdf5')
            vocab_loc = os.path.join(load_loc, 'textgenrnn_vocab.json')
            config_loc = os.path.join(load_loc, 'textgenrnn_config.json')
            self.__thisModel = textgenrnn(
                weights_path=weights_loc, vocab_path=vocab_loc, config_path=config_loc)
            self.__thisGenerateButton.config(state=NORMAL)
            self.__thisGenToFileButton.config(state=NORMAL)

    def __newModel(self):
        self.__thisNewModel = True
        self.__thisModel = textgenrnn()
        self.__thisModelSaveName.delete(0, 'end')
        self.__thisModelSaveName.insert(0, '')

    def __goTrain(self):
        # save results before training in case user aborts
        save_dir = os.path.join('weights', self.__thisModelSaveName.get())
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        files = ['textgenrnn_weights.hdf5',
                 'textgenrnn_vocab.json', 'textgenrnn_config.json']
        for f in files:
            shutil.copy(f, save_dir)

        if self.__thisDatasetPath == "" or self.__thisDatasetPath == None:
            print("No dataset selected.")
            # TODO: disable training button if no __setDatasetPath
            return

        if self.__thisWordLevel.get() and not self.__thisLineDelimited.get():
            print ('Using word-level mode with large text.')
            self.__thisModel.train_from_largetext_file(self.__thisDatasetPath, num_epochs=self.__thisNumEpochs.get(
            ), new_model=self.__thisNewModel, word_level=True, max_words=int(self.__thisMaxWordsEntry.get()),
            train_size=self.__thisTrainSize.get(), rnn_layers=self.__thisNumLayers.get(), is_csv=self.__thisIsCSV.get(),
            rnn_bidirectional=self.__thisBidirectional.get(), validation=False, max_length=self.__thisMaxTrainLength.get())
        elif self.__thisWordLevel.get():
            print('Using word-level mode.')
            self.__thisModel.train_from_file(self.__thisDatasetPath, num_epochs=self.__thisNumEpochs.get(
            ), new_model=self.__thisNewModel, word_level=True, max_words=int(self.__thisMaxWordsEntry.get()),
            train_size=self.__thisTrainSize.get(), rnn_layers=self.__thisNumLayers.get(), is_csv=self.__thisIsCSV.get(),
            rnn_bidirectional=self.__thisBidirectional.get(), validation=False, max_length=self.__thisMaxTrainLength.get())
        elif not self.__thisLineDelimited.get():
            print('Using large text mode.')
            self.__thisModel.train_from_largetext_file(
                self.__thisDatasetPath, num_epochs=self.__thisNumEpochs.get(), new_model=self.__thisNewModel,
                train_size=self.__thisTrainSize.get(), rnn_layers=self.__thisNumLayers.get(), is_csv=self.__thisIsCSV.get(),
                rnn_bidirectional=self.__thisBidirectional.get(), validation=False, max_length=self.__thisMaxTrainLength.get())
        else:
            print('Beginning training.')
            self.__thisModel.train_from_file(
                self.__thisDatasetPath, num_epochs=self.__thisNumEpochs.get(), new_model=self.__thisNewModel,
                train_size=self.__thisTrainSize.get(), rnn_layers=self.__thisNumLayers.get(), is_csv=self.__thisIsCSV.get(),
                rnn_bidirectional=self.__thisBidirectional.get(), validation=False, max_length=self.__thisMaxTrainLength.get())
        for f in files:
            shutil.copy(f, save_dir)
        self.__thisGenerateButton.config(state=NORMAL)
        self.__thisNewModel = False
        print ("*** Training complete ***\n")

    def __goGenerate(self):

        if self.__thisModel:
            print ("\n*************************\n*** Generating %s samples\n*** Model: \'%s\'\n*** Temperature %0.2f\n*************************\n" %
                   (self.__thisNumGenEntry.get(), self.__thisModelSaveName.get(), self.__thisTemperature.get()))
            self.__thisModel.generate(n=int(self.__thisNumGenEntry.get()), temperature=self.__thisTemperature.get(
            ), prefix=self.__thisPrefixEntry.get(), max_gen_length=int(self.__thisMaxGenLength.get()))
            print ("***\n")

    def __goGenToFile(self):

        if self.__thisModel:
            genFile = "sampled_"+self.__thisModelSaveName.get()+".txt"
            output = os.path.join('output', genFile)
            print ("\n*************************\n*** Generating %s samples to file %s\n*** Model: \'%s\'\n*** Temperature %0.2f\n*************************\n" %
                   (genFile, self.__thisNumGenEntry.get(), self.__thisModelSaveName.get(), self.__thisTemperature.get()))
            self.__thisModel.generate_to_file(n=int(self.__thisNumGenEntry.get()), temperature=self.__thisTemperature.get(
            ), prefix=self.__thisPrefixEntry.get(), max_gen_length=int(self.__thisMaxGenLength.get()), destination_path=output)
            print ("***\n")

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("RNNGui", "Joel Matthys")

    def run(self):

        # Run main application
        self.__root.mainloop()


# Run main application
rnngui = RNNGui(width=360, height=680)
rnngui.run()
