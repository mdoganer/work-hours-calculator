# gui/widgets.py
import tkinter as tk

class UndoRedoEntry(tk.Entry):
    """Custom Entry widget with undo/redo capability"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.undo_stack = []
        self.redo_stack = []
        self.current_text = ""
        
        # Bind events for tracking changes
        self.bind("<Key>", self._on_key)
        self.bind("<FocusIn>", self._on_focus_in)
    
    def _on_focus_in(self, event):
        # Save initial state when focus enters the widget
        self.current_text = self.get()
    
    def _on_key(self, event):
        # Ignore special keys that don't change content
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 
                           'Alt_L', 'Alt_R', 'Caps_Lock'):
            return
        
        # For Ctrl+Z and Ctrl+Y, we'll handle it separately
        if (event.keysym == 'z' and event.state & 4) or (event.keysym == 'y' and event.state & 4):
            return
            
        # Wait a bit to get the new text after the key is processed
        self.after(10, self._save_state)
    
    def _save_state(self):
        new_text = self.get()
        if new_text != self.current_text:
            # Add to undo stack and clear redo stack
            self.undo_stack.append(self.current_text)
            self.redo_stack.clear()
            # Update current state
            self.current_text = new_text
    
    def undo(self):
        if not self.undo_stack:
            return
            
        # Get the last state from undo stack
        prev_text = self.undo_stack.pop()
        # Add current text to redo stack
        self.redo_stack.append(self.get())
        
        # Update the entry without triggering our change tracking
        self.delete(0, tk.END)
        self.insert(0, prev_text)
        self.current_text = prev_text
    
    def redo(self):
        if not self.redo_stack:
            return
            
        # Get the last state from redo stack
        next_text = self.redo_stack.pop()
        # Add current text to undo stack
        self.undo_stack.append(self.get())
        
        # Update the entry without triggering our change tracking
        self.delete(0, tk.END)
        self.insert(0, next_text)
        self.current_text = next_text