import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

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
                            #print("I AM IN WHILE LOOP")
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

# clears list if user decides to pick another project 
            htmlFilesList.clear()

            all_files = os.listdir(filesPath[-1])
            html_files = [] 
            for file in all_files:
                if file.endswith(".html"):
                    html_files.append(file)

            for file in html_files:
                htmlFilesList.append([file])

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
window = builder.get_object("window1")
window.set_title("Html Assistant")
window.show_all()

# show Files column in Tree View
for i, col_title in enumerate(["Files:"]):
    renderer = Gtk.CellRendererText()
    filesTreeView = builder.get_object("filesTreeView")
    column = Gtk.TreeViewColumn(col_title, renderer, text=i)
    filesTreeView.append_column(column)

Gtk.main()
