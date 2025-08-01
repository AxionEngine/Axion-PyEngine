import os
import json
import shutil
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
from datetime import datetime

class NewProjectDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Create New Project")
        self.geometry("500x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.center_dialog(parent)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Styling
        self.title_font = ("Arial", 14, "bold")
        self.label_font = ("Arial", 11)
        self.entry_font = ("Arial", 11)
        self.button_font = ("Arial", 11, "bold")
        
        # Project Name
        ctk.CTkLabel(self, text="PROJECT NAME", font=self.title_font).grid(
            row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Enter project name",
            font=self.entry_font,
            height=35
        )
        self.name_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.name_entry.bind("<Return>", lambda e: self.create_project())
        self.name_entry.focus_set()
        
        # Project Path
        ctk.CTkLabel(self, text="PROJECT PATH", font=self.title_font).grid(
            row=2, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="w")
        
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.path_frame.grid_columnconfigure(0, weight=1)
        
        self.path_entry = ctk.CTkEntry(
            self.path_frame, 
            font=self.entry_font,
            height=35
        )
        self.path_entry.grid(row=0, column=0, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            self.path_frame, 
            text="Browse",
            width=80,
            height=35,
            command=self.browse_path
        )
        self.browse_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Default path
        default_path = os.path.join(os.path.expanduser("~"), "Documents")
        self.path_entry.insert(0, default_path)
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="e")
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame, 
            text="Cancel",
            width=100,
            command=self.destroy
        )
        self.cancel_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.create_btn = ctk.CTkButton(
            self.button_frame, 
            text="Create & Edit",
            width=120,
            font=self.button_font,
            command=self.create_project
        )
        self.create_btn.grid(row=0, column=1)
        
    def center_dialog(self, parent):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
    
    def browse_path(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)
    
    def create_project(self):
        name = self.name_entry.get().strip()
        path = self.path_entry.get().strip()
        
        if not name:
            self.name_entry.configure(border_color="red")
            return
            
        if not os.path.exists(path):
            self.path_entry.configure(border_color="red")
            return
            
        project_path = os.path.join(path, name)
        self.destroy()
        self.callback(name, project_path)


