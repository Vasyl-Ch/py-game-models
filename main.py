import json
import init_django_orm  # noqa: F401


from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as data_file:
        players = json.load(data_file)

    for nickname, data in players.items():
        guild_obj = None
        guild_data = data.get("guild")

        if guild_data:
            guild_description = guild_data["description"]

            guild_defaults = {}
            if guild_description is not None:
                guild_defaults["description"] = guild_description

            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults=guild_defaults
            )

        race_data = data.get("race")
        race_obj, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data["description"]}
        )

        for skill in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill["name"],
                race=race_obj,
                defaults={"bonus": skill["bonus"]}

            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": data["email"],
                "bio": data["bio"],
                "race": race_obj,
                "guild": guild_obj
            }
        )


if __name__ == "__main__":
    main()
