## Tkinter is part of python library so we don't need to install it
import tkinter as tk

from tkinter import filedialog ## it opens the file explorer dialog box

from tkinter import messagebox ## this is imported to get the drop down list

class Menubar:

	def __init__(self, parent):

		font_specs = ("windows",9)

		menubar = tk.Menu(parent.master, font = font_specs)

		## thus now in this code, we are creating a menubar and displaying it in the master window
		parent.master.config(menu=menubar)

		## place the dropdown in the menubar
		file_dropdown = tk.Menu(menubar, font = font_specs, tearoff=0) ## this tearoff is passed bcoz else we are able to take the 
		## File menu icon and move it anywhere, thus to keep it stable we pass this argument

		file_dropdown.add_command(label="New File", accelerator= "Ctrl+N" ,command=parent.new_file)
		file_dropdown.add_command(label="Open File",accelerator= "Ctrl+O" ,command=parent.open_file)
		file_dropdown.add_command(label="Save", accelerator= "Ctrl+S",command=parent.save)
		file_dropdown.add_command(label="Save As", accelerator= "Ctrl+Shift+S",command=parent.save_as)
		file_dropdown.add_separator()
		file_dropdown.add_command(label="Exit",command = parent.master.destroy)

		about_dropdown = tk.Menu(menubar,font = font_specs, tearoff=0)

		about_dropdown.add_command(label="Release Notes", command=self.show_release_notes)
		about_dropdown.add_separator()
		about_dropdown.add_command(label="About", command=self.show_about_message)

		menubar.add_cascade(label = "File" ,menu=file_dropdown)
		menubar.add_cascade(label = "About", menu=about_dropdown)


	def show_about_message(self):

		box_title = "About Pytext"
		box_message= "A cool python Text Editor made using Tkinter :)"

		messagebox.showinfo(box_title,box_message)


	def show_release_notes(self):

		box_title = "Notes"
		box_message= "Version 1.68"

		messagebox.showinfo(box_title,box_message)




class Statusbar:

	def __init__(self, parent):

		font_specs = ("windows",9)

		self.status = tk.StringVar() ## It allows us to create a string variable
		self.status.set("PyText - 0.1 Vian")

		label = tk.Label(parent.textarea, textvariable = self.status, fg="black", bg="lightgrey", anchor='sw', font=font_specs) ## fg=foreground, bg =background,
		## anchor tag is for position of the text,here it is south west

		label.pack(side=tk.BOTTOM, fill=tk.BOTH)


	def update_status(self, *args):

		if isinstance(args[0], bool): ## so this args[0] is the first parameter in the above *args and if it's boolean value id true then do the foll.
			self.status.set("Your file has been saved!")
		else:
			self.status.set("PyText - 0.1 Vian")




## This is going to be the main class
## functions like open the editor, save n all are going to come over here
class Pytext:

	def __init__(self,master):

		master.title("Vian")
		master.geometry("970x500")

		font_specs = ("windows",11)

		self.filename = None ## initially there won't be any file

		## as master is one of our main window so we need it's access everwhere
		## thus to pass it even in the Menubar class we write this
		self.master = master 

		self.textarea = tk.Text(master, font = font_specs)
		self.scroll = tk.Scrollbar(master, command = self.textarea.yview) ## yview means that scroll it in the Y-axis direction

		## but we just don't only want to scroll using the side scroll bar
		## that is we don't want to keep clicking the side bar for scrolling
		## but we also want to scroll it using the mouse
		self.textarea.configure(yscrollcommand = self.scroll.set)

		## this line of code is to place the textarea in the left place of scrollbar using geometry commands
		self.textarea.pack(side=tk.LEFT, fill=tk.BOTH , expand=True)
		## so here we say that place it to the left,
		## make it occupy the entire window screen,
		## if u try the third argument to be False, then it won't fit the entire screen, it will just be a square not touching the scrollbar



		## this line of code is to place the scrollbar in the rightmost place using geometry commands
		self.scroll.pack(side=tk.RIGHT, fill = tk.Y)
		## as for the scrollbar we just need it to take the Y-axis space so we write tk.Y


		self.menubar = Menubar(self)
		self.statusbar = Statusbar(self)

		self.bind_shortcuts()


## note here there are two reasons or cases when we are going to use the "name" parameter in set_window_title function

## 1st => when we open a file from the open_file function, we need to pass the name of opened file so that it's name comes at the top

## 2nd => when we just create a new file and don't assign any name to it, at that time we need the default name to be just "new document" or anyhting

	def set_window_title(self, name=None):
		
		if name:
			self.master.title(name + " = PyText")
		else:
			self.master.title("Vian")



	def new_file(self, *args):
		
		self.textarea.delete(1.0, tk.END)
		self.filename = None
		self.set_window_title()



	def open_file(self, *args):
		
		self.filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
																						("Text File" , "*.txt"),
																						("Python Scripts", "*.py"),
																						("Markdown Documents","*.md"),
																						("JavaScript Files", "*.js"),
																						("HTML Documents", "*.html"),
																						("CSS Documents","*.css")])
		if self.filename:
			self.textarea.delete(1.0,tk.END) ## first as we r opening a new file delete all the previous contents in the text area

			with open(self.filename, "r") as f: ## open the specific file in the read mode

				self.textarea.insert(1.0,f.read()) ## so now insert the contents of the file from the first character place

			self.set_window_title(self.filename)






	def save(self, *args):
		
		if self.filename:
			
			try:
				textarea_content = self.textarea.get(1.0,tk.END)
				with open(self.filename, "w") as f:
					f.write(textarea_content)
				self.statusbar.update_status(True)
			except Exception as e:
				print(e)

		else:
			self.save_as()





	def save_as(self, *args):
		
		try:
			new_file = filedialog.asksaveasfilename(initialfile ="Untitled.txt",defaultextension=".txt", filetypes=[("All Files", "*.*"),
																													("Text File" , "*.txt"),
																													("Python Scripts", "*.py"),
																													("Markdown Documents","*.md"),
																													("JavaScript Files", "*.js"),
																													("HTML Documents", "*.html"),
																													("CSS Documents","*.css")])


			textarea_content = self.textarea.get(1.0,tk.END) ## what this does is it takes all what so ever is written in the tetarea
															 ## currently and say copies it in the variable textarea_content
															 ## and then this is used in f.write(textarea_content) 

			with open(new_file, "w") as f:
				f.write(textarea_content)
			self.filename = new_file
			self.set_window_title(self.filename)
			self.statusbar.update_status(True)


		except Exception as e:
			print(e)




	def bind_shortcuts(self):

		self.textarea.bind('<Control-n>', self.new_file)
		self.textarea.bind('<Control-o>', self.open_file)
		self.textarea.bind('<Control-s>', self.save)
		self.textarea.bind('<Control-S>', self.save_as)
		self.textarea.bind('<Key>',self.statusbar.update_status)








##this is the code which is going to launch our program
if __name__ == "__main__":

	## master is actually the main window
	master = tk.Tk()
	pt = Pytext(master)
	master.mainloop()





















































