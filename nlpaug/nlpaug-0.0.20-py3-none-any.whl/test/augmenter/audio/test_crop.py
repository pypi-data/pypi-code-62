import unittest
import os
import numpy as np
from dotenv import load_dotenv

import nlpaug.augmenter.audio as naa
from nlpaug.util import AudioLoader


class TestCrop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', '..', '.env'))
        load_dotenv(env_config_path)
        # https://freewavesamples.com/yamaha-v50-rock-beat-120-bpm
        cls.sample_wav_file = os.path.join(
            os.environ.get("TEST_DIR"), 'res', 'audio', 'Yamaha-V50-Rock-Beat-120bpm.wav'
        )
        cls.audio, cls.sampling_rate = AudioLoader.load_audio(cls.sample_wav_file)

    def test_empty_input(self):
        audio = np.array([])
        aug = naa.CropAug(sampling_rate=self.sampling_rate)
        augmented_audio = aug.augment(audio)

        self.assertTrue(np.array_equal(audio, augmented_audio))

    def test_substitute(self):
        aug = naa.CropAug(sampling_rate=self.sampling_rate)
        augmented_audio = aug.augment(self.audio)

        self.assertNotEqual(len(self.audio), len(augmented_audio))

    def test_coverage(self):
        aug = naa.CropAug(sampling_rate=self.sampling_rate, coverage=0.1)
        augmented_data = aug.augment(self.audio)
        audio_size = len(self.audio)
        augmented_size = len(augmented_data)
        expected_crop_size = len(self.audio) * (aug.model.zone[1] - aug.model.zone[0]) * 0.1

        self.assertTrue(-1 <= audio_size - augmented_size - expected_crop_size <= 1)

    def test_duration(self):
        duration = 1
        audio_size = len(self.audio)

        for _ in range(10):
            aug = naa.CropAug(sampling_rate=self.sampling_rate, duration=duration)
            aug.model.stateless = False
            augmented_data = aug.augment(self.audio)
            augmented_size = len(augmented_data)
            expected_crop_size = self.sampling_rate * duration

            self.assertGreater(audio_size, augmented_size)
            self.assertEqual(len(self.audio[aug.model.start_pos:aug.model.end_pos]), expected_crop_size)
