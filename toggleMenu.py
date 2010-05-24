import gedit
import gtk
import os

# Toggle menu item XML
ui_manager_xml = """
<ui>
  <menubar name="MenuBar">
    <menu name="ViewMenu" action="View">
      <placeholder name="ViewOps_2">
        <separator/>
        <menuitem name="toggleMenuBar" action="toggleMenuBar"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class toggleMenuInstance:
  def __init__(self, plugin, window):
    
    self._window = window
    self._plugin = plugin
    
    # Find location of Toggle Menu config file (if it's possible)
    try: self._config = os.path.expanduser('~')+"/.toggleMenu"
    except: self._config = ""
    
    # Get gEdit main menu bar object
    self._manager = self._window.get_ui_manager()
    self._menuBar = self._manager.get_widget("/ui/MenuBar")
    
    # Append custom menu item and key shortcut to toggle menu bar
    toggleMenuBar = (
      'toggleMenuBar',
      None,
      _("Toggle Menu"),
      '<Ctrl><Alt>M',
      _("Show or Hide Menu Bar"),
      self.toggle
    )
    self._action_group = gtk.ActionGroup("toggleMenuBar")
    self._action_group.add_actions([toggleMenuBar])
    self._manager.insert_action_group(self._action_group, -1)
    
    self._ui_id = self._manager.add_ui_from_string(ui_manager_xml)
    
    # Auto start with menu hidden?
    try:
      if os.path.exists(self._config):
        self._menuBar.hide()
        
    except: pass
  
  # Show menu, remove custom menu item & keyboard shortcut
  def deactivate(self):
    self._menuBar.show()
    self._manager.remove_ui(self._ui_id)
    self._manager.ensure_update()
    
    del self
  
  # Toggle menu bar and save current status in file (kinda)
  def toggle(self, action):
    if self._menuBar.flags() & gtk.VISIBLE:
      
      self._menuBar.hide()
      try: open(self._config, 'w').close()
      except: pass
    
    else:
      
      self._menuBar.show()
      try: os.unlink(self._config)
      except: pass

# Basic gEdit plugin structure (nothing interesting)
class toggleMenuPlugin(gedit.Plugin):
  def __init__(self):
    gedit.Plugin.__init__(self)
    self._instances = {}
  
  def activate(self, window):
    self._instances[window] = toggleMenuInstance(self, window)
    
  def deactivate(self, window):
    self._instances[window].deactivate()
    del self._instances[window]
    
  def update_ui(self, window):
    pass