class ProjectManager:
    def __init__(self):
        self.app = ctk.CTk()
        self.projects_file = "projects.json"
        self.projects = []
        self.selected_project = None
        self.selected_bg_color = "#1e6ba8"
        self.selected_fg_color = "white"
        self.default_fg_color = "white"
        self.path_fg_color = "gray"
        
        # Setup window first
        self.setup_window()
        
        # Define template path
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "core", "editor", "template"
        )
        
        # Then load assets and create widgets
        self.load_assets()
        self.load_projects()
        self.create_widgets()
        
    def setup_window(self):
        self.app.title("Project Manager")
        self.app.geometry("900x600")
        self.app.minsize(800, 500)
        
        # Center the window immediately after setting geometry
        self.center_window()
        
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        
    def center_window(self):
        """Properly center the window on screen"""
        # Update the window to calculate its actual size
        self.app.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        
        # Get window dimensions
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set geometry with calculated position
        self.app.geometry(f"+{x}+{y}")
        
    def load_assets(self):
        self.icons = {
            "new_project": self.create_placeholder_icon(),
            "import": self.create_placeholder_icon(),
            "scan": self.create_placeholder_icon(),
            "folder": self.create_placeholder_icon(),
            "project": self.create_placeholder_icon(size=(64,64)),
            "open": self.create_placeholder_icon(),
            "run": self.create_placeholder_icon()
        }
        
    def create_placeholder_icon(self, size=(16,16)):
        img = Image.new("RGBA", size, (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, size[0]-1, size[1]-1], outline="gray")
        return ctk.CTkImage(img)
        
    def load_projects(self):
        try:
            with open(self.projects_file, "r") as f:
                self.projects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.projects = []
            
    def save_projects(self):
        with open(self.projects_file, "w") as f:
            json.dump(self.projects, f, indent=2)
            
    def create_widgets(self):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Main content area
        self.main_content = ctk.CTkFrame(self.app, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nswe")
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # Sidebar buttons
        ctk.CTkLabel(self.sidebar, text="Projects", font=("Arial", 14, "bold")).grid(
            row=0, column=0, padx=10, pady=(20, 10), sticky="w")
            
        self.new_btn = ctk.CTkButton(
            self.sidebar,
            text="New Project",
            command=self.new_project,
            image=self.icons["new_project"],
            compound="left",
            anchor="w"
        )
        self.new_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")
        
        self.import_btn = ctk.CTkButton(
            self.sidebar,
            text="Import",
            command=self.import_project,
            image=self.icons["import"],
            compound="left",
            anchor="w"
        )
        self.import_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        
        self.scan_btn = ctk.CTkButton(
            self.sidebar,
            text="Scan Projects",
            command=self.scan_projects,
            image=self.icons["scan"],
            compound="left",
            anchor="w"
        )
        self.scan_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")
        
        # Action buttons
        self.open_btn = ctk.CTkButton(
            self.sidebar,
            text="Open Project",
            command=self.open_selected_project,
            image=self.icons["open"],
            compound="left",
            anchor="w",
            state="disabled"
        )
        self.open_btn.grid(row=4, column=0, padx=10, pady=(20,5), sticky="we")
        
        self.run_btn = ctk.CTkButton(
            self.sidebar,
            text="Run Project",
            command=self.run_project,
            image=self.icons["run"],
            compound="left",
            anchor="w",
            state="disabled"
        )
        self.run_btn.grid(row=5, column=0, padx=10, pady=5, sticky="we")
        
        # Version label
        ctk.CTkLabel(self.sidebar, text=f"Version: 0.1dev1").grid(
            row=7, column=0, padx=10, pady=(10, 20), sticky="w")
        
        # Project list
        self.project_frame = ctk.CTkScrollableFrame(self.main_content)
        self.project_frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        self.project_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_project_list()
        
    def refresh_project_list(self):
        # Remember which project was selected
        selected_path = self.selected_project["path"] if self.selected_project else None
        
        # Clear existing projects
        for widget in self.project_frame.winfo_children():
            widget.destroy()
        
        # Add current projects
        for i, project in enumerate(self.projects):
            card = self.add_project_card(project, i)
            
            # Re-select if it was the previously selected project
            if selected_path and project["path"] == selected_path:
                self.select_project_card(card)
    
    def add_project_card(self, project, index):
        card = ctk.CTkFrame(
            self.project_frame, 
            height=80,
            fg_color="transparent",
            border_width=1,
            border_color="gray20"
        )
        card.grid(row=index, column=0, sticky="we", pady=(0, 10))
        card.grid_columnconfigure(1, weight=1)
        
        # Store project reference in card
        card.project_data = project
        card.is_selected = False
        
        # Project icon
        icon = ctk.CTkLabel(card, text="", image=self.icons["project"], width=60)
        icon.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        
        # Project info
        name_label = ctk.CTkLabel(
            card, 
            text=project["name"], 
            font=("Arial", 14, "bold"), 
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="we", padx=(0, 10), pady=(10, 0))
        
        path_label = ctk.CTkLabel(
            card, 
            text=project["path"], 
            text_color=self.path_fg_color, 
            anchor="w"
        )
        path_label.grid(row=1, column=1, sticky="we", padx=(0, 10), pady=(0, 10))
        
        modified_label = ctk.CTkLabel(
            card, 
            text=f"Modified: {project['modified']}", 
            anchor="e"
        )
        modified_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="ns")
        
        # Store references to labels
        card.labels = [name_label, path_label, modified_label, icon]
        
        # Hover effects
        def on_enter(e):
            if not card.is_selected:
                card.configure(border_color="gray40")
                
        def on_leave(e):
            if not card.is_selected:
                card.configure(border_color="gray20")
                
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Click handling
        card.bind("<Button-1>", lambda e, c=card: self.select_project_card(c))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, c=card: self.select_project_card(c))
            
        return card
    
    def select_project_card(self, card):
        # Deselect all other cards first
        for existing_card in self.project_frame.winfo_children():
            if hasattr(existing_card, 'is_selected') and existing_card.is_selected:
                self.deselect_card(existing_card)
        
        # Select the clicked card
        card.configure(fg_color=self.selected_bg_color)
        for label in card.labels:
            if label == card.labels[1]:  # Path label
                label.configure(text_color=self.selected_fg_color)
            else:
                label.configure(text_color=self.selected_fg_color)
        card.is_selected = True
        
        # Update selected project
        self.selected_project = card.project_data
        self.open_btn.configure(state="normal")
        self.run_btn.configure(state="normal")
    
    def deselect_card(self, card):
        card.configure(fg_color="transparent")
        for label in card.labels:
            if label == card.labels[1]:  # Path label
                label.configure(text_color=self.path_fg_color)
            else:
                label.configure(text_color=self.default_fg_color)
        card.is_selected = False
        card.configure(border_color="gray20")
    
    def new_project(self):
        NewProjectDialog(self.app, self.create_new_project)
    
    def create_new_project(self, name, path):
        project_path = os.path.join(path, name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create project from template
        self.create_from_template(project_path, name)
        
        # Add to projects list
        project_data = {
            "name": name,
            "path": project_path,
            "version": "0.1dev1",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "modified": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.projects.append(project_data)
        self.save_projects()
        self.refresh_project_list()
        
        # Open the project in editor
        self.open_project(project_path)
    
    def create_from_template(self, project_path, project_name):
        """Create project structure from template"""
        # Copy template files
        if os.path.exists(self.template_path):
            try:
                # Copy entire template directory
                shutil.copytree(
                    self.template_path, 
                    project_path, 
                    dirs_exist_ok=True
                )
                
                # Update project.axie file
                axie_path = os.path.join(project_path, "project.axie")
                if os.path.exists(axie_path):
                    with open(axie_path, "r") as f:
                        axie_data = json.load(f)
                    
                    # Update with project-specific data
                    axie_data["name"] = project_name
                    axie_data["version"] = "0.1dev1"
                    created = datetime.now().strftime("%Y-%m-%d %H:%M")
                    axie_data["created"] = created
                    axie_data["modified"] = created
                    
                    with open(axie_path, "w") as f:
                        json.dump(axie_data, f, indent=2)
            except Exception as e:
                print(f"Error creating from template: {str(e)}")
        else:
            print(f"Template path not found: {self.template_path}")
    
    def open_project(self, project_path):
        """Open project in editor"""
        print(f"Opening project: {project_path}")
        # In real implementation, this would launch the editor
        # from components.core.editor import editor
        # editor.run(project_path)
    
    def import_project(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            # Verify it's a valid project
            if not os.path.exists(os.path.join(path, "project.axie")):
                print("Not a valid project: missing project.axie file")
                return
                
            name = os.path.basename(path)
            project_data = {
                "name": name,
                "path": path,
                "version": "0.1dev1",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "modified": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.projects.append(project_data)
            self.save_projects()
            self.refresh_project_list()
    
    def scan_projects(self):
        """Scan for projects and update metadata"""
        print("Scanning for projects...")
        updated_count = 0
        
        for project in self.projects:
            axie_path = os.path.join(project["path"], "project.axie")
            if os.path.exists(axie_path):
                try:
                    with open(axie_path, "r") as f:
                        axie_data = json.load(f)
                    
                    # Update metadata from project file
                    project["name"] = axie_data.get("name", project["name"])
                    project["version"] = axie_data.get("version", project["version"])
                    project["modified"] = axie_data.get("modified", project["modified"])
                    updated_count += 1
                except:
                    print(f"Failed to read project file: {axie_path}")
        
        if updated_count:
            self.save_projects()
            self.refresh_project_list()
            print(f"Updated {updated_count} projects")
    
    def open_selected_project(self):
        if self.selected_project:
            self.open_project(self.selected_project["path"])
    
    def run_project(self):
        if self.selected_project:
            print(f"Running project: {self.selected_project['name']}")
            # In real implementation, this would launch the engine
            # from components.core.engine import engine
            # engine.run(self.selected_project["path"])
    
    def run(self):
        self.app.mainloop()

def run():
    pm = ProjectManager()
    pm.run()