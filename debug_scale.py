import music21
t = music21.pitch.Pitch('A')
s = music21.scale.MajorScale(t)
pitches = s.getPitches(t, t.transpose('P8'))
print("Major Pitches:", [str(p) for p in pitches])

# Try without end
pitches_no_end = s.getPitches(t) # This usually returns all but often needs a range
print("Pitches default:", [str(p) for p in pitches_no_end])
