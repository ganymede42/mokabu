###### EDIT #####################
#Directory with ui and resource files
RESOURCE_DIR = .#src/resources

#Directory for compiled resources
#COMPILED_DIR = src/ui
COMPILED_DIR = .#src/ui

#UI files to compile
UI_FILES = DlgTest2.ui DlgTest.ui QDialog1.ui QDialog2.ui QDialog3.ui QMainWindow1.ui QWidget1.ui WndKlienten.ui WndMain.ui WndTest.ui

#Qt resource files to compile
RESOURCES = #images.qrc

#pyuic5 and pyrcc4 binaries
PYUIC = pyuic5
PYRCC = pyuic5

#################################
# DO NOT EDIT FOLLOWING

#COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)
COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/%.py)
COMPILED_RESOURCES = $(RESOURCES:%.qrc=$(COMPILED_DIR)/%_rc.py)

all: resources ui

resources : $(COMPILED_RESOURCES)

ui: $(COMPILED_UI)

#$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
$(COMPILED_DIR)/%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) -x $< -o $@

$(COMPILED_DIR)/%_rc.py : $(RESOURCE_DIR)/%.qrc
	$(PYRCC) $< -o $@

clean:
	$(RM) $(COMPILED_UI) $(COMPILED_RESOURCES) $(COMPILED_UI:.py=.pyc) $(COMPILED_RESOURCES:.py=.pyc)

