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
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#e6f7ff")  # Light blue background
        self.pokedex = Pokedex()
        self.current_pokemon = None
        self._build_interface()
        self._configure_styles()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), foreground="#2c3e50")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#34495e")
        style.configure("Normal.TLabel", font=("Segoe UI", 11), foreground="#7f8c8d")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TEntry", font=("Segoe UI", 10), padding=4)
        # Removed TFrame and Card.TFrame styles as using tk.Frame

    def _build_interface(self):
        main_frame = tk.Frame(self.root, bg="#e6f7ff", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main_frame, text="🔍 Pokedex Search", style="Title.TLabel")
        title.pack(pady=(0, 20))

        search_frame = tk.Frame(main_frame, bg="#e6f7ff")
        search_frame.pack(fill=tk.X, pady=(0, 20))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50, style="TEntry")
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_entry.bind("<Return>", lambda event: self.search_pokemon())

        search_button = ttk.Button(search_frame, text="🔍 Search", command=self.search_pokemon, style="TButton")
        search_button.pack(side=tk.LEFT, padx=(0, 5))

        random_button = ttk.Button(search_frame, text="🎲 Random", command=self.search_random, style="TButton")
        random_button.pack(side=tk.LEFT)

        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=(0, 20))

        self.result_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        help_label = ttk.Label(main_frame, text="Enter a Pokemon name or ID and click Search, or click Random for a surprise!", style="Normal.TLabel")
        help_label.pack(pady=(10, 0))

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
        """Display Pokemon information with sprite, types, stats, and moves, themed by type."""
        if not pokemon:
            return

        self._clear_result_frame()
        self.current_pokemon = pokemon

        # Theme based on primary type
        primary_type = pokemon.types[0] if pokemon.types else "normal"
        theme_color = TYPE_COLORS.get(primary_type, "#A8A878")
        self.result_frame.configure(style="Card.TFrame")  # Reset to base
        # Note: ttk doesn't easily allow dynamic background changes, so we'll use tk widgets for accents

        left_panel = tk.Frame(self.result_frame, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, padx=(0, 16), pady=8, anchor=tk.N)

        sprite_image = self._load_sprite(pokemon.sprite_url)
        if sprite_image:
            self._sprite_image = sprite_image
            sprite_label = tk.Label(left_panel, image=sprite_image, bg="white")
            sprite_label.pack(pady=10, anchor=tk.N)
        else:
            no_sprite = tk.Label(left_panel, text="No Image Available", bg="white", width=20, height=10, font=("Segoe UI", 10), fg="#7f8c8d")
            no_sprite.pack(pady=10, anchor=tk.N)

        right_panel = tk.Frame(self.result_frame, bg="white")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)

        name_label = tk.Label(right_panel, text=f"{pokemon.name.upper()} #{pokemon.id}", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        name_label.pack(anchor=tk.W, pady=(0, 8))

        type_frame = tk.Frame(right_panel, bg="white")
        type_frame.pack(anchor=tk.W, pady=(0, 12))
        tk.Label(type_frame, text="Types:", font=("Segoe UI", 12, "bold"), bg="white", fg="#34495e").pack(side=tk.LEFT, padx=(0, 8))
        for ptype in pokemon.types:
            color = TYPE_COLORS.get(ptype, "#888888")
            badge = tk.Label(
                type_frame,
                text=ptype.upper(),
                bg=color,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                padx=10,
                pady=5,
                relief=tk.RAISED,
                bd=1
            )
            badge.pack(side=tk.LEFT, padx=4)

        info_frame = tk.Frame(right_panel, bg="white")
        info_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
        tk.Label(info_frame, text=f"Height: {pokemon.height} dm", font=("Segoe UI", 11), bg="white", fg="#7f8c8d").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"Weight: {pokemon.weight} hg", font=("Segoe UI", 11), bg="white", fg="#7f8c8d").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"Abilities: {', '.join(pokemon.abilities)}", font=("Segoe UI", 11), bg="white", fg="#7f8c8d").pack(anchor=tk.W)

        stats_frame = tk.LabelFrame(right_panel, text="Stats", bg="white", fg="#2c3e50", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        stats_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
        for stat_name, value in pokemon.stats.items():
            stat_row = tk.Frame(stats_frame, bg="white")
            stat_row.pack(anchor=tk.W, fill=tk.X, pady=3)
            tk.Label(stat_row, text=f"{stat_name.title()}:", width=10, font=("Segoe UI", 10), bg="white", fg="#34495e").pack(side=tk.LEFT)
            tk.Label(stat_row, text=f"{value}", width=4, font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(side=tk.LEFT, padx=(8, 0))
            progress = tk.Canvas(stat_row, width=200, height=15, bg="white", highlightthickness=0)
            progress.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)
            progress.create_rectangle(0, 0, min(value / 255 * 200, 200), 15, fill=theme_color, outline="")

        moves_frame = tk.LabelFrame(right_panel, text="Moves", bg="white", fg="#2c3e50", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        moves_frame.pack(anchor=tk.W, fill=tk.X)
        if pokemon.moves:
            moves_text = ", ".join(pokemon.moves[:8])
        else:
            moves_text = "No moves available"
        tk.Label(moves_frame, text=moves_text, font=("Segoe UI", 10), bg="white", fg="#7f8c8d", wraplength=500, justify=tk.LEFT).pack(anchor=tk.W)

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
