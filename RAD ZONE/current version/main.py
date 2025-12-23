import pygame
import os
from game import Game

# -------- AUDIO CONFIG (MUST COME FIRST) --------
pygame.mixer.pre_init(
    frequency=44100,                # SAMPLE RATE
    size=-16,                       # 16 BIT
    channels=2,                     # STEREO/MONO
    buffer=8192                     # Stable music + low-latency SFX
)

pygame.init()                       # Initializes all pygame modules INCLUDING mixer
pygame.mixer.set_num_channels(64)   # SETS THE NUMBER OF AUDIO CHANNELS
pygame.mixer.set_reserved(8)        # Protects SFX channels from music

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('RAD ZONE')

# -------- STARTUP SOUND --------
# startup_sound = pygame.mixer.Sound('RAD ZONE/current version/Audio/pygame.wav')
# startup_sound.play()

# -------- FUNCTION TO PLAY ANIMATED LOGO --------
def play_nacho_logo(screen, clock, folder_path='RAD ZONE/current version/Graphics/Nacho Logo Animation', fps=24):
    # Load all PNG frames in order
    frames = []
    frame_files = sorted(f for f in os.listdir(folder_path) if f.startswith("frame") and f.endswith(".png"))
    
    for file in frame_files:
        img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        frames.append(img)

    startup_sound = pygame.mixer.Sound('RAD ZONE/current version/Audio/pygame.wav')
    startup_sound.play()

    # Compute centered rectangles for each frame
    rects = [frame.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) for frame in frames]

    # Play frames
    for frame, rect in zip(frames, rects):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        screen.blit(frame, rect)
        pygame.display.flip()
        clock.tick(fps)

# -------- PLAY ANIMATED LOGO --------
# play_nacho_logo(screen, clock)
# pygame.time.delay(500)  # optional pause before starting game

# -----------------------------------------------
Game().run()
