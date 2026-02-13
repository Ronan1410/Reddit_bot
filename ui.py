import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from bot import post_to_reddit, get_reddit

CONFIG_FILE = 'posts_config.json'

class RedditBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Reddit Bot Manager')
        self.root.geometry('1000x700')
        self.posts = []
        self.subreddits = []
        self.load_config()
        
        self.create_widgets()
    
    def load_config(self):
        """Load posts and subreddits from config file"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self.posts = data.get('posts', [])
                self.subreddits = data.get('subreddits', [])
    
    def save_config(self):
        """Save posts and subreddits to config file"""
        data = {
            'posts': self.posts,
            'subreddits': self.subreddits
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Subreddit management
        left_frame = ttk.LabelFrame(main_frame, text='Subreddits', padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Subreddit listbox
        subreddit_scroll = ttk.Scrollbar(left_frame)
        subreddit_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.subreddit_listbox = tk.Listbox(
            left_frame,
            yscrollcommand=subreddit_scroll.set,
            height=20
        )
        self.subreddit_listbox.pack(fill=tk.BOTH, expand=True)
        subreddit_scroll.config(command=self.subreddit_listbox.yview)
        
        # Subreddit input
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.subreddit_entry = ttk.Entry(input_frame, width=20)
        self.subreddit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            input_frame,
            text='Add',
            command=self.add_subreddit
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Button(
            input_frame,
            text='Remove',
            command=self.remove_subreddit
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_subreddit_list()
        
        # Right panel - Post management
        right_frame = ttk.LabelFrame(main_frame, text='Posts', padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Post listbox
        post_scroll = ttk.Scrollbar(right_frame)
        post_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.post_listbox = tk.Listbox(
            right_frame,
            yscrollcommand=post_scroll.set,
            height=15
        )
        self.post_listbox.pack(fill=tk.BOTH, expand=True)
        self.post_listbox.bind('<<ListboxSelect>>', self.on_post_select)
        post_scroll.config(command=self.post_listbox.yview)
        
        # Post buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text='New Post',
            command=self.new_post
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text='Edit',
            command=self.edit_post
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text='Delete',
            command=self.delete_post
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text='Post Now',
            command=self.post_now
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_post_list()
        
        # Post details panel
        details_frame = ttk.LabelFrame(self.root, text='Post Details', padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Details text area
        self.details_text = tk.Text(details_frame, height=10, width=100)
        self.details_text.pack(fill=tk.BOTH, expand=True)
    
    def add_subreddit(self):
        subreddit = self.subreddit_entry.get().strip()
        if not subreddit:
            messagebox.showwarning('Input Error', 'Please enter a subreddit name')
            return
        
        if subreddit in self.subreddits:
            messagebox.showwarning('Duplicate', f'r/{subreddit} already added')
            return
        
        self.subreddits.append(subreddit)
        self.subreddit_entry.delete(0, tk.END)
        self.refresh_subreddit_list()
        self.save_config()
    
    def remove_subreddit(self):
        selection = self.subreddit_listbox.curselection()
        if not selection:
            messagebox.showwarning('Selection Error', 'Please select a subreddit')
            return
        
        subreddit = self.subreddit_listbox.get(selection[0])
        self.subreddits.remove(subreddit)
        self.refresh_subreddit_list()
        self.save_config()
    
    def refresh_subreddit_list(self):
        self.subreddit_listbox.delete(0, tk.END)
        for sub in self.subreddits:
            self.subreddit_listbox.insert(tk.END, f'r/{sub}')
    
    def refresh_post_list(self):
        self.post_listbox.delete(0, tk.END)
        for i, post in enumerate(self.posts):
            title = post.get('title', 'Untitled')
            subreddit = post.get('subreddit', 'Unknown')
            self.post_listbox.insert(tk.END, f'{i+1}. {title} → r/{subreddit}')
    
    def on_post_select(self, event):
        selection = self.post_listbox.curselection()
        if not selection:
            return
        
        post = self.posts[selection[0]]
        details = f"Title: {post.get('title', 'N/A')}\n\n"
        details += f"Subreddit: r/{post.get('subreddit', 'N/A')}\n\n"
        details += f"Type: {post.get('type', 'N/A')}\n\n"
        
        if post.get('type') == 'image':
            details += f"Image: {post.get('image_path', 'N/A')}\n\n"
            details += f"Description:\n{post.get('description', '')}"
        elif post.get('type') == 'text':
            details += f"Content:\n{post.get('content', '')}"
        elif post.get('type') == 'link':
            details += f"URL: {post.get('url', 'N/A')}"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def new_post(self):
        PostEditWindow(self, None)
    
    def edit_post(self):
        selection = self.post_listbox.curselection()
        if not selection:
            messagebox.showwarning('Selection Error', 'Please select a post')
            return
        
        PostEditWindow(self, selection[0])
    
    def delete_post(self):
        selection = self.post_listbox.curselection()
        if not selection:
            messagebox.showwarning('Selection Error', 'Please select a post')
            return
        
        del self.posts[selection[0]]
        self.refresh_post_list()
        self.save_config()
    
    def post_now(self):
        selection = self.post_listbox.curselection()
        if not selection:
            messagebox.showwarning('Selection Error', 'Please select a post')
            return
        
        post = self.posts[selection[0]]
        
        if messagebox.askyesno('Confirm', f"Post '{post['title']}' to r/{post['subreddit']} now?"):
            try:
                reddit = get_reddit()
                if post_to_reddit(reddit, post):
                    messagebox.showinfo('Success', 'Post submitted successfully!')
                else:
                    messagebox.showerror('Error', 'Failed to post. Check credentials.')
            except Exception as e:
                messagebox.showerror('Error', f'Error: {str(e)}')


class PostEditWindow:
    def __init__(self, parent_ui, post_index):
        self.parent_ui = parent_ui
        self.post_index = post_index
        self.window = tk.Toplevel(parent_ui.root)
        self.window.title('Edit Post' if post_index is not None else 'New Post')
        self.window.geometry('600x500')
        
        if post_index is not None:
            self.post = parent_ui.posts[post_index].copy()
        else:
            self.post = {'type': 'image'}
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text='Title:').grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(frame, width=50)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW)
        self.title_entry.insert(0, self.post.get('title', ''))
        
        # Subreddit
        ttk.Label(frame, text='Subreddit:').grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.subreddit_var = tk.StringVar(value=self.post.get('subreddit', ''))
        self.subreddit_combo = ttk.Combobox(
            frame,
            textvariable=self.subreddit_var,
            values=self.parent_ui.subreddits,
            width=47
        )
        self.subreddit_combo.grid(row=1, column=1, sticky=tk.EW, pady=(10, 0))
        
        # Type
        ttk.Label(frame, text='Type:').grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.type_var = tk.StringVar(value=self.post.get('type', 'image'))
        type_combo = ttk.Combobox(
            frame,
            textvariable=self.type_var,
            values=['image', 'text', 'link'],
            width=47,
            state='readonly'
        )
        type_combo.grid(row=2, column=1, sticky=tk.EW, pady=(10, 0))
        type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Image path (for image posts)
        ttk.Label(frame, text='Image:').grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.image_frame = ttk.Frame(frame)
        self.image_frame.grid(row=3, column=1, sticky=tk.EW, pady=(10, 0))
        self.image_entry = ttk.Entry(self.image_frame, width=40)
        self.image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.image_entry.insert(0, self.post.get('image_path', ''))
        ttk.Button(
            self.image_frame,
            text='Browse',
            command=self.browse_image
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Description/Content
        ttk.Label(frame, text='Description/Content:').grid(row=4, column=0, sticky=tk.NW, pady=(10, 0))
        self.content_text = tk.Text(frame, height=8, width=50)
        self.content_text.grid(row=4, column=1, sticky=tk.EW, pady=(10, 0))
        content = self.post.get('description') or self.post.get('content', '')
        self.content_text.insert(1.0, content)
        
        # URL (for link posts)
        ttk.Label(frame, text='URL:').grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
        self.url_entry = ttk.Entry(frame, width=50)
        self.url_entry.grid(row=5, column=1, sticky=tk.EW, pady=(10, 0))
        self.url_entry.insert(0, self.post.get('url', ''))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text='Save', command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Cancel', command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(1, weight=1)
        self.on_type_change()
    
    def on_type_change(self):
        post_type = self.type_var.get()
        if post_type == 'image':
            self.image_frame.grid()
        else:
            self.image_frame.grid_remove()
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[('Images', '*.png *.jpg *.jpeg *.gif'), ('All Files', '*.*')]
        )
        if filename:
            self.image_entry.delete(0, tk.END)
            self.image_entry.insert(0, filename)
    
    def save(self):
        title = self.title_entry.get().strip()
        subreddit = self.subreddit_var.get().strip()
        post_type = self.type_var.get()
        
        if not title or not subreddit:
            messagebox.showwarning('Input Error', 'Title and subreddit are required')
            return
        
        self.post['title'] = title
        self.post['subreddit'] = subreddit
        self.post['type'] = post_type
        
        if post_type == 'image':
            image_path = self.image_entry.get().strip()
            if not image_path:
                messagebox.showwarning('Input Error', 'Image path is required')
                return
            self.post['image_path'] = image_path
            self.post['description'] = self.content_text.get(1.0, tk.END).strip()
        elif post_type == 'text':
            self.post['content'] = self.content_text.get(1.0, tk.END).strip()
        elif post_type == 'link':
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning('Input Error', 'URL is required')
                return
            self.post['url'] = url
        
        if self.post_index is not None:
            self.parent_ui.posts[self.post_index] = self.post
        else:
            self.parent_ui.posts.append(self.post)
        
        self.parent_ui.refresh_post_list()
        self.parent_ui.save_config()
        self.window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = RedditBotUI(root)
    root.mainloop()
