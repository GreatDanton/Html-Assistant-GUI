import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

filesPath = [] 

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

    print(html_files)

# get text from navigation_editor
       
    # finding and replacing navigation for each file
    for file in html_files:
        # reading file
        current_file = open(file, 'r')
        current_file_text = current_file.read()
        current_file.close()

        editor = builder.get_object("navigation_editor")
        start_iter = editor.get_buffer().get_start_iter()
        end_iter = editor.get_buffer().get_end_iter()
        new_navigation_text = editor.get_buffer().get_text(start_iter, end_iter, True)
  

# if search_for is in current file
        if (search_for in current_file_text):
            start = current_file_text.find(search_for)

            if ('<div' in search_for):
                ending_with = '</div>'
            elif ('<nav' in search_for):
                ending_with = '</nav>'
            end = current_file_text.find(ending_with, start) + 6

            
            final_text = current_file_text[0:start] + new_navigation_text + current_file_text[end:]
            # write file
            output_file = open(file, 'w')
            output_file.write(final_text)
            output_file.close()

            console = builder.get_object("consoleOutput")
            console_end_iter = console.get_buffer().get_end_iter()
            console.get_buffer().insert(console_end_iter, file + " => Updated" + "\n")
            print(file + " -> Updated")
        else:
# add navigation if it doesnt exist
            if ('<body>' in current_file_text):
                start = current_file_text.find('<body>') + 6 
            else:
                start = current_file_text.find('>')
  
            final_text = current_file_text[0:start] + '\n' + new_navigation_text + current_file_text[start:]
            # write to file
            output_file = open(file, 'w')
            output_file.write(final_text)
            output_file.close()
            print(file + " -> Navigation added")

# end of replace function

class Handler:
    def selectFolder(self, button):
        folderChooserModal = builder.get_object("folderChooserModal")
        response = folderChooserModal.run()
        openBtn = builder.get_object("openFolderBtn")
        if response == 1:

# get files path and append it to filesPath array
            filesPath1 = folderChooserModal.get_uri()
            filesPath1 = filesPath1.replace("file://", "")
            filesPath.append(filesPath1)

# append .html files into files tree view
            filesTreeView =  builder.get_object("filesTreeView")
            htmlFilesList = builder.get_object("htmlFilesList")
            filesTreeView.set_model(htmlFilesList)
            
            all_files = os.listdir(filesPath[-1])
            html_files = [] 
            for file in all_files:
                if file.endswith(".html"):
                    html_files.append(file)

            for file in html_files:
                htmlFilesList.append([file])

# show files in Tree View
            for i, col_title in enumerate(["Files:"]):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(col_title, renderer, text=i)
                filesTreeView.append_column(column)

# hides openFolderDialog
            folderChooserModal.hide()
        else:
            folderChooserModal.hide()

    def updateNavigation(self, button):
        print(filesPath)
        replaceNav = builder.get_object("replaceNavBox")
        search_for = replaceNav.get_buffer().get_text()

        replace(filesPath[-1], search_for)


# when x is clicked, program exit
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

builder = Gtk.Builder()
builder.add_from_file("assistant.glade")
# connect signals
builder.connect_signals(Handler())

#showing window
window = builder.get_object("window1")
window.show_all()
Gtk.main()
