import pygame
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((400,300))
    pygame.display.set_caption('Music Player')
    font = pygame.font.SysFont('Arial', 20)
    sfont = pygame.font.SysFont('Arial', 16)
    paused = False
    done = False

    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)
    pir = Player()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == SONG_END:
                pir.next_song()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                if event.key == pygame.K_p:
                    pir.play_current()
                if event.key == pygame.K_n:
                    pir.next_song()
                if event.key == pygame.K_b:
                    pir.prev_song()
                if event.key == pygame.K_s or event.key == pygame.K_SPACE:
                    pir.pause()

        screen.fill((30, 30, 30))

        label = font.render('Now Playing:', True, (171, 178, 191))
        screen.blit(label, (20, 100))
        
        song_label = font.render(pir.current_song_name, True, (97, 175, 239))
        screen.blit(song_label, (20, 130))

        status_text = 'PAUSED' if pir.paused else 'PLAYING'
        status_color = (224, 108, 117) if pir.paused else (152, 195, 121)
        status_label = sfont.render(f'Status: {status_text}', True, status_color)
        screen.blit(status_label, (20, 160))

        hint = sfont.render('SPACE: Pause | N: Next | B: Back | Q: Quit', True, (90, 90, 90))
        screen.blit(hint, (20, 260))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()    
        
