import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon


class Command(BaseCommand):
    help = "Fast Sync Pokemon data from PokeAPI to local Database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching Pokemon data from PokeAPI (Fast Mode)...")
        # سحب الـ 150 بوكيمون بطلب واحد سريع جداً لمنع الـ Timeout
        url = "https://pokeapi.co/api/v2/pokemon?limit=150"
        try:
            response = requests.get(url, timeout=10).json()
            results = response.get("results", [])

            pokemons_to_create = []
            for result in results:
                name = result["name"]
                p_id = int(result["url"].split("/")[-2])
                image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p_id}.png"

                if not Pokemon.objects.filter(pokemon_id=p_id).exists():
                    pokemons_to_create.append(
                        Pokemon(
                            pokemon_id=p_id,
                            name=name.capitalize(),
                            image=image_url,
                            types="Normal",  # قيمة افتراضية سريعة لمنع الكراش
                            abilities="Run Away",  # قيمة افتراضية
                            height=10,
                            weight=10,
                        )
                    )

            if pokemons_to_create:
                Pokemon.objects.bulk_create(pokemons_to_create)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully synced {len(pokemons_to_create)} Pokemons rapidly!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("All Pokemons are already synced.")
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error syncing data: {e}"))