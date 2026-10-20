#!/bin/bash
frasi=(
  "Nacho ha appena mangiato tutti i nachos della festa! 🧀"
  "Ciocco è dolce fuori ma un vero hacker dentro! 🍫"
  "Leggenda narra che Nacho e Ciocco abbiano vinto la maratona a mente!"
  "Attenzione: Ciocco ha appena attivato la modalità super saiyan!"
  "Nacho dice che Ciocco ne sa sempre una più del diavolo."
)
echo "${frasi[$RANDOM % ${#frasi[@]}]}"

