import random
import datetime

# 30 Pre-written Rolls Royce Scripts
SCRIPTS = [
    "Rolls Royce. Where dreams meet engineering. Every Spirit of Ecstasy takes over 5 hours to polish by hand. The iconic V12 engine whispers at just 40 decibels. Silence is luxury. Power is effortless. From the Phantom to the Cullinan, each vehicle is a masterpiece. This isn't just transportation. It's a statement. It's legacy. It's the pinnacle of automotive excellence.",
    "The Rolls Royce Phantom. 450 hours of handcrafted perfection. The paint alone requires 5 coats and 3 weeks to cure. Lamb's wool carpets. Starlight headliner with 1,600 fiber optic lights. The doors close with a whisper. The ride floats on air suspension. This is what happens when engineering meets art. This is automotive royalty.",
    "1904. Henry Royce met Charles Rolls. A partnership that changed luxury forever. From the Silver Ghost to today's Spectre EV, one principle remains. Perfection is not optional. Every detail matters. Every surface is flawless. The Spirit of Ecstasy leads the way. Rolls Royce. The ultimate driving machine for those who prefer to be driven.",
    "The Rolls Royce Cullinan. Named after the largest diamond ever discovered. This SUV redefines luxury off-road. 563 horsepower. Twin-turbo V12. Yet it glides like a sedan. Viewing suite in the rear. Champagne fridge included. Power meets practicality. Adventure meets elegance. This is how royalty explores the world.",
    "Bespoke. That word defines Rolls Royce. Want your initials in gold thread? Done. Custom paint matching your favorite flower? Possible. Picnic tables in the doors? Standard. Each car takes 6 months to build. Each one is unique. This isn't mass production. This is personal luxury at its finest."
]

def generate_rolls_royce_script():
    """Pick a random Rolls Royce script from the collection"""
    today = datetime.date.today()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    script = random.choice(SCRIPTS)
    print(f"✅ Script selected")
    print(f"📝 Length: {len(script)} characters")
    return script

if __name__ == "__main__":
    script = generate_rolls_royce_script()
    print(f"\n📝 Script:\n{script}")
  
