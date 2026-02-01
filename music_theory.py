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

    def suggest_scales(self, concert_key_str):
        """
        Suggests scales based on the detected key string (e.g., 'C major').
        """
        k = self._get_key_obj(concert_key_str)
        tonic_name = k.tonic.name
        is_major = (k.mode == 'major')
        
        suggestions = {}
        if is_major:
            suggestions['Main Scale'] = f"{tonic_name} Major"
            suggestions['Pentatonic'] = f"{tonic_name} Major Pentatonic"
            suggestions['Blues'] = f"{tonic_name} Major Blues"
            suggestions['Relative Minor'] = f"{k.relative.tonic.name} Minor"
        else:
            suggestions['Main Scale'] = f"{tonic_name} Minor"
            suggestions['Pentatonic'] = f"{tonic_name} Minor Pentatonic"
            suggestions['Blues'] = f"{tonic_name} Minor Blues"
            suggestions['Relative Major'] = f"{k.relative.tonic.name} Major"
            
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
