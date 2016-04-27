#
#  ======= HTML ASSISTANT ========
#
# Author: Jan Pribosek
# Version: 0.2.0
#
# ======= LICENSE =======
#
"""
MIT License

Copyright (c) [2016] [Jan Pribosek]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import gi
import os
import webbrowser
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

filesPath = [] 
documentation_url = 'http://greatdanton.github.io/Html-Assistant-GUI/documentation.html'
DATA = ""
TEMPLATES = []
PROGRAM_DIRECTORY = os.getcwd()


def replace(folder, search_for):
    # search in directory
    os.chdir(folder)
# list of all files
    all_files = os.listdir(folder)

# list of all html files
    html_files = []

    for file in all_files:
        if file.endswith(".html"):
            html_files.append(file)


# get text from navigation_editor
    editor = builder.get_object("navigation_editor")
    start_iter = editor.get_buffer().get_start_iter()
    end_iter = editor.get_buffer().get_end_iter()
    new_navigation_text = editor.get_buffer().get_text(start_iter, end_iter, True)
     
    console = builder.get_object("consoleOutput")
    console_end = console.get_buffer().get_end_iter()
    console.get_buffer().insert(console_end, "\n")
 
# finding and replacing navigation for each file
    for file in html_files:
        # reading file
        current_file = open(file, 'r')
        current_file_text = current_file.read()
        current_file.close()

# if search_for is in current file
        if (search_for in current_file_text):
            start = current_file_text.find(search_for)

            if ('<nav' in search_for):
                ending_with = '</nav>'
                end = current_file_text.find(ending_with, start)
                end = current_file_text.find('>', end) + 1
            elif ('<footer' in search_for):
                ending_with = '</footer>'
                end = current_file_text.find(ending_with, start)
                end = current_file_text.find('>', end) + 1
            elif ('<head' in search_for):
                ending_with = '</head>'
                end = current_file_text.find(ending_with, start)
                end = current_file_text.find('>', end) + 1

# if div is in search_for check if navigation is made of nested divs
            elif ('<div' in search_for):
                open_tag = current_file_text.find("<div", start + 1)
                close_tag = current_file_text.find("</div", start + 1)
                if (close_tag == -1):
                    console_end_iter = console.get_buffer().get_end_iter()
                    console.get_buffer().insert(console_end_iter, file + " => please add closing </div> tag" + "\n")
                    break 
                elif (open_tag == -1):
                    end = close_tag + 6
                elif (close_tag < open_tag):
                    end = close_tag + 6
                else:
                    while(close_tag > open_tag):
                        open_tag = current_file_text.find("<div", open_tag + 1)
                        close_tag = current_file_text.find("</div", close_tag + 1)
                        if (close_tag == -1):
                            console_end_iter = console.get_buffer().get_end_iter()
                            console.get_buffer().insert(console_end_iter, file + " => please add closing </div> tag" + "\n")
                            break 
                        elif (open_tag == -1):
                            end = close_tag + 6
                            break

            final_text = current_file_text[0:start] + new_navigation_text + current_file_text[end:]
# write file
            output_file = open(file, 'w')
            output_file.write(final_text)
            output_file.close()

            console_end_iter = console.get_buffer().get_end_iter()
            console.get_buffer().insert(console_end_iter, file + " => Updated" + "\n")
            print(file + " -> Updated")
        else:
# tell user that element doesn't exist 
            console_end_iter = console.get_buffer().get_end_iter()
            console.get_buffer().insert(console_end_iter, file + " => this element does not exist" + "\n")
            print(file + " -> this element does not exist")

# end of replace function


class Handler:


# main menu button click handlers

##### NEW FILE MENU & MODAL HANDLERS #####

# opens newFile modal when newFile icon is clicked
    def menu_click_newFile(self, button):
        templatePicker = builder.get_object("newFile_templatePicker")
        templateList = builder.get_object("templateStorage")
        templateTreeView = builder.get_object("newFile_templateTreeView")
        editor = builder.get_object("newFile_templateViewer")

# append template title to tree view
        # append names from template to templateTreeView. On select show data from DATA in editor
        templateList.clear()
        for template in DATA["templates"]:
            templateList.append([template])

        if len(TEMPLATES) >= 1:
            templateTreeView.set_cursor(0)

        response = templatePicker.run()
        if response == -4:
            templatePicker.hide()

    def templatePicker_row_click(self, selection):
        treeView = builder.get_object("newFile_templateTreeView")
        editor = builder.get_object("newFile_templateViewer")

# get currently selected name from tree view
        selected = selection.get_selection()
        selected = selected.get_selected()

        model, treeiter = selected
        if treeiter != None:
            templateName = model[treeiter][0]

        #if templateName in TEMPLATES:
        editor.get_buffer().set_text(DATA["templates"][templateName])

    def newFile_templatePicker_ok_click(self, button):
        newFileModal = builder.get_object("newFileModal")

        if ('/' in DATA["path"]):
            os.chdir(DATA["path"])

        newFileModal.set_current_name("Untitled.html")

        response1 = newFileModal.run()
        
        if response1 == -4:
            newFileModal.hide()

    def newFileModal_save_click(self, button):
        templatePicker = builder.get_object("newFile_templatePicker")
        newFileModal = builder.get_object("newFileModal")
        fileName = newFileModal.get_current_name()
        editor = builder.get_object("newFile_templateViewer")

# get text from editor window
        start_iter = editor.get_buffer().get_start_iter()
        end_iter = editor.get_buffer().get_end_iter()
        editor_text = editor.get_buffer().get_text(start_iter, end_iter, True)
        
# if file exists in the project directory, display warning modal,
# else create new file
        if os.path.isfile(fileName):
            msgModal = builder.get_object("msg_fileAlreadyExist")
            modal_response = msgModal.run()
            if modal_response == -4:
                msgModal.hide()
        else:
            output_file = open(fileName, 'x')
            output_file.write(editor_text)
            output_file.close()

            newFileModal.hide()
            templatePicker.hide()

# close save file modal on cancel click
    def newFileModal_cancel_click(self, button):
        fileModal = builder.get_object("newFileModal")
        fileModal.hide()


##### EDIT TEMPLATE MENU & MODAL  HANDLERS ######

# opens editTemplate modal when editTemplate icon is clicked
    def menu_click_editTemplate(self, button):
        editTemplate = builder.get_object("editTemplateModal")
        templateTreeView = builder.get_object("templateTreeView")
        templateList = builder.get_object("templateStorage")

        templateList.clear()
        
        for template in DATA["templates"]:
            templateList.append([template])
            TEMPLATES.append(template)

# select first row if 1 template exist
        if len(TEMPLATES) >= 1:
            templateTreeView.set_cursor(0)

        response = editTemplate.run()
        if response == -4:
            editTemplate.hide()
    

# add template
    def editTemplate_addTemplate_click(self, button):
        templateTreeView = builder.get_object("templateTreeView")
        templateList = builder.get_object("templateStorage")
        tb_templateName = builder.get_object("editTemplate_templateName")
# add to template list
        all_files = [];
        for row in templateList:
            all_files.append(row[:])
    
# flatten all_files array 
        all_files = [item for sublist in all_files for item in sublist]

# if untitled name exist in the all_files array add - number
        name = 'Untitled'
        i = 1
        while (name in all_files):
            name = 'Untitled' + '-' + str(i)
            i += 1

# add new name to the View & update text box
        templateList.append([name])
        tb_templateName.set_text(name)
       
# select/focus last created element
        path = Gtk.TreePath(len(all_files))
        templateTreeView.set_cursor(path, None)

# when template is added, empty editor window
        template_editor = builder.get_object("editTemplate_editor")
        template_editor.get_buffer().set_text("")        


# delete template
    def editTemplate_deleteTemplate_click(self, button):
        templateTreeView = builder.get_object("templateTreeView")
        templateList = builder.get_object("templateStorage")

        selected = templateTreeView.get_selection()
        selected = selected.get_selected()

# remove selected row
        print(selected[1])
        model, treeiter = selected
        if treeiter != None:
            delete_template_name = model[treeiter][0]

# update TEMPLATES and write DATA to config.json
        if delete_template_name in TEMPLATES:
            index = TEMPLATES.index(delete_template_name)
            del TEMPLATES[index]
            del DATA["templates"][delete_template_name]
# update config.json   
            with open(PROGRAM_DIRECTORY + "/config.json", "w") as outfile:
                json.dump(DATA, outfile, indent=4)

# remove selected deleted item from templateList
        if selected[1] != None:
            templateList.remove(selected[1])
        else:
            tb_templateName = builder.get_object("editTemplate_templateName")
            tb_templateName.set_text("")


# save template
    def editTemplate_saveTemplate_click(self, button):

        templateTreeView = builder.get_object("templateTreeView")
        templateList = builder.get_object("templateStorage")
        editor = builder.get_object("editTemplate_editor")
        tb_templateName = builder.get_object("editTemplate_templateName")

# get name of selected row
        selected = templateTreeView.get_selection()
        selected = selected.get_selected()

        model, treeiter = selected
        if treeiter !=None:
            name = model[treeiter][0]
        selected = name

# get text from templateName text box
        new_name = tb_templateName.get_text()

# get text from editor window
        start_iter = editor.get_buffer().get_start_iter()
        end_iter = editor.get_buffer().get_end_iter()
        editor_text = editor.get_buffer().get_text(start_iter, end_iter, True)

# update DATA and config.json
        DATA["templates"][new_name] = editor_text

        if selected in TEMPLATES:
            del DATA["templates"][selected]
            DATA["templates"][new_name] = editor_text

            with open(PROGRAM_DIRECTORY + "/config.json", "w") as outfile:
                json.dump(DATA, outfile, indent=4)

# updating TEMPLATES (replace old name with new one)
            templates_index = TEMPLATES.index(selected)
            TEMPLATES[templates_index] = new_name
            
            templateList[treeiter][0] = new_name
        else:
            DATA["templates"][new_name] = editor_text
            with open(PROGRAM_DIRECTORY + "/config.json", "w") as outfile:
                json.dump(DATA, outfile, indent=4)
# updating TEMPLATES and treeView
            TEMPLATES.append(new_name)
            templateList[treeiter][0] = new_name
        

    def templateTreeView_row_click(self, selection):
        templateTreeView = builder.get_object("templateTreeView")
        templateEditor = builder.get_object("editTemplate_editor")
        tb_templateName = builder.get_object("editTemplate_templateName")

        selected = selection.get_selection()
        selected = selected.get_selected()

        model, treeiter = selected
        if treeiter != None:
            fileName = model[treeiter][0]
            tb_templateName.set_text(fileName)

        if fileName in TEMPLATES:
            templateEditor.get_buffer().set_text(DATA["templates"][fileName])    
        else:
            templateEditor.get_buffer().set_text("")

########## HELP ########## 
# opens web browser when help icon is clicked
    def menu_click_help(self, button):
        webbrowser.open(documentation_url)


########## ABOUT ##########  
# open about modal when about icon is clicked
    def menu_click_about(self, button):
        about_modal = builder.get_object("about_modal")
        response = about_modal.run()
        if response:
            about_modal.hide()


########## OPEN PROJECT ########## 
    def menu_click_openProject(self, button):
        folderChooserModal = builder.get_object("folderChooserModal")
        response = folderChooserModal.run()
        openBtn = builder.get_object("openFolderBtn")
        if response == 1:

# get files path and append it to filesPath array
            filesPath1 = folderChooserModal.get_filename()
            filesPath.append(filesPath1)

            tb_projectPath = builder.get_object("tb_projectPath")
            tb_projectPath.set_text(filesPath1)

# append .html files into files tree view
            filesTreeView =  builder.get_object("filesTreeView")
            htmlFilesList = builder.get_object("htmlFilesList")
            filesTreeView.set_model(htmlFilesList)

# clears list if user decides to pick another project 
            htmlFilesList.clear()

            all_files = os.listdir(filesPath[-1])
            html_files = [] 
            for file in all_files:
                if file.endswith(".html"):
                    html_files.append(file)

            for file in html_files:
                htmlFilesList.append([file])

# store project path into config.json
            DATA["path"] = filesPath[-1]
            with open(PROGRAM_DIRECTORY + "/config.json", "w") as outfile:
                json.dump(DATA, outfile, indent=4)
            
# hides openFolderDialog
            folderChooserModal.hide()
        else:
            folderChooserModal.hide()


    def updateNavigation(self, button):
        replaceNav = builder.get_object("replaceNavBox")
        search_for = replaceNav.get_buffer().get_text()
        
        projectPath = builder.get_object("tb_projectPath")
        path = projectPath.get_text()
        replace(path, search_for)

# update path
        tb_replaceNav = builder.get_object("replaceNavBox")

        replace_editor = builder.get_object("navigation_editor")
        start_iter = replace_editor.get_buffer().get_start_iter()
        end_iter = replace_editor.get_buffer().get_end_iter()
        editor_text = replace_editor.get_buffer().get_text(start_iter, end_iter, True)


        DATA["latestFindAndReplace"] = tb_replaceNav.get_text()
        DATA["replaceEditor"] = editor_text 
        DATA["path"] =  path 
        with open(PROGRAM_DIRECTORY + "/config.json", "w") as outfile:
            json.dump(DATA, outfile, indent=4)
            

# when x is clicked, program exit
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)



# load css styling
style_provider = Gtk.CssProvider()
css = open('style.css', 'rb')
css_data = css.read()
css.close()

style_provider.load_from_data(css_data)

Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

# show main window & connect signals
builder = Gtk.Builder()
builder.add_from_file("assistant.glade")
# connect signals
builder.connect_signals(Handler())

#showing window
window = builder.get_object("mainWindow")
window.set_title("Html Assistant")
window.show_all()



# load last project path from config.json, add path to
# project path textbox and add files to TreeView
with open('config.json') as data_file:
    DATA = json.load(data_file)

for template in DATA["templates"]:
    TEMPLATES.append(template)

tb_projectPath = builder.get_object("tb_projectPath")
tb_projectPath.set_text(DATA["path"])

html_files = os.listdir(DATA["path"])
htmlFilesList = builder.get_object("htmlFilesList")
for file in html_files:
    htmlFilesList.append([file])

tb_findAndReplace = builder.get_object("replaceNavBox")
tb_findAndReplace.set_text(DATA["latestFindAndReplace"])

replace_editor = builder.get_object("navigation_editor")
replace_editor.get_buffer().set_text(DATA["replaceEditor"])


# show Files column in Tree View
for i, col_title in enumerate(["Files:"]):
    renderer = Gtk.CellRendererText()
    filesTreeView = builder.get_object("filesTreeView")
    column = Gtk.TreeViewColumn(col_title, renderer, text=i)
    filesTreeView.append_column(column)


# add text templates in templates tree view
for i, col_title in enumerate(["Templates:"]):
    renderer = Gtk.CellRendererText()
    templateTreeView = builder.get_object("templateTreeView")
    column = Gtk.TreeViewColumn(col_title, renderer, text=i)
    templateTreeView.append_column(column)


# append "Templates" to tree view in new file modal
templateTreeView = builder.get_object("newFile_templateTreeView")
templateTreeView.append_column(Gtk.TreeViewColumn("Templates:", Gtk.CellRendererText(), text=i))


Gtk.main()
