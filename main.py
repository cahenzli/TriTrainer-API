from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

class AthleteProfile(BaseModel):
    age: int
    weight: float
    ftp: int  # Watt beim Radfahren
    vvo2max: float  # Geschwindigkeit in m/s oder min/km umgerechnet
    hf_max: int
    hf_rest: int
    training_days_per_week: int
    goal: str  # Sprint, Olympisch, 70.3, Ironman

class Workout(BaseModel):
    day: str
    sport: str
    title: str
    description: str
    target: str

def calculate_hf_zone(hf_max, hf_rest, intensity_percent):
    """Berechne Herzfrequenz-Zielzone basierend auf Karvonen-Formel"""
    return int(((hf_max - hf_rest) * intensity_percent) + hf_rest)

@app.post("/generate-trainingplan", response_model=List[Workout])
def generate_trainingplan(profile: AthleteProfile):
    plan = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_days = random.sample(days, profile.training_days_per_week)

    for day in selected_days:
        sport = random.choice(["Swim", "Bike", "Run", "Strength"])

        if sport == "Swim":
            target_pace = f"CSS Pace + {random.randint(3,8)} sec/100m"
            workout = Workout(
                day=day,
                sport="Swim",
                title="Intervall-Session Schwimmen",
                description="8x50m Technik, 4x200m moderat",
                target=target_pace
            )

        elif sport == "Bike":
            target_watt = int(profile.ftp * random.uniform(0.85, 1.05))
            workout = Workout(
                day=day,
                sport="Bike",
                title="FTP-Training Rad",
                description="5x6min Intervalle bei 90-105% FTP",
                target=f"{target_watt} Watt"
            )

        elif sport == "Run":
            target_pace = round((60 / profile.vvo2max) * random.uniform(0.9, 1.05), 2)
            workout = Workout(
                day=day,
                sport="Run",
                title="Tempolauf / Intervalle",
                description="6x400m schnell, Pausen joggen",
                target=f"{target_pace} min/km"
            )

        elif sport == "Strength":
            workout = Workout(
                day=day,
                sport="Strength",
                title="Krafttraining Ganzkörper",
                description="Kniebeugen, Bankdrücken, Klimmzüge, Core",
                target="3x12 Wiederholungen moderat schwer"
            )

        plan.append(workout)

    return plan
