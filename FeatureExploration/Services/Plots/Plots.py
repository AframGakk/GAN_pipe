import matplotlib.pyplot as plt
import seaborn as sns

class Plots:

    def plot_sound_heat(self, wave):
        plt.figure(figsize=(10, 10))
        axes = plt.gca()
        axes.set_xlim([0, 20])
        axes.set_ylim([0, 5])
        plt.imshow(wave, cmap='hot', interpolation='nearest')

    def plot_audio(self, data, name):
        plt.title(name)
        plt.xlabel('Hz')
        plt.ylabel('Spectrum')
        plt.plot(data, '-')

    def plot_audio_ext(self, data, name, hz):
        plt.title(name)
        plt.xlabel('Hz')
        plt.ylabel('Spectrum')
        plt.figure(figsize=(16, 4))
        plt.plot(data[:hz], '.')
        plt.plot(data[:hz], '-')

    def sound_length_violinplot(self, records):
        _, ax = plt.subplots(figsize=(16, 4))
        sns.violinplot(ax=ax, x="types", y="nframes", data=records)
        plt.xticks(rotation=90)
        plt.title('Distribution of audio frames, per label', fontsize=16)
        plt.show()