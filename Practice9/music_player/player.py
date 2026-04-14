import pygame
import os

playlist = []
index = 0
playing = False
folder = "music"

def init_player():
    global playlist
    playlist = sorted(os.listdir(folder))


def load_song():
    path = os.path.join(folder, playlist[index])
    pygame.mixer.music.load(path)


def play():
    global playing
    pygame.mixer.music.play()
    playing = True


def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False


def next_song():
    global index
    index = (index + 1) % len(playlist)
    load_song()
    if playing:
        play()


def prev_song():
    global index
    index = (index - 1) % len(playlist)
    load_song()
    if playing:
        play()


def get_current_song():
    return playlist[index]