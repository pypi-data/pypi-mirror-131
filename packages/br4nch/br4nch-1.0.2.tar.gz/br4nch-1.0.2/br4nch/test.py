import br4nch

br4nch.add.branch(branch="Streaming", header="Movies & Series")
br4nch.add.layer(branch="Streaming", layer=["Netflix", "Prime Video"], position="0")
br4nch.add.layer(branch="Streaming", layer=["Movies", "Series"], position="*")
br4nch.add.layer(branch="Streaming", layer="Interstellar", position="1.1")
br4nch.add.layer(branch="Streaming", layer=["Squid Game", "The Crown"], position="1.2")
br4nch.add.layer(branch="Streaming", layer=["Tenet", "Parasite"], position="2.1")
br4nch.add.layer(branch="Streaming", layer="The Walking Dead", position="2.2")

br4nch.display.branch(branch="*")
