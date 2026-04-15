import tkinter as tk
from tkinter import messagebox, ttk

from app.pokedex import Pokedex


class PokeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokedex Search")
        self.root.geometry("640x560")
        self.pokedex = Pokedex()
        self._build_interface()

    def _build_interface(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="Pokedex Search", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(0, 12))

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, pady=(0, 12))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=32)
        search_entry.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)
        search_entry.bind("<Return>", lambda event: self.search_pokemon())

        search_button = ttk.Button(search_frame, text="Search", command=self.search_pokemon)
        search_button.pack(side=tk.LEFT)

        random_button = ttk.Button(search_frame, text="Random Pokemon", command=self.search_random)
        random_button.pack(side=tk.LEFT, padx=(8, 0))

        self.result_text = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED, width=72, height=24)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        help_label = ttk.Label(frame, text="Enter a Pokemon name or ID, then click Search. Click Random to display a random Pokemon.")
        help_label.pack(pady=(12, 0))

    def _display_result(self, pokemon):
        if not pokemon:
            return

        lines = [
            f"Name: {pokemon.name.title()}",
            f"ID: {pokemon.id}",
            f"Types: {', '.join(pokemon.types)}",
            f"Abilities: {', '.join(pokemon.abilities)}",
            f"Height: {pokemon.height} dm",
            f"Weight: {pokemon.weight} hg",
            "Stats:",
        ]

        for stat_name, value in pokemon.stats.items():
            lines.append(f"  - {stat_name.title()}: {value}")

        lines.append(f"Sprite URL: {pokemon.sprite_url}")
        lines.append("Moves:")
        lines.extend([f"  - {move}" for move in pokemon.moves])

        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(lines))
        self.result_text.configure(state=tk.DISABLED)

    def search_pokemon(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Search required", "Please enter a Pokemon name or ID.")
            return

        try:
            pokemon = self.pokedex.search(query)
            self._display_result(pokemon)
        except ValueError as error:
            messagebox.showerror("Pokemon not found", str(error))
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
