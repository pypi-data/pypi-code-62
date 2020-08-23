import unittest

import nlpaug.augmenter.word as naw


class TestRandom(unittest.TestCase):
    def test_swap(self):
        texts = [
            'The quick brown fox jumps over the lazy dog'
        ]
        aug = naw.RandomWordAug(action="swap")

        for text in texts:
            tokens = text.lower().split(' ')
            orig_token_freq = {}
            for w in tokens:
                orig_token_freq[w] = tokens.count(w)

            augmented_text = text

            # https://github.com/makcedward/nlpaug/issues/77
            for i in range(10):
                augmented_text = aug.augment(augmented_text)

            aug_tokens = augmented_text.lower().split(' ')
            aug_token_freq = {}
            for w in tokens:
                aug_token_freq[w] = aug_tokens.count(w)

            for orig_token, orig_freq in orig_token_freq.items():
                self.assertTrue(orig_token in aug_token_freq)
                self.assertTrue(aug_token_freq[orig_token] == orig_freq)

            self.assertNotEqual(text, augmented_text)

    def test_substitute_without_target_word(self):
        texts = [
            'The quick brown fox jumps over the lazy dog'
        ]
        aug = naw.RandomWordAug(action='substitute')

        for text in texts:
            augmented_text = aug.augment(text)

            self.assertIn('_', augmented_text)
            self.assertNotEqual(text, augmented_text)

    def test_substitute_with_target_word(self):
        texts = [
            'The quick brown fox jumps over the lazy dog'
        ]
        target_words = ['$', '#', '^^^']
        aug = naw.RandomWordAug(action='substitute', target_words=target_words)

        for text in texts:
            augmented_text = aug.augment(text)

            replaced = False
            for w in target_words:
                if w in augmented_text:
                    replaced = True
                    break
            self.assertTrue(replaced)
            self.assertNotEqual(text, augmented_text)

    def test_delete(self):
        texts = [
            'The quick brown fox jumps over the lazy dog'
        ]
        aug = naw.RandomWordAug()

        for text in texts:
            augmented_text = aug.augment(text)
            self.assertNotEqual(text, augmented_text)

    # https://github.com/makcedward/nlpaug/issues/76
    def test_swap_one_token(self):
        texts = [
            'The'
        ]
        aug = naw.RandomWordAug(action='swap')

        for text in texts:
            augmented_text = aug.augment(text)

            self.assertEqual(text, augmented_text)

    # https://github.com/makcedward/nlpaug/issues/76
    def test_delete_one_token(self):
        texts = [
            'The'
        ]
        aug = naw.RandomWordAug(action='delete')

        for text in texts:
            augmented_text = aug.augment(text)
            self.assertEqual(text, augmented_text)


    def test_crop(self):
        texts = [
            'The quick brown fox jumps over the lazy dog'
        ]
        aug = naw.RandomWordAug(action='crop', include_detail=True)

        for text in texts:
            orig_tokens = text.split(' ')

            augmented_text, change_logs = aug.augment(text)
            start_pos = -1
            for change_log in change_logs:
                crop_token = change_log['orig_token']
                
                for i, t in enumerate(orig_tokens[start_pos:]):
                    if t == crop_token:
                        if start_pos == -1:
                            start_pos == i
                        elif start_pos + 1 == i:
                            start_pos == i
                        else:
                            self.assertTrue(False)