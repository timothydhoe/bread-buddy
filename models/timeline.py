"""
filename: timeline.py
---------------------

BakeTimeline model. Generates a full bake schedule working backward
from a target "bread ready" datetime.

Scientific basis: The Sourdough Framework by Hendrik Kleinwächter.
Fermentation adjustment factor (1.12) matches dough.py.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


FERMENTATION_ADJUSTMENT_FACTOR = 1.12  # ~10-15% change per °C, matches dough.py
REFERENCE_TEMP = 21.0  # °C baseline for fermentation calculations


@dataclass
class BakeStep:
    time: datetime
    label: str
    description: str
    milestone: bool = False
    cue: str = ""

    @property
    def day_str(self):
        return self.time.strftime("%A %d %b")

    @property
    def hour_str(self):
        return self.time.strftime("%H:%M")


class BakeTimeline:
    """Generates a full chronological bake schedule.

    Works backward from a target 'bread ready' datetime. All timing estimates
    are grounded in The Sourdough Framework's fermentation science.

    Bread type configurations:
        flatbread     — stove-only, very accessible, any flour
        loaf_pan      — oven required, forgiving, any flour
        freestanding  — Dutch oven, highest skill, gluten flour required
    """

    CONFIGS = {
        "flatbread": {
            "cooling_mins": 5,
            "bake_mins": 10,       # 5 min each side on stove
            "preheat_mins": 0,
            "base_bulk_hours": 6.0,  # wait for 50% rise; reference at 21°C
            "room_proof_hours": 0,   # no separate proofing step for flatbread
            "cold_proof_hours": 0,
            "num_stretch_folds": 0,
            "supports_cold_proof": False,
        },
        "loaf_pan": {
            "cooling_mins": 30,
            "bake_mins": 40,       # 200°C
            "preheat_mins": 20,
            "base_bulk_hours": 4.5,  # reference at 21°C
            "room_proof_hours": 2,
            "cold_proof_hours": 10,
            "num_stretch_folds": 2,
            "supports_cold_proof": True,
        },
        "freestanding": {
            "cooling_mins": 90,
            "bake_mins": 45,       # 20 min lid on + 25 min lid off
            "preheat_mins": 60,    # Dutch oven must be fully heated
            "base_bulk_hours": 5.0,  # reference at 21°C
            "room_proof_hours": 3,
            "cold_proof_hours": 12,
            "num_stretch_folds": 4,
            "supports_cold_proof": True,
        },
    }

    @staticmethod
    def adjusted_bulk_hours(base_hours: float, room_temp: float) -> float:
        """Adjust bulk fermentation time for actual room temperature.

        Uses the same 1.12 factor as Dough.calculate_fermentation_time().
        Capped at 1.5h–18h to avoid unrealistic extremes.
        """
        factor = FERMENTATION_ADJUSTMENT_FACTOR ** (REFERENCE_TEMP - room_temp)
        return round(min(max(base_hours * factor, 1.5), 18.0), 1)

    @staticmethod
    def starter_feed_hours(room_temp: float) -> float:
        """Hours before mixing that starter should be fed.

        Based on 8h at 20°C, scaled by the same 1.12 temperature factor.
        Capped between 5h and 14h for practical use.
        """
        factor = FERMENTATION_ADJUSTMENT_FACTOR ** (20.0 - room_temp)
        return round(min(max(8.0 * factor, 5.0), 14.0), 1)

    @classmethod
    def generate(
        cls,
        target_datetime: datetime,
        room_temp: float = 20.0,
        starter_pct: float = 0.10,
        proofing_method: str = "cold",
        autolyse_mins: int = 30,
        bread_type: str = "freestanding",
    ) -> list:
        """Generate a complete bake schedule.

        Args:
            target_datetime: When the bread should be ready to eat.
            room_temp: Ambient temperature in °C.
            starter_pct: Starter as decimal fraction of flour (0.10 = 10%).
            proofing_method: "room_temp" or "cold" (retard overnight).
            autolyse_mins: Autolyse rest in minutes. 0 to skip.
            bread_type: One of "flatbread", "loaf_pan", "freestanding".

        Returns:
            List of BakeStep objects sorted chronologically.
        """
        cfg = cls.CONFIGS.get(bread_type, cls.CONFIGS["freestanding"])
        steps = []
        t = target_datetime  # anchor; we work backward from here

        # ── READY TO EAT ────────────────────────────────────────────────
        steps.append(BakeStep(
            time=t,
            label="Ready to eat",
            description="Your bread is ready. You made that. Well done.",
            milestone=True,
        ))

        # ── COOLING ─────────────────────────────────────────────────────
        t -= timedelta(minutes=cfg["cooling_mins"])
        if bread_type == "flatbread":
            steps.append(BakeStep(t, "Off the stove",
                "Wrap in a clean kitchen towel to keep soft and warm. "
                "Flatbreads are best eaten immediately. They do not improve with waiting."))
        elif bread_type == "loaf_pan":
            steps.append(BakeStep(t, "Out of the oven",
                "Rest in the pan for 10 minutes, then turn out onto a rack. "
                "Internal temperature should have reached 92°C / 198°F."))
        else:
            steps.append(BakeStep(t, "Out of the oven",
                "Place on a wire rack. Do not cut it yet: the crumb is still "
                "setting inside. Wait the full 90 minutes for best results. "
                "It will be worth it.",
                cue="Tap the bottom: it should sound hollow, like knocking on a wooden door. "
                    "The internal temperature should read 96°C / 205°F. The crust will "
                    "crackle as it cools, which is one of the better sounds in cooking. Do not cut it. "
                    "The crumb is still setting and cutting early produces a gummy, dense slice. "
                    "Ninety minutes. Then eat."))

        # ── BAKE ────────────────────────────────────────────────────────
        if bread_type == "flatbread":
            t -= timedelta(minutes=cfg["bake_mins"])
            steps.append(BakeStep(t, "Cook on the stove",
                "Medium heat, lightly oiled pan. Cover with a lid while cooking: "
                "trapped steam makes the bread fluffier. Golden-brown on the bottom "
                "(about 5 minutes), then flip and cook 5 minutes more.",
                milestone=True))

        elif bread_type == "loaf_pan":
            t -= timedelta(minutes=cfg["bake_mins"])
            steps.append(BakeStep(t, "Bake at 200°C (390°F) for 40 min",
                "Place pan in the centre of the oven. Check at 30 minutes. "
                "If the top is browning too fast, tent it loosely with foil. "
                "Done when the internal temperature reaches 92°C.",
                milestone=True))

        else:  # freestanding
            t -= timedelta(minutes=25)
            steps.append(BakeStep(t, "Remove lid: bake uncovered 25 min",
                "Carefully remove the hot lid and continue at 230°C. "
                "The crust will develop its colour and crunch. "
                "Done when the internal temperature reaches 96°C / 205°F.",
                cue="By now the loaf should have sprung up visibly and the score should be open. "
                    "The surface will be pale gold: that is correct. The next 25 minutes build colour and crunch. "
                    "Pull it when the internal temperature reaches 96°C, or when the crust is deep amber "
                    "and sounds hollow when you tap the bottom."))
            t -= timedelta(minutes=20)
            steps.append(BakeStep(t, "Score and load: lid on for 20 min",
                "Work quickly: score the cold dough with a sharp lame or razor at a "
                "30-45 degree angle. Lower into the screaming-hot Dutch oven. "
                "Lid on immediately. Trapped steam is what gives you oven spring.",
                milestone=True,
                cue="Work fast: the Dutch oven loses heat every second it is open. The cold dough "
                    "should feel firm and hold its shape on the board. Score decisively at "
                    "30-45 degrees, one confident cut. Hesitant scoring drags and tears. "
                    "Get the lid on within 30 seconds of opening the oven."))

        # ── PREHEAT ─────────────────────────────────────────────────────
        if cfg["preheat_mins"] > 0:
            t -= timedelta(minutes=cfg["preheat_mins"])
            if bread_type == "freestanding":
                steps.append(BakeStep(t, "Preheat oven to 230°C with Dutch oven inside",
                    "Place the empty Dutch oven (lid on) in the oven and heat for a full 60 minutes. "
                    "This is not optional. A cold Dutch oven will ruin your oven spring completely."))
            else:
                steps.append(BakeStep(t, "Preheat oven to 200°C",
                    "Grease your loaf pan generously with oil or butter. "
                    "Remove the dough from the fridge now if you cold-proofed it."))

        # ── PROOFING + SHAPING ──────────────────────────────────────────
        if bread_type == "flatbread":
            bulk_hours = cls.adjusted_bulk_hours(cfg["base_bulk_hours"], room_temp)
            t -= timedelta(hours=bulk_hours)
            mix_time = t
            steps.append(BakeStep(t, "Mix all ingredients and wait for 50% rise",
                f"Mix flour, water, starter, and salt until fully combined. "
                f"Cover tightly. At {room_temp}°C, expect roughly {bulk_hours:.1f} hours. "
                f"Ready when the dough has grown at least 50% in size and "
                f"you can see active bubbles on the sides and surface.",
                milestone=True))

        else:
            # Proofing step (working backward from preheat/bake start)
            use_cold = proofing_method == "cold" and cfg["supports_cold_proof"]

            if use_cold:
                cold_h = cfg["cold_proof_hours"]
                shape_time = t - timedelta(hours=cold_h)
                steps.append(BakeStep(shape_time, f"Shape and refrigerate for {cold_h}h (overnight)",
                    f"Shape your loaf. Freestanding: place seam-side-up in a well-floured banneton. "
                    f"Loaf pan: place seam-side-down in an oiled pan. Cover with plastic wrap and "
                    f"into the fridge for {cold_h} hours. The cold retard develops flavour and "
                    f"gives you a firm, scoreable dough. Bake straight from cold: do not let it warm up first.",
                    milestone=True,
                    cue="The shaped loaf should feel taut on the surface, like a drum skin pulled tight. "
                        "If it is spreading sideways immediately, the gluten needs more work: rest it "
                        "20 minutes uncovered, then reshape. Once in the banneton, the cold will firm "
                        "it up and it will hold its shape beautifully for scoring."))
                t = shape_time
            else:
                room_h = cfg["room_proof_hours"]
                shape_time = t - timedelta(hours=room_h)
                steps.append(BakeStep(shape_time, f"Shape and proof at room temperature: roughly {room_h}h",
                    f"Shape your loaf and place in a banneton or oiled pan. Cover. "
                    f"At {room_temp}°C expect roughly {room_h} hours. "
                    f"Use the poke test: a well-proofed loaf springs back slowly when gently pressed.",
                    milestone=True,
                    cue="Taut surface first, like a drum skin pulled tight. Then the poke test: gently "
                        "press a floured finger about 1cm into the dough. Slow spring-back with a small "
                        "indent remaining means it is ready. Instant spring-back means it needs more time. "
                        "No spring-back at all means it is over-proofed: get it in the oven immediately."))
                t = shape_time

            # ── BULK FERMENTATION ────────────────────────────────────────
            bulk_hours = cls.adjusted_bulk_hours(cfg["base_bulk_hours"], room_temp)
            mix_time = t - timedelta(hours=bulk_hours)

            steps.append(BakeStep(t, "Bulk fermentation done: shape now",
                f"At {room_temp}°C bulk takes roughly {bulk_hours:.1f} hours. Signs it is ready: "
                f"the dough has grown 50-75%, the surface is domed and jiggly, "
                f"bubbles are visible on the sides, and the dough pulls away from the bowl cleanly.",
                milestone=True,
                cue="The dough should have grown 50-75% in volume. Tip the bowl gently: it should "
                    "wobble like jelly. The surface should be domed, not flat or sunken. Bubbles should "
                    "be visible on the sides and ideally the bottom. The dough should feel airy and pull "
                    "away from the bowl cleanly. If it smells strongly alcoholic or over-yeasty, it has "
                    "gone a little too far. Shape it immediately and get it cold."))

            # ── STRETCH & FOLDS ──────────────────────────────────────────
            num_sf = cfg["num_stretch_folds"]
            for i in range(1, num_sf + 1):
                sf_time = mix_time + timedelta(minutes=30 * i)
                if sf_time < t - timedelta(minutes=30):
                    steps.append(BakeStep(sf_time, f"Stretch and fold #{i}",
                        "Wet your hands. Grab one side of the dough, stretch it upward as far as it "
                        "will go without tearing, then fold it over the centre. Rotate 90 degrees. "
                        "Repeat four times total. Cover and rest. This builds gluten strength "
                        "without any of the effort of traditional kneading.",
                        cue="After each set the dough should feel a little more taut and elastic than before. "
                            "By the final set the surface should look smooth and the dough should briefly "
                            "hold its shape when released, rather than immediately spreading flat. "
                            "That resistance is gluten doing exactly what it should."))

            # ── MIX ─────────────────────────────────────────────────────
            if autolyse_mins > 0:
                add_starter_time = mix_time + timedelta(minutes=autolyse_mins)
                steps.append(BakeStep(add_starter_time, "Add starter and salt",
                    "Autolyse rest done. Add your active starter and salt. "
                    "Squeeze the dough through your fingers to incorporate everything fully. "
                    "It will feel slimy at first. Keep working for 2-3 minutes.",
                    cue="The salt makes the dough feel briefly slimy and stringy. That is completely normal. "
                        "Keep squeezing it through your fingers for 2-3 minutes until it becomes uniform. "
                        "It should end up slightly tacky rather than wet and sticky."))
                steps.append(BakeStep(mix_time, f"Autolyse: mix flour and water only",
                    f"Combine flour and water until no dry patches remain. "
                    f"Cover and rest for {autolyse_mins} minutes. The autolyse lets amylase and "
                    f"protease work quietly: building sugars and softening gluten before the "
                    f"starter and salt join the party.",
                    milestone=True,
                    cue="The dough will look rough and shaggy at this point. That is fine. "
                        "You are only looking for no dry flour patches. Cover it, leave it alone, "
                        "and resist the urge to prod it. After the rest it will feel noticeably "
                        "smoother and more willing to cooperate."))
            else:
                steps.append(BakeStep(mix_time, "Mix all ingredients",
                    "Combine flour, water, active starter, and salt. "
                    "Pinch and fold until fully incorporated. No dry spots.",
                    milestone=True,
                    cue="No dry patches, no flour streaks. The dough will look rough and lumpy: that is fine. "
                        "It should feel tacky but not wet and unmanageably sticky. Cover it and let it rest."))

        # ── STARTER FEEDING ──────────────────────────────────────────────
        feed_hours = cls.starter_feed_hours(room_temp)
        feed_time = mix_time - timedelta(hours=feed_hours)

        if starter_pct <= 0.05:
            ratio = "1:10:10"
        elif starter_pct <= 0.12:
            ratio = "1:5:5"
        else:
            ratio = "1:5:2.5"

        steps.append(BakeStep(feed_time,
            "Feed your starter",
            f"Feed at a {ratio} ratio (old starter : flour : water). "
            f"At {room_temp}°C it should peak in roughly {feed_hours:.0f} hours. "
            f"Use it when it has doubled, the top is domed, and it smells "
            f"tangy and faintly yeasty.",
            milestone=True,
            cue="Ready when it has doubled in size, the top is domed rather than flat or sunken, "
                "you can see active bubbles on the sides of the jar, and it smells tangy and faintly yeasty. "
                "Float test: drop a small spoonful into a glass of water. If it floats, you are ready. "
                "If it sinks, give it more time."))

        steps.sort(key=lambda s: s.time)
        return steps
