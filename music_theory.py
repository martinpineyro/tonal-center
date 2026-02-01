import music21

class MusicTheoryHelper:
    def __init__(self):
        pass
        
    def _get_interval(self, instrument_type):
        if instrument_type == 'Bb':
            return music21.interval.Interval('M2')
        elif instrument_type == 'Eb':
            return music21.interval.Interval('M6')
        return None

    def _get_key_obj(self, key_str):
        # robustness against "A major" vs "A"
        parts = key_str.split(' ')
        tonic = parts[0]
        mode = 'major'
        if len(parts) > 1:
            mode = parts[1].lower()
        return music21.key.Key(tonic, mode)

    def _get_scale_notes(self, tonic_name, scale_type):
        """
        Returns a string of notes for the given tonic and scale type.
        """
        try:
            t = music21.pitch.Pitch(tonic_name)
            if scale_type == 'major':
                s = music21.scale.MajorScale(t)
                pitches = s.getPitches(t)
            elif scale_type == 'minor':
                s = music21.scale.MinorScale(t)
                pitches = s.getPitches(t)
            elif scale_type == 'major pentatonic':
                # Manually handle pentatonic as music21 doesn't have a direct simple class for all types
                intervals = ['P1', 'M2', 'M3', 'P5', 'M6']
                pitches = [t.transpose(i) for i in intervals]
            elif scale_type == 'minor pentatonic':
                intervals = ['P1', 'm3', 'P4', 'P5', 'm7']
                pitches = [t.transpose(i) for i in intervals]
            elif scale_type == 'major blues':
                intervals = ['P1', 'M2', 'm3', 'M3', 'P5', 'M6']
                pitches = [t.transpose(i) for i in intervals]
            elif scale_type == 'minor blues':
                intervals = ['P1', 'm3', 'P4', 'A4', 'P5', 'm7']
                pitches = [t.transpose(i) for i in intervals]
            else:
                return ""
            
            return " ".join([p.name.replace('-', 'b') for p in pitches])
        except:
            return ""

    def suggest_scales(self, concert_key_str):
        """
        Suggests scales based on the detected key string (e.g., 'C major').
        Returns a dict: { type: { label: str, notes: str } }
        """
        k = self._get_key_obj(concert_key_str)
        tonic_name = k.tonic.name
        is_major = (k.mode == 'major')
        
        suggestions = {}
        if is_major:
            suggestions['Main Scale'] = {
                'label': f"{tonic_name} Major",
                'notes': self._get_scale_notes(tonic_name, 'major')
            }
            suggestions['Pentatonic'] = {
                'label': f"{tonic_name} Major Pentatonic",
                'notes': self._get_scale_notes(tonic_name, 'major pentatonic')
            }
            suggestions['Blues'] = {
                'label': f"{tonic_name} Major Blues",
                'notes': self._get_scale_notes(tonic_name, 'major blues')
            }
            suggestions['Relative Minor'] = {
                'label': f"{k.relative.tonic.name} Minor",
                'notes': self._get_scale_notes(k.relative.tonic.name, 'minor')
            }
        else:
            suggestions['Main Scale'] = {
                'label': f"{tonic_name} Minor",
                'notes': self._get_scale_notes(tonic_name, 'minor')
            }
            suggestions['Pentatonic'] = {
                'label': f"{tonic_name} Minor Pentatonic",
                'notes': self._get_scale_notes(tonic_name, 'minor pentatonic')
            }
            suggestions['Blues'] = {
                'label': f"{tonic_name} Minor Blues",
                'notes': self._get_scale_notes(tonic_name, 'minor blues')
            }
            suggestions['Relative Major'] = {
                'label': f"{k.relative.tonic.name} Major",
                'notes': self._get_scale_notes(k.relative.tonic.name, 'major')
            }
            
        return suggestions

    def get_instrument_suggestions(self, concert_key_str, instrument_type='Bb'):
        """
        Returns transposed scale suggestions.
        """
        interval = self._get_interval(instrument_type)
        if not interval:
            return self.suggest_scales(concert_key_str)
            
        k = self._get_key_obj(concert_key_str)
        transposed_k = k.transpose(interval)
        
        # music21 Key.name returns e.g. "D major" which we now handle safely in _get_key_obj
        return self.suggest_scales(transposed_k.name)

    def get_transposed_key(self, concert_key_str, instrument_type='Bb'):
        """
        Returns the name of the transposed key for a given instrument.
        """
        interval = self._get_interval(instrument_type)
        if not interval:
            return concert_key_str
            
        k = self._get_key_obj(concert_key_str)
        transposed_k = k.transpose(interval)
        return transposed_k.name

if __name__ == "__main__":
    helper = MusicTheoryHelper()
    concert = "A major"
    print(f"Concert: {concert}")
    try:
        print("Suggestions (Concert):", helper.suggest_scales(concert))
        print("Suggestions (Tenor Bb):", helper.get_instrument_suggestions(concert, 'Bb'))
        print("Suggestions (Alto Eb):", helper.get_instrument_suggestions(concert, 'Eb'))
    except Exception as e:
        import traceback
        traceback.print_exc()
