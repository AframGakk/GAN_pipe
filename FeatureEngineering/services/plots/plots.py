import matplotlib.pyplot as plt



def plot_audio(audio, frames=None):

    if frames:
        plt.figure(figsize=(16, 4))
        plt.plot(audio[:frames], '.')
        plt.plot(audio[:frames], '-')
        plt.show()
    else:
        plt.figure(figsize=(16, 4))
        plt.plot(audio[:], '.')
        plt.plot(audio[:], '-')
        plt.show()