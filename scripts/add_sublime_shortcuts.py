"""
Sublime shortcuts for jupyter notebook
"""

from jupyter_core.paths import jupyter_config_dir
import os
custom_js_path = os.path.join(jupyter_config_dir(), 'custom', 'custom.js')
custom_path = os.path.join(jupyter_config_dir(), 'custom')


js_script_for_sublime_shortcuts = """
require(["codemirror/keymap/sublime", "notebook/js/cell", "base/js/namespace"],
    function(sublime_keymap, cell, IPython) {
        cell.Cell.options_default.cm_config.keyMap = 'sublime';
        cell.Cell.options_default.cm_config.extraKeys["Ctrl-Enter"] = function(cm) {}
        var cells = IPython.notebook.get_cells();
        for(var cl=0; cl< cells.length ; cl++){
            cells[cl].code_mirror.setOption('keyMap', 'sublime');
            cells[cl].code_mirror.setOption("extraKeys", {
                "Ctrl-Enter": function(cm) {}
            });
        }
    } 
);
"""

if not os.path.exists(custom_path):
    os.makedirs(custom_path)
    
with open(custom_js_path, 'a') as f:
    f.write(js_script_for_sublime_shortcuts)