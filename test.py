import math
import random
import mido

#              C       D       E       F       G       A       B
FREQUENCIES = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]

DURATION_QUARTER = 480
DURATION_HALF = 2 * DURATION_QUARTER
DURATION_WHOLE = 2 * DURATION_HALF

MELODY_LENGTH = 4800 

def generate_random_melody(length, num_notes=10, max_simultaneous_notes=3, seed=None):
    if seed is not None:
        random.seed(seed)
    
    melody = []
    
    for _ in range(num_notes):
        current_time = 0
        while current_time < length:
            num_simultaneous_notes = random.randint(1, max_simultaneous_notes)
            frequencies = random.choices(FREQUENCIES, k=num_simultaneous_notes)
            duration = random.choice([DURATION_QUARTER, DURATION_HALF, DURATION_WHOLE])
            for freq in frequencies:
                midi_note = int(69 + 12 * (math.log2(freq / 440)))
                note_on = mido.Message('note_on', note=midi_note, velocity=64, time=current_time)
                note_off = mido.Message('note_off', note=midi_note, velocity=64, time=current_time + duration)
                melody.extend([note_on, note_off])
            current_time += duration
    
    return melody

# Melody generation part ----------------------------------------------------------------------------------------------------
num_melodies = 5
combined_melody = []
for i in range(num_melodies):
    melody = generate_random_melody(MELODY_LENGTH, num_notes=random.randint(5, 15), max_simultaneous_notes=3, seed=i)
    combined_melody.extend(melody)

combined_melody = sorted(combined_melody, key=lambda msg: msg.time)

random_suffix = ''.join(random.choices('0123456789', k=6))
file_name = f"Song_{random_suffix}.mid"

midi = mido.MidiFile()
track = mido.MidiTrack()
midi.tracks.append(track)
for msg in combined_melody:
    track.append(msg)

midi.save(file_name)

print(f"Combined melody saved as {file_name}")
