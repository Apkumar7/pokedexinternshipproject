import tkinter as tk
from io import BytesIO
from tkinter import messagebox, ttk
from urllib.request import urlopen

from PIL import Image, ImageTk

from app.pokedex import Pokedex

TYPE_COLORS = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC",
}


class PokeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokedex Search")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.pokedex = Pokedex()
        self.current_pokemon = None
        self._build_interface()
        self._configure_styles()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Normal.TLabel", font=("Segoe UI", 10))

    def _build_interface(self):
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main_frame, text="🔍 Pokedex Search", style="Title.TLabel")
        title.pack(pady=(0, 16))

        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 16))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)
        search_entry.bind("<Return>", lambda event: self.search_pokemon())

        search_button = ttk.Button(search_frame, text="Search", command=self.search_pokemon)
        search_button.pack(side=tk.LEFT, padx=(0, 4))

        random_button = ttk.Button(search_frame, text="Random", command=self.search_random)
        random_button.pack(side=tk.LEFT)

        canvas = tk.Canvas(main_frame, bg="white", height=1, highlightthickness=0)
        canvas.pack(fill=tk.X, pady=(0, 16))
        canvas.create_line(0, 0, 900, 0, fill="#cccccc", width=1)

        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        help_label = ttk.Label(main_frame, text="Enter a Pokemon name or ID and click Search, or click Random for a surprise!")
        help_label.pack(pady=(12, 0))

    def _load_sprite(self, url):
        """Load and return a PhotoImage from a URL."""
        if not url:
            return None
        try:
            with urlopen(url, timeout=5) as response:
                image_data = response.read()
            image = Image.open(BytesIO(image_data))
            image = image.resize((200, 200), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def _clear_result_frame(self):
        """Remove all widgets from the result frame."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def _display_result(self, pokemon):
        """Display Pokemon information with sprite, types, stats, and moves."""
        if not pokemon:
            return

        self._clear_result_frame()
        self.current_pokemon = pokemon

        left_panel = ttk.Frame(self.result_frame)
        left_panel.pack(side=tk.LEFT, padx=(0, 16), pady=8)

        sprite_image = self._load_sprite(pokemon.sprite_url)
        if sprite_image:
            self._sprite_image = sprite_image
            sprite_label = tk.Label(left_panel, image=sprite_image, bg="white", relief=tk.RAISED)
            sprite_label.pack()
        else:
            no_sprite = tk.Label(left_panel, text="No image", bg="white", width=20, height=10)
            no_sprite.pack()

        right_panel = ttk.Frame(self.result_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)

        name_label = ttk.Label(right_panel, text=f"{pokemon.name.upper()} #{pokemon.id}", style="Header.TLabel")
        name_label.pack(anchor=tk.W, pady=(0, 8))

        type_frame = ttk.Frame(right_panel)
        type_frame.pack(anchor=tk.W, pady=(0, 12))
        ttk.Label(type_frame, text="Types:", style="Normal.TLabel").pack(side=tk.LEFT, padx=(0, 8))
        for ptype in pokemon.types:
            color = TYPE_COLORS.get(ptype, "#888888")
            badge = tk.Label(
                type_frame,
                text=ptype.upper(),
                bg=color,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                padx=8,
                pady=4,
            )
            badge.pack(side=tk.LEFT, padx=4)

        info_frame = ttk.Frame(right_panel)
        info_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
        ttk.Label(info_frame, text=f"Height: {pokemon.height} dm", style="Normal.TLabel").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Weight: {pokemon.weight} hg", style="Normal.TLabel").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Abilities: {', '.join(pokemon.abilities)}", style="Normal.TLabel").pack(anchor=tk.W)

        stats_frame = ttk.LabelFrame(right_panel, text="Stats", padding=8)
        stats_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
        for stat_name, value in pokemon.stats.items():
            stat_row = ttk.Frame(stats_frame)
            stat_row.pack(anchor=tk.W, fill=tk.X, pady=2)
            ttk.Label(stat_row, text=f"{stat_name.title()}:", width=10, style="Normal.TLabel").pack(side=tk.LEFT)
            ttk.Label(stat_row, text=f"{value}", width=4, style="Normal.TLabel").pack(side=tk.LEFT, padx=(8, 0))
            progress_bar = ttk.Progressbar(stat_row, length=150, maximum=255, value=value)
            progress_bar.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)

        moves_frame = ttk.LabelFrame(right_panel, text="Moves", padding=8)
        moves_frame.pack(anchor=tk.W, fill=tk.X)
        moves_text = ", ".join(pokemon.moves[:6])
        ttk.Label(moves_frame, text=moves_text, style="Normal.TLabel", wraplength=400).pack(anchor=tk.W)

    def search_pokemon(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Search Required", "Please enter a Pokemon name or ID.")
            return

        try:
            pokemon = self.pokedex.search(query)
            self._display_result(pokemon)
        except ValueError as error:
            messagebox.showerror("Not Found", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to retrieve Pokemon data:\n{error}")

    def search_random(self):
        try:
            pokemon = self.pokedex.random_pokemon()
            self.search_var.set(pokemon.name)
            self._display_result(pokemon)
        except Exception as error:
            messagebox.showerror("Error", f"Unable to retrieve random Pokemon:\n{error}")

    def run(self):
        self.root.mainloop()
