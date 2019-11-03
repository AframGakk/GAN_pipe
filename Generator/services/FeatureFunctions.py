import soundfile as sf
from scipy import signal
import librosa
import numpy as np
import os

hparams = {
    'sample_rate': 16000,
    'ref_level_db': 20,
    'preemphasis': 0.97,
    'ref_level_db': 20,
    'min_level_db': -80,
    'griffin_lim_iters': 60,
    'frame_shift_ms': 8.0,
    'frame_length_ms ': 16.0,
    'num_freq': 1013,
    'num_mels': 128
}

# Conversions:
_mel_basis = None
_inv_mel_basis = None


def generate_images(self, generator_model):
    """Feeds random seeds into the generator and tiles and saves the output to a PNG file."""
    test_image_stack = generator_model.generate_sound(np.random.rand(10, 100))

    output_dir = './tmp/'

    # generate and save sample audio file for each epoch
    for i in range(4):
        w = test_image_stack[i]
        outfile = os.path.join(output_dir, "train_audio_.wav")
        self.save_audio(w, outfile)


def save_audio(self, y, path):
    """ generate a wav file from a given spectrogram and save it """
    s = np.squeeze(y)
    # s = self.denormalize(s)
    w = self.inv_melspectrogram(s)
    self.save_wav(w, path)


def denormalize(self, norm_s):
    """ normalized spectrogram to original spectrogram using the calculated mean/standard deviation """

    assert norm_s.shape[0] == mel_means.shape[0]
    Y = (norm_s * (3.0 * mel_stds)) + mel_means
    return Y


def inv_spectrogram(self, spectrogram):
    S = self._db_to_amp(self._denormalize(spectrogram) + hparams['ref_level_db'])  # Convert back to linear
    return self._inv_preemphasis(self._griffin_lim(S ** 1.5))  # Reconstruct phase


def _mel_to_linear(self, mel_spectrogram):
    global _inv_mel_basis
    if _inv_mel_basis is None:
        _inv_mel_basis = np.linalg.pinv(self._build_mel_basis())
    return np.maximum(1e-10, np.dot(_inv_mel_basis, mel_spectrogram))


def inv_melspectrogram(self, melspectrogram):
    S = self._mel_to_linear(self._db_to_amp(self._denormalize(melspectrogram)))  # Convert back to linear
    return self._inv_preemphasis(self._griffin_lim(S ** 1.5))  # Reconstruct phase


def _build_mel_basis(self):
    n_fft = (hparams['num_freq'] - 1) * 2
    return librosa.filters.mel(hparams['sample_rate'], n_fft, n_mels=hparams['num_mels'])


def _inv_preemphasis(self, x):
    return signal.lfilter([1], [1, -hparams['preemphasis']], x)


def save_wav(self, wav, path):
    sf.write(path, wav, 16000, subtype='PCM_16')  # 16000 sample rate


def _denormalize(self, S):
    return (np.clip(S, 0, 1) * -hparams['min_level_db']) + hparams['min_level_db']


def _db_to_amp(self, x):
    return np.power(10.0, x * 0.05)


def _griffin_lim(self, S):
    angles = np.exp(2j * np.pi * np.random.rand(*S.shape))
    S_complex = np.abs(S).astype(np.complex)
    for i in range(hparams['griffin_lim_iters']):
        if i > 0:
            angles = np.exp(1j * np.angle(self._stft(y)))
        y = self._istft(S_complex * angles)
    return y


def _istft(self, y):
    hop_length = int(hparams['frame_shift_ms'] / 1000. * hparams['sample_rate'])
    win_length = int(hparams['frame_length_ms '] / 1000. * hparams['sample_rate'])
    return librosa.istft(y, hop_length=hop_length, win_length=win_length)


def _stft(self, y):
    n_fft = (hparams['num_freq'] - 1) * 2
    hop_length = int(hparams['frame_shift_ms'] / 1000. * hparams['sample_rate'])
    win_length = int(hparams['frame_length_ms'] / 1000. * hparams['sample_rate'])
    return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)