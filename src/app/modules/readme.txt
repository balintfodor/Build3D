To get your module listed in the app please put it in a subfolder and give a name that starts with the "module" word. Also, the extension should be .py. Submenus are only created from the top level script directories so modules/<folder_name> will be converted to <folder_name> submenu, but modules/<folder_name>/<sub_folder> won't generate any other submenus. The module search is recursive though. Please use unique names for the module files in the entire modules directory tree.

Examples:
modules/examples/module_hello.py -> will be displayed under the "examples" submenu with the menu item "hello"
modules/examples/hello.py -> this file won't be listed in the menu
modules/examples/subfolder/module_hello.py -> will be displayed under the "examples" submenu with the menu item "hello"

The files should not be hidden and note that empty folders are not listed.